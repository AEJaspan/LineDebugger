"""docker run -d -p 8080:8080 semitechnologies/weaviate:latest"""
import weaviate
from sentence_transformers import SentenceTransformer
import json

# Initialize Weaviate client
client = weaviate.Client("http://localhost:8080")

# Define your schema
schema = {
    "classes": [
        {
            "class": "LogEntry",
            "properties": [
                {
                    "name": "line_number",
                    "dataType": ["int"],
                },
                {
                    "name": "line_content",
                    "dataType": ["text"],
                },
                {
                    "name": "function_name",
                    "dataType": ["text"],
                },
                {
                    "name": "call_stack",
                    "dataType": ["text[]"],
                },
                {
                    "name": "code_context",
                    "dataType": ["text[]"],
                },
                {
                    "name": "local_variables",
                    "dataType": ["text[]"],
                },
                {
                    "name": "global_variables",
                    "dataType": ["text[]"],
                }
            ],
            "vectorizer": "none",  # we'll handle vectorization manually
        }
    ]
}

# Create the schema in Weaviate
client.schema.create(schema)

# Load your log data
with open('debug_log.json', 'r') as file:
    log_data = json.load(file)

# Initialize the embedding model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Insert log entries into Weaviate
for entry in log_data:
    text = f"Line {entry['line_number']}: {entry['line_content']} " \
           f"Function: {entry['function_name']} Context: {entry['code_context']}"
    vector = model.encode(text).tolist()

    # Prepare the data object
    data_object = {
        "line_number": entry['line_number'],
        "line_content": entry['line_content'],
        "function_name": entry['function_name'],
        "call_stack": entry['call_stack'],
        "code_context": [v for k, v in entry['code_context'].items()],
        "local_variables": [f"{k}: {v}" for k, v in entry['local_variables'].items()],
        "global_variables": [f"{k}: {v}" for k, v in entry['global_variables'].items()]
    }

    # Insert the data object with its vector
    client.data_object.create(
        data_object,
        "LogEntry",
        vector=vector
    )

print("Data has been successfully inserted into Weaviate.")
query_text = "target function with specific variables"
query_vector = model.encode(query_text).tolist()

result = client.query.get("LogEntry", ["line_number", "line_content", "function_name"]) \
    .with_near_vector({"vector": query_vector}) \
    .with_limit(5) \
    .do()

print("Search Results:")
for res in result['data']['Get']['LogEntry']:
    print(res)
