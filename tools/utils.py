import os, subprocess, re, tempfile
from typing import List, Dict, Any, Optional, Literal, Union, Tuple

def is_safe_path(path: str, base_dir: Optional[str] = None) -> bool:
    """Check if a path is within a safe directory."""
    if base_dir is None:
        base_dir = os.getcwd()

    # Convert to absolute paths
    path = os.path.abspath(path)
    base_dir = os.path.abspath(base_dir)

    # Check if the path is within the base directory
    return path.startswith(base_dir)

def _apply_diff(file_path: str, diff_content: str) -> str:
    """
    Parse and apply a git diff to a file.

    Args:
        file_path: Path to the file to modify.
        diff_content: The git diff content to apply.

    Returns:
        A confirmation message.
    """
    # Check if file exists
    if not os.path.exists(file_path) and not diff_content.startswith('diff --git'):
        # Create empty file if it doesn't exist and we're applying a pure patch
        with open(file_path, 'w', encoding='utf-8') as f:
            pass

    # Try to apply the diff using the git patch command if git is available
    if _is_git_available():
        return _apply_diff_using_git(file_path, diff_content)
    else:
        # Fall back to our custom diff parser if git is not available
        return _apply_diff_manually(file_path, diff_content)

def _is_git_available() -> bool:
    """Check if git is available on the system."""
    try:
        subprocess.run(['git', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def _apply_diff_using_git(file_path: str, diff_content: str) -> str:
    """Apply a diff using git apply."""
    try:
        # Write the diff to a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as temp_file:
            temp_file_path = temp_file.name
            temp_file.write(diff_content)

        try:
            # Try to apply the patch using git
            result = subprocess.run(
                ['git', 'apply', '--ignore-whitespace', '--verbose', temp_file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return f"Git diff applied to {file_path} successfully using git apply"
        except subprocess.CalledProcessError as e:
            # If git apply fails, try our manual approach
            return _apply_diff_manually(file_path, diff_content)
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
    except Exception as e:
        return f"Error applying git diff with git apply: {str(e)}"

def _apply_diff_manually(file_path: str, diff_content: str) -> str:
    """
    Manually parse and apply a diff without relying on git.
    Supports unified diff format.
    """
    try:
        # Read the current file content if it exists
        current_content = ""
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                current_content = file.read()

        # Split the file content into lines
        current_lines = current_content.splitlines()

        # Parse the diff
        new_lines = _parse_unified_diff(current_lines, diff_content)

        # Write the new content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(new_lines))
            # Add a newline at the end if the original had one
            if current_content and current_content.endswith('\n'):
                file.write('\n')

        return f"Git diff applied to {file_path} successfully using manual diff parser"
    except Exception as e:
        return f"Error applying git diff manually: {str(e)}"

def _parse_unified_diff(current_lines: list, diff_content: str) -> list:
    """
    Parse a unified diff and apply it to the current lines.

    Args:
        current_lines: List of current file lines.
        diff_content: The unified diff content.

    Returns:
        List of new file lines after applying the diff.
    """
    # Copy the current lines to avoid modifying the original
    new_lines = current_lines.copy()

    # Parse the diff to extract hunks
    hunks = _extract_hunks(diff_content)

    # Apply each hunk in reverse order to avoid line number changes
    for hunk in reversed(hunks):
        start_line, removed_count, added_lines = hunk

        # Adjust for 0-based indexing
        start_idx = start_line - 1

        # Remove the specified lines
        if removed_count > 0:
            new_lines[start_idx:start_idx + removed_count] = []

        # Add the new lines
        for i, line in enumerate(added_lines):
            new_lines.insert(start_idx + i, line)

    return new_lines

def _extract_hunks(diff_content: str) -> list:
    """
    Extract hunks from a unified diff.

    Args:
        diff_content: The unified diff content.

    Returns:
        List of hunks. Each hunk is a tuple (start_line, removed_count, added_lines).
    """
    hunks = []
    current_hunk = None
    added_lines = []

    # Skip the header lines
    in_header = True
    lines = diff_content.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for hunk header
        if re.match(r'^@@ -(\d+),(\d+) \+(\d+),(\d+) @@', line):
            in_header = False

            # Save the previous hunk if exists
            if current_hunk is not None:
                hunks.append((current_hunk[0], current_hunk[1], added_lines))
                added_lines = []

            # Parse the hunk header
            match = re.match(r'^@@ -(\d+),(\d+) \+(\d+),(\d+) @@', line)
            old_start = int(match.group(1))
            old_count = int(match.group(2))
            new_start = int(match.group(3))

            current_hunk = (new_start, old_count, [])

        # Skip header lines
        elif in_header:
            pass

        # Process context and added lines
        elif line.startswith('+'):
            added_lines.append(line[1:])  # Remove the '+' prefix

        # Skip removed lines (starting with '-')
        elif line.startswith('-'):
            pass

        # Process context lines
        elif line.startswith(' '):
            added_lines.append(line[1:])  # Remove the ' ' prefix

        i += 1

    # Add the last hunk
    if current_hunk is not None:
        hunks.append((current_hunk[0], current_hunk[1], added_lines))

    return hunks