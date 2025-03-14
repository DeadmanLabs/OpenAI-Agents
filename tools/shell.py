import os, re, fnmatch, json, shutil, glob, subprocess, requests
from typing import List, Dict, Any, Optional, Literal, Union, Tuple
from langchain_core.tools import BaseTool, tool
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from agents import Agent, FunctionTool, RunContextWrapper, function_tool

@function_tool
def shell_executor(command: str, dangerous_patterns: Optional[List[str]] = None) -> str:
    """
    Execute a shell command and return its output.

    Args:
        command: The shell command to execute.
        dangerous_patterns: Optional list of patterns to check for dangerous commands.

    Returns:
        The command output or a request for permission if the command is potentially dangerous.
    """
    # Default dangerous patterns if none provided
    if dangerous_patterns is None:
        dangerous_patterns = [
            r"rm\s+(-rf?|--recursive)\s+/",  # Dangerous rm commands
            r"dd\s+.*of=/dev/",              # Writing to device files
            r">\s*/etc/",                    # Writing to system configs
            r"chmod\s+.*777",                # Overly permissive chmod
            r"mkfs",                         # Formatting drives
            r"mv\s+.*(/etc|/usr|/bin|/sbin|/lib|/boot|/dev|/proc)",  # Moving system files
            r"wget.*(sh|bash|zsh)\s+-\s*\|.*(sh|bash|zsh)",  # Piping downloaded content to shell
            r"curl.*(sh|bash|zsh)\s+-\s*\|.*(sh|bash|zsh)",   # Piping downloaded content to shell

            r"rmdir\s+/s\s+/q\s+[A-Z]:\\Windows",  # Deleting Windows directory
            r"del\s+/[fqs].*[A-Z]:\\Windows",      # Deleting Windows files
            r"format\s+[A-Z]:",                    # Formatting drives
            r"rd\s+/s\s+/q\s+[A-Z]:\\Windows",     # Recursive directory deletion of Windows
            r"del\s+/[fqs].*system32",             # Deleting system32 files
            r"move\s+.*\\Windows\\",               # Moving Windows files
            r"reg\s+delete\s+HKLM",                # Deleting registry keys
            r"reg\s+delete\s+HKCU",                # Deleting registry keys
            r"powershell\s+.*-ExecutionPolicy\s+Bypass",  # Bypassing PowerShell execution policy
            r"powershell\s+.*Invoke-Expression.*Net.WebClient",  # PowerShell download and execute
            r"powershell\s+.*IEX.*Net.WebClient",   # PowerShell download and execute (shorthand)
            r"bitsadmin\s+/transfer.*powershell",   # Download and execute via bitsadmin
            r"certutil\s+-urlcache\s+-split\s+-f",  # Download files with certutil
            r"wmic\s+product\s+where.*call\s+uninstall",  # Mass uninstallation of software
            r"net\s+user\s+.*\s+/add",              # Adding users
            r"net\s+localgroup\s+administrators\s+.*\s+/add",  # Adding to admin group
            r"bcdedit\s+/set\s+.*\s+0",             # Modifying boot configuration
            r"schtasks\s+/create.*cmd",             # Creating scheduled tasks with cmd
        ]

    # Check for potentially dangerous commands
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            raise Exception(f"The command '{command}' appears to be potentially dangerous.")

    # Execute the command and capture output
    process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True,
            text=True
    )
    stdout, stderr = process.communicate()

    # Prepare the result
    result = f"Exit code: {process.returncode}\n"

    if stdout:
        result += f"\nSTDOUT:\n{stdout}"

    if stderr:
        result += f"\nSTDERR:\n{stderr}"

    return result
    
@function_tool
def safe_shell_execute(command: str, args: List[str]) -> str:
    """
    Execute a shell command with arguments in a safer way by separating the command from its arguments.

    Args:
        command: The shell command to execute.
        args: List of arguments to pass to the command.

    Returns:
        The command output.
    """
    # Default dangerous patterns if none provided
    if dangerous_patterns is None:
        dangerous_patterns = [
            r"rm\s+(-rf?|--recursive)\s+/",  # Dangerous rm commands
            r"dd\s+.*of=/dev/",              # Writing to device files
            r">\s*/etc/",                    # Writing to system configs
            r"chmod\s+.*777",                # Overly permissive chmod
            r"mkfs",                         # Formatting drives
            r"mv\s+.*(/etc|/usr|/bin|/sbin|/lib|/boot|/dev|/proc)",  # Moving system files
            r"wget.*(sh|bash|zsh)\s+-\s*\|.*(sh|bash|zsh)",  # Piping downloaded content to shell
            r"curl.*(sh|bash|zsh)\s+-\s*\|.*(sh|bash|zsh)",   # Piping downloaded content to shell

            r"rmdir\s+/s\s+/q\s+[A-Z]:\\Windows",  # Deleting Windows directory
            r"del\s+/[fqs].*[A-Z]:\\Windows",      # Deleting Windows files
            r"format\s+[A-Z]:",                    # Formatting drives
            r"rd\s+/s\s+/q\s+[A-Z]:\\Windows",     # Recursive directory deletion of Windows
            r"del\s+/[fqs].*system32",             # Deleting system32 files
            r"move\s+.*\\Windows\\",               # Moving Windows files
            r"reg\s+delete\s+HKLM",                # Deleting registry keys
            r"reg\s+delete\s+HKCU",                # Deleting registry keys
            r"powershell\s+.*-ExecutionPolicy\s+Bypass",  # Bypassing PowerShell execution policy
            r"powershell\s+.*Invoke-Expression.*Net.WebClient",  # PowerShell download and execute
            r"powershell\s+.*IEX.*Net.WebClient",   # PowerShell download and execute (shorthand)
            r"bitsadmin\s+/transfer.*powershell",   # Download and execute via bitsadmin
            r"certutil\s+-urlcache\s+-split\s+-f",  # Download files with certutil
            r"wmic\s+product\s+where.*call\s+uninstall",  # Mass uninstallation of software
            r"net\s+user\s+.*\s+/add",              # Adding users
            r"net\s+localgroup\s+administrators\s+.*\s+/add",  # Adding to admin group
            r"bcdedit\s+/set\s+.*\s+0",             # Modifying boot configuration
            r"schtasks\s+/create.*cmd",             # Creating scheduled tasks with cmd
        ]

    # Check for potentially dangerous commands
    for pattern in dangerous_patterns:
        if re.search(pattern, command):
            raise Exception(f"The command '{command}' appears to be potentially dangerous.")

    # Execute the command with arguments provided as a list (safer)
    process = subprocess.Popen(
        [command] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()

    # Prepare the result
    result = f"Exit code: {process.returncode}\n"

    if stdout:
        result += f"\nSTDOUT:\n{stdout}"

    if stderr:
        result += f"\nSTDERR:\n{stderr}"

    return result