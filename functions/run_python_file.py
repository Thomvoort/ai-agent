import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not is_valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(target_file_path) or not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]
        if args is not None:
            command.extend(args)
        
        completed_process = subprocess.run(args=command, capture_output=True, text=True, timeout=30.0)
        output = []
        if completed_process.returncode != 0:
            output.append(f"Process exited with code {completed_process.returncode}")
        if not completed_process.stdout and not completed_process.stderr:
            output.append("No output produced")
        if completed_process.stdout:
            output.append(f"STDOUT: {completed_process.stdout}")
        if completed_process.stderr:
            output.append(f"STDERR: {completed_process.stderr}")
            
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file as a subprocess. Returns stdout and stderr, or if neither have content, gives a 'No output produced' message. Requires file with .py extension, and optional args.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of python file in a specified directory relative to the working directory, including the file extension .py"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="List of arguments with which to run the python file. Default is None, any provided args are added to the subprocess command."
            )
        },
        required=["file_path"]
    )
)