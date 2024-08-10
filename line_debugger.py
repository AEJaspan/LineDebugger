import linecache
import sys
import traceback
import json
import os

class Debugger:
    def __init__(self, script_path):
        self.script_path = os.path.abspath(script_path)
        self.execution_log = []

    def capture_state(self, frame):
        line_number = frame.f_lineno
        line_content = linecache.getline(self.script_path, line_number).strip()
        local_vars = frame.f_locals.copy()
        global_vars = frame.f_globals.copy()
        self.execution_log.append({
            'line_number': line_number,
            'line_content': line_content,
            'local_variables': local_vars,
            'global_variables': global_vars
        })

    def trace_calls(self, frame, event, arg):
        # Only trace calls that belong to the script
        # We check if the filename of the current frame is equal to the absolute path of the script
        if event == 'line' and (os.path.abspath(frame.f_code.co_filename) == self.script_path):
            self.capture_state(frame)
        return self.trace_calls

    def run_script(self):
        sys.settrace(self.trace_calls)
        try:
            with open(self.script_path, 'r') as script_file:
                exec(script_file.read(), {})
        except Exception:
            traceback.print_exc()
        finally:
            sys.settrace(None)
    
    def get_log(self):
        return self.execution_log

    def save_log(self, output_path):
        # Save or print the log as needed
        with open(output_path, 'w') as log_file:
            for entry in self.execution_log:
                log_file.write(f"Line {entry['line_number']}: {entry['line_content']}\n")
                log_file.write("Local Variables:\n")
                log_file.write(str(entry['local_variables']))
                log_file.write("\n")
                log_file.write("Global Variables:\n")
                log_file.write(str(entry['global_variables']))
                log_file.write("\n")

# Example usage:
# Example usage:
debugger = Debugger('example_script.py')
debugger.run_script()
debugger.save_log('debug_log.txt')
    
# debugger = Debugger('your_script.py')
# debugger.run_script()
log = debugger.get_log()
for entry in log:
    print(entry)

    # def __init__(self, script_path):
    #     self.script_path = script_path
    #     self.execution_log = []

    # def capture_state(self, frame, line_number):
    #     local_vars = frame.f_locals.copy()
    #     global_vars = frame.f_globals.copy()
    #     line_content = linecache.getline(self.script_path, line_number).strip()
    #     self.execution_log.append({
    #         'line_number': line_number,
    #         'line_content': line_content,
    #         'local_variables': local_vars,
    #         'global_variables': global_vars
    #     })

    # def trace_calls(self, frame, event, arg):
    #     if event == 'line':
    #         self.capture_state(frame, frame.f_lineno)
    #     return self.trace_calls

    # def run_script(self):
    #     sys.settrace(self.trace_calls)
    #     try:
    #         with open(self.script_path, 'r') as script_file:
    #             script_code = script_file.read()
    #             exec(script_code, {})
    #     except Exception:
    #         traceback.print_exc()
    #     finally:
    #         sys.settrace(None)
    
# # Example usage:
# debugger = Debugger('example_script.py')
# debugger.run_script()
# debugger.save_log('debug_log.txt')
