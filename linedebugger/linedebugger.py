import linecache
import sys
import traceback
import json
import os
import runpy
import io
import openai
from dotenv import load_dotenv

load_dotenv()

_PROMPT_TEMPLATE = """
Given the following stack trace, please explain how to fix the error.
Stack Trace: {stack_trace}
"""
USE_GENERATIVE_MODEL = True
GPT_MODEL = "gpt-3.5-turbo"
CLIENT = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


STANDARD_VARS = frozenset(
    [
        "__name__",
        "__doc__",
        "__package__",
        "__loader__",
        "__spec__",
        "__file__",
        "__cached__",
        "__builtins__",
    ]
)


def get_standard_vars() -> frozenset:
    """Returns a set of standard variable names."""
    return STANDARD_VARS


# def remove_standard_vars(d):
#     standard_vars = get_standard_vars()
#     return {k: v for k, v in d.items() if k not in standard_vars}


def remove_standard_vars(d):
    standard_vars = get_standard_vars()
    d_out = d.copy()
    for k in standard_vars:
        d_out.pop(k, None)
    return d_out


class Debugger:
    def __init__(self, script_path):
        print(script_path)
        self.script_path = script_path
        self.execution_log = []
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        self.output_capture = io.StringIO()
        self.error_capture = io.StringIO()
        self.error_explanation = ""

    def capture_state(self, frame, line_number, error=None):
        local_vars = remove_standard_vars(frame.f_locals)
        global_vars = remove_standard_vars(frame.f_globals)
        line_content = linecache.getline(self.script_path, line_number).strip()

        # Capture function name and calling stack
        function_name = frame.f_code.co_name
        call_stack = self.get_call_stack(frame)

        # Capture surrounding code context
        code_context = self.get_code_context(line_number)

        log_entry = {
            "line_number": line_number,
            "line_content": line_content,
            "local_variables": local_vars,
            "global_variables": global_vars,
            "function_name": function_name,
            "call_stack": call_stack,
            "code_context": code_context,
            "output": self.output_capture.getvalue(),
            "errors": self.error_capture.getvalue(),
        }
        if error:
            log_entry["__runtime_error"] = {
                "type": type(error).__name__,
                "message": str(error),
                "traceback": traceback.format_exc(),
            }
        self.execution_log.append(log_entry)

    def get_code_context(self, line_number, context_lines=2):
        start_line = max(1, line_number - context_lines)
        end_line = line_number + context_lines
        context = {}
        for i in range(start_line, end_line + 1):
            context[i] = linecache.getline(self.script_path, i).strip()
        return context

    def get_call_stack(self, frame):
        stack = []
        while frame:
            frame_info = {
                "file_name": frame.f_code.co_filename,
                "line_number": frame.f_lineno,
                "function_name": frame.f_code.co_name,
            }
            stack.append(frame_info)
            frame = frame.f_back
        return stack[::-1]  # Reverse to show the call order from start to current frame

    def trace_calls(self, frame, event, arg):
        # Only trace calls that belong to the script
        # We check if the filename of the current frame is equal to the absolute path of the script
        if event == "line" and frame.f_code.co_filename == self.script_path:
            print(event, frame.f_code.co_filename)
            self.capture_state(frame, frame.f_lineno)
        return self.trace_calls

    def explain_errors(self):
        print("\n\n\n\nExplaining errors...")
        error_message = ""
        for entry in self.execution_log:
            if "__runtime_error" in entry:
                print(entry["code_context"])
                error_message = entry["code_context"]
                # error_type = entry["error"]["type"]
                # error_message = entry["error"]["message"]
                # error_traceback = entry["error"]["traceback"]
                # error_message = f"Error Type: {error_type}\nError Message: {error_message}\nError Traceback: {error_traceback}"
                break
        if error_message == "":
            error_message = "No runtime errors found."
        print(error_message)
        self.error_explanation = (
            CLIENT.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": _PROMPT_TEMPLATE.format(stack_trace=error_message),
                    }
                ],
                model=GPT_MODEL,
            )
            .choices[0]
            .message.content
            if USE_GENERATIVE_MODEL
            else error_message
        )
        print(self.error_explanation)

    def run_script(self):
        # sys.settrace(self.trace_calls)
        # try:
        #     runpy.run_path(self.script_path, run_name="__main__")
        # except Exception:
        #     traceback.print_exc()
        # finally:
        #     sys.settrace(None)
        # sys.settrace(self.trace_calls)
        # try:
        #     runpy.run_path(self.script_path, run_name="__main__")
        # except Exception as e:
        #     # Capture the error and its traceback
        #     exc_type, exc_value, exc_traceback = sys.exc_info()
        #     for frame, lineno in traceback.walk_tb(exc_traceback):
        #         if frame.f_code.co_filename == self.script_path:
        #             self.capture_state(frame, lineno, error=exc_value)
        # finally:
        #     sys.settrace(None)
        # Redirect stdout and stderr
        sys.stdout = self.output_capture
        sys.stderr = self.error_capture

        sys.settrace(self.trace_calls)
        try:
            runpy.run_path(self.script_path, run_name="__main__")
        except Exception as e:
            # Capture the error and its traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            for frame, lineno in traceback.walk_tb(exc_traceback):
                if frame.f_code.co_filename == self.script_path:
                    self.capture_state(frame, lineno, error=exc_value)
        finally:
            sys.settrace(None)
            # Restore original stdout and stderr
            sys.stdout = self.original_stdout
            sys.stderr = self.original_stderr

    def get_log(self):
        return self.execution_log

    def save_log(self, output_path):
        # Save or print the log as needed
        with open(output_path, "w") as log_file:
            for idx, entry in enumerate(self.execution_log):
                log_file.write(
                    f"Call Step {idx + 1}: Line Number {entry['line_number']}: {entry['line_content']}\n"
                )
                log_file.write("Local Variables:\n")
                log_file.write(str(entry["local_variables"]))
                log_file.write("\n")
                log_file.write("Global Variables:\n")
                log_file.write(str(entry["global_variables"]))
                log_file.write("\n")
                log_file.write("Output:\n")
                log_file.write(entry.get("output", "No output") + "\n")
                log_file.write("Errors:\n")
                log_file.write(entry.get("errors", "No errors") + "\n")
                if "__runtime_error" in entry:
                    log_file.write(f"Error Type: {entry['error']['type']}\n")
                    log_file.write(f"Error Message: {entry['error']['message']}\n")
                    log_file.write(f"Traceback:\n{entry['error']['traceback']}\n")
                log_file.write("\n")

    def save_markdown(self, output_path):
        with open(output_path, "w") as log_file:
            for idx, entry in enumerate(self.execution_log):
                log_file.write(f"### Call Step {idx + 1}\n")
                log_file.write(f"**Line Number**: {entry['line_number']}\n")
                log_file.write(f"**Line Content**: `{entry['line_content']}`\n\n")
                # log_file.write("**Local Variables**:\n")
                # log_file.write(
                #     f"```json\n{json.dumps(entry.get('local_variables', {}), indent=2)}\n```\n\n"
                # # )
                # log_file.write("**Global Variables**:\n")
                # log_file.write(
                #     f"```json\n{json.dumps(entry.get('global_variables', {}), indent=2)}\n```\n\n"
                # )
                log_file.write("**Output**:\n")
                log_file.write(f"```\n{entry.get('output', 'No output')}\n```\n\n")
                log_file.write("**Errors**:\n")
                log_file.write(f"```\n{entry.get('errors', 'No errors')}\n```\n\n")
                if "error" in entry:
                    log_file.write(f"**Error Type**: {entry['error']['type']}\n")
                    log_file.write(f"**Error Message**: {entry['error']['message']}\n")
                    log_file.write(
                        f"**Traceback**:\n```\n{entry['error']['traceback']}\n```\n\n"
                    )
            log_file.write("\n")
            log_file.write(
                f"**Errors Explanation**:\n```\n{json.dumps(self.error_explanation, indent=2)}\n```\n\n"
            )

    def save_json(self, output_path):
        with open(output_path, "w") as log_file:
            json.dump(self.execution_log, log_file, indent=4, cls=CustomEncoder)


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # Convert objects to strings to avoid TypeError
        return str(obj)


def debug_script(script: str, output: str):
    try:
        # Example usage:
        debugger = Debugger(script)
        debugger.run_script()
        debugger.explain_errors()
        debugger.save_markdown(output)
        print(f"Debug log saved to {output}")
    except Exception as e:
        traceback.print_exc()
