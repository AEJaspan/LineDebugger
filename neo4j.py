"""docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=none neo4j:latest"""

from neo4j import GraphDatabase
import json

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=None)

def create_log_entry(tx, entry):
    # Create a node for each line of code
    tx.run("""
        CREATE (log:LogEntry {
            line_number: $line_number,
            line_content: $line_content,
            function_name: $function_name,
            local_variables: $local_variables,
            global_variables: $global_variables
        })
        """,
        line_number=entry['line_number'],
        line_content=entry['line_content'],
        function_name=entry['function_name'],
        local_variables=str(entry['local_variables']),
        global_variables=str(entry['global_variables'])
    )

def create_relationship(tx, previous_line, current_line):
    # Create a relationship between consecutive lines of code
    tx.run("""
        MATCH (prev:LogEntry {line_number: $prev_line_number}),
              (curr:LogEntry {line_number: $curr_line_number})
        CREATE (prev)-[:NEXT]->(curr)
        """,
        prev_line_number=previous_line['line_number'],
        curr_line_number=current_line['line_number']
    )

# Load your log data
with open('debug_log.json', 'r') as file:
    log_data = json.load(file)

# Insert log entries and relationships
with driver.session() as session:
    for i, entry in enumerate(log_data):
        session.write_transaction(create_log_entry, entry)
        if i > 0:
            session.write_transaction(create_relationship, log_data[i-1], entry)

print("Data has been successfully inserted into Neo4j.")
with driver.session() as session:
    result = session.run("""
        MATCH (log:LogEntry)
        WHERE log.function_name = $function_name
        RETURN log.line_number, log.line_content, log.local_variables, log.global_variables
        """, function_name="target_function")

    for record in result:
        print(f"Line {record['log.line_number']}: {record['log.line_content']}")
