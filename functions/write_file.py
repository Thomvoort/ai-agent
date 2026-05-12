import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        is_valid_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        
        if not is_valid_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
            
        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
        
        with open(target_file_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="When provided with a file path relative to the working directory, write the contents to the specified file. Any required dirs are created if they do not exists.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to working directory. Provided file path cannot be an existing directoy. Will create dirs and file if path doesn't exists, and will overwrite existing files if they do."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file. Will override existing content."
            )
        },
        required=["file_path", "content"]
    )
)