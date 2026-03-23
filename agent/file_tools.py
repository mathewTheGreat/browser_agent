"""
File system tools for the browser agent.
Provides read, write, edit, and search capabilities for local files.
"""

import os
from typing import Optional
from agent.tools import tool


@tool
def read_file(file_path: str) -> str:
    """
    Read the contents of a file from the filesystem.
    
    Use this to read existing files before editing or to retrieve file contents.
    
    Parameters:
        file_path: Absolute path to the file (e.g., /path/to/file.txt or relative path from working directory)
    
    Returns: The contents of the file as a string
    """
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        if not os.path.isfile(file_path):
            return f"Error: Path is not a file: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return f"File: {file_path}\n{'=' * 50}\n{content}"
    
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Write content to a file, creating it if it doesn't exist or overwriting if it does.
    
    Use this to save results, reports, or any text data to files.
    
    Parameters:
        file_path: Absolute path to the file (e.g., /path/to/file.txt or relative path from working directory)
        content: The text content to write to the file
    
    Returns: Confirmation message with file path
    """
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Successfully wrote to: {file_path}\nContent length: {len(content)} characters"
    
    except Exception as e:
        return f"Error writing file: {str(e)}"


@tool
def edit_file(file_path: str, old_string: str, new_string: str) -> str:
    """
    Edit an existing file by replacing specific text.
    
    Use this to modify specific sections of a file without rewriting the entire file.
    
    Parameters:
        file_path: Absolute path to the file
        old_string: The exact text to find and replace (must match exactly)
        new_string: The replacement text
    
    Returns: Confirmation message or error
    """
    try:
        if not os.path.isabs(file_path):
            file_path = os.path.abspath(file_path)
        
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if old_string not in content:
            return f"Error: Could not find the specified text in the file.\nText to find: {old_string[:100]}..."
        
        new_content = content.replace(old_string, new_string, 1)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return f"Successfully edited: {file_path}"
    
    except Exception as e:
        return f"Error editing file: {str(e)}"


@tool
def list_directory(path: str = ".") -> str:
    """
    List the contents of a directory.
    
    Use this to see what files and folders exist in a directory.
    
    Parameters:
        path: Directory path to list (default: current directory)
    
    Returns: List of files and directories in the path
    """
    try:
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        
        if not os.path.exists(path):
            return f"Error: Directory not found: {path}"
        
        if not os.path.isdir(path):
            return f"Error: Path is not a directory: {path}"
        
        entries = os.listdir(path)
        
        if not entries:
            return f"Directory is empty: {path}"
        
        result = [f"Contents of: {path}", "=" * 50]
        for entry in sorted(entries):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                result.append(f"[DIR]  {entry}/")
            else:
                size = os.path.getsize(full_path)
                result.append(f"[FILE] {entry} ({size} bytes)")
        
        return "\n".join(result)
    
    except Exception as e:
        return f"Error listing directory: {str(e)}"


@tool
def search_files(pattern: str, path: str = ".") -> str:
    """
    Search for files matching a pattern in directory names.
    
    Use glob patterns like *.txt, *.py, test_*.py, etc.
    
    Parameters:
        pattern: Glob pattern to match (e.g., "*.txt", "*.py", "**/*.md")
        path: Directory to search in (default: current directory)
    
    Returns: List of matching file paths
    """
    try:
        import glob
        
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        
        search_pattern = os.path.join(path, "**", pattern)
        matches = glob.glob(search_pattern, recursive=True)
        
        if not matches:
            return f"No files matching pattern '{pattern}' found in {path}"
        
        result = [f"Files matching '{pattern}' in {path}", "=" * 50]
        for match in sorted(matches):
            if os.path.isfile(match):
                result.append(match)
        
        return "\n".join(result) if len(result) > 1 else f"No files matching '{pattern}' found"
    
    except Exception as e:
        return f"Error searching files: {str(e)}"


@tool
def grep_files(pattern: str, path: str = ".", file_pattern: str = "*") -> str:
    """
    Search for text content within files.
    
    Parameters:
        pattern: Text pattern to search for
        path: Directory to search in (default: current directory)
        file_pattern: Only search files matching this pattern (default: *)
    
    Returns: Lines containing the pattern with file names and line numbers
    """
    try:
        import glob
        
        if not os.path.isabs(path):
            path = os.path.abspath(path)
        
        matches = []
        search_pattern = os.path.join(path, "**", file_pattern)
        
        for file_path in glob.glob(search_pattern, recursive=True):
            if not os.path.isfile(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if pattern.lower() in line.lower():
                            matches.append(f"{file_path}:{line_num}: {line.rstrip()}")
            except (UnicodeDecodeError, PermissionError):
                continue
        
        if not matches:
            return f"No matches found for '{pattern}'"
        
        return f"Found {len(matches)} matches for '{pattern}':\n" + "=" * 50 + "\n" + "\n".join(matches[:50])
    
    except Exception as e:
        return f"Error searching files: {str(e)}"


@tool
def bash(command: str) -> str:
    """
    Execute a bash/shell command and return the output.
    
    Use this for running shell commands, scripts, or system operations.
    
    Parameters:
        command: The shell command to execute
    
    Returns: Command output or error message
    """
    try:
        import subprocess
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = []
        if result.stdout:
            output.append("STDOUT:")
            output.append(result.stdout)
        if result.stderr:
            output.append("STDERR:")
            output.append(result.stderr)
        output.append(f"Exit code: {result.returncode}")
        
        return "\n".join(output)
    
    except subprocess.TimeoutExpired:
        return "Error: Command timed out after 30 seconds"
    except Exception as e:
        return f"Error executing command: {str(e)}"


def get_file_tools():
    """Get all file system tools for agent use."""
    return [
        read_file,
        write_file,
        edit_file,
        list_directory,
        search_files,
        grep_files,
        bash
    ]
