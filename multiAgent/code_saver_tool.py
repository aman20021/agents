import os
import json
from typing import Dict, Any
from google.adk.tools import FunctionTool

def save_code_to_file(filename: str, content: str, directory: str = "generated_code") -> Dict[str, Any]:
    """
    Save code content to a file.
    
    Args:
        filename: Name of the file to save
        content: File content (raw code without markdown)
        directory: Directory to save the file in
        
    Returns:
        Dict with success status and file path
    """
    try:
        # Clean up content - remove any markdown code blocks
        content = clean_content(content)
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Create full file path
        filepath = os.path.join(directory, filename)
        
        # Write the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "filepath": filepath,
            "message": f"Successfully saved {filename}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to save {filename}: {str(e)}"
        }

def clean_content(content: str) -> str:
    """Remove markdown code block markers from content."""
    import re
    
    # Remove opening code block markers
    content = re.sub(r'^```[a-zA-Z]*\s*\n?', '', content, flags=re.MULTILINE)
    # Remove closing code block markers
    content = re.sub(r'\n?```\s*$', '', content)
    
    return content.strip()

def save_multiple_files(files: list) -> Dict[str, Any]:
    """
    Save multiple files.
    
    Args:
        files: List of file dictionaries with filename, content, and optional directory
        
    Returns:
        Dict with overall success status and individual file results
    """
    results = []
    success_count = 0
    
    for file_info in files:
        filename = file_info.get('filename', 'temp.py')
        content = file_info.get('content', '')
        directory = file_info.get('directory', 'generated_code')
        
        result = save_code_to_file(filename, content, directory)
        results.append(result)
        
        if result['success']:
            success_count += 1
    
    return {
        "success": success_count == len(files),
        "total_files": len(files),
        "successful_saves": success_count,
        "message": f"Saved {success_count}/{len(files)} files successfully"
    }

# Create the tools
code_saver_tool = FunctionTool(func=save_code_to_file)
multi_file_saver_tool = FunctionTool(func=save_multiple_files)

# For backward compatibility
CodeSaverTool = lambda: code_saver_tool
MultiFileSaverTool = lambda: multi_file_saver_tool
