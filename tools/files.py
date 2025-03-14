import os, re, fnmatch, json, shutil, glob, subprocess, requests
from typing import List, Dict, Any, Optional, Literal, Union, Tuple
from langchain_core.tools import BaseTool, tool
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from agents import Agent, FunctionTool, RunContextWrapper, function_tool

from utils import _apply_diff

@function_tool
def read_file(file_path: str, pattern: str = "*") -> str:
    """
    Read text content from a file that matches a pattern.

    Args:
        file_path: Path to the file to read.
        pattern: Pattern to match within the file. Can be a regex pattern or a glob pattern.
            Use "*" to match the entire file (default).

    Returns:
        The matched content of the file as a string.
    """
    # Maximum size in characters before warning (assuming ~4 chars per token)
    if not os.path.exists(file_path):
        raise Exception(f"Error: File {file_path} does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        # If pattern is "*", return the entire file (with size check)
        if pattern == "*":
            if len(content) > os.environ.get("MAX_FILE_TOKENS"):
                raise Exception(f"Matched content too large for context window")
            return content

        # Otherwise, search for pattern matches
        matched_content = ""

        # Try as regex pattern first
        try:
            regex = re.compile(pattern, re.MULTILINE | re.DOTALL)
            matches = regex.findall(content)
            if matches:
                matched_content = "\n".join(matches)
            else:
                # If no regex matches, try as glob-style pattern (line by line)
                lines = content.splitlines()
                matched_lines = [line for line in lines if fnmatch.fnmatch(line, pattern)]
                matched_content = "\n".join(matched_lines)
        except re.error:
            # If regex fails, default to glob-style pattern matching
            lines = content.splitlines()
            matched_lines = [line for line in lines if fnmatch.fnmatch(line, pattern)]
            matched_content = "\n".join(matched_lines)

        # Check if matched content might be too large
        if len(matched_content) > os.environ.get("MAX_FILE_TOKENS"):
            raise Exception(f"Matched content too large for context window")

        if not matched_content:
            raise Exception(f"No content in {file_path} matches the pattern '{pattern}'.")

        return matched_content

@function_tool
def write_file(file_path: str, content: str) -> None:
    """
    Write content to a file. If the content is a git diff, it will be parsed and applied.

    Args:
        file_path: Path to the file to write.
        content: Content to write to the file or a git diff to apply.
    """
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    # Check if content is a git diff
    if (content.startswith('diff --git') or
        content.startswith('---') or
        content.startswith('+++') or
        re.match(r'^@@ -\d+,\d+ \+\d+,\d+ @@', content)):

        return _apply_diff(file_path, content)
    else:
        # Normal file write
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    
@function_tool
def ensure_directory(directory_path: str) -> None:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory.
    """
    os.makedirs(directory_path, exist_ok=True)
    
@function_tool
def copy_file(source_path: str, destination_path: str) -> None:
    """
    Copy a file from source to destination.

    Args:
        source_path: Path to the source file.
        destination_path: Path to the destination file.
    """
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(destination_path)), exist_ok=True)

    shutil.copy2(source_path, destination_path)
    return f"File copied from {source_path} to {destination_path}"
    
@function_tool
def delete_file(file_path: str, force: bool = False) -> None:
    """
    Delete a file from disk.

    Args:
        file_path: Path to the file to delete.
        force: Set to True to bypass safety checks.
    """
    if not force and not is_safe_path(file_path):
        raise Exception("The requested path is outside the top-level directory of our application, and is thus, off limits.")

    if os.path.exists(file_path):
        os.remove(file_path)
        return f"File {file_path} has been deleted"
    else:
        return f"File {file_path} does not exist"
    
@function_tool
def list_files(directory_path: str, pattern: str = "*") -> List[str]:
    """
    List all files in a directory matching a pattern.

    Args:
        directory_path: Path to the directory.
        pattern: Glob pattern to match files.

    Returns:
        A list of file paths.
    """
    if not os.path.exists(directory_path):
        return [f"Directory {directory_path} does not exist"]

    file_paths = []
    for file_path in glob.glob(os.path.join(directory_path, pattern)):
        if os.path.isfile(file_path):
            file_paths.append(file_path)

    return file_paths
    
@function_tool
def list_directories(directory_path: str, pattern: str = "*") -> List[str]:
    """
    List all directories in a directory matching a pattern.

    Args:
        directory_path: Path to the directory.
        pattern: Glob pattern to match directories.

    Returns:
        A list of directory paths.
    """
    if not os.path.exists(directory_path):
        return [f"Directory {directory_path} does not exist"]

    dir_paths = []
    for dir_path in glob.glob(os.path.join(directory_path, pattern)):
        if os.path.isdir(dir_path):
            dir_paths.append(dir_path)

    return dir_paths