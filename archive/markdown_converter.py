import os
import re

def convert_markdown_file(file_path):
    """
    Convert markdown file header formats while preserving Python code blocks.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split content into parts: normal markdown and code blocks
    parts = []
    current_pos = 0
    
    # Find all Python code blocks
    code_block_pattern = re.compile(r'```python.*?```', re.DOTALL)
    for match in code_block_pattern.finditer(content):
        # Add text before code block
        if match.start() > current_pos:
            parts.append(('markdown', content[current_pos:match.start()]))
        
        # Add code block (don't modify it)
        parts.append(('code', match.group(0)))
        current_pos = match.end()
    
    # Add any remaining text
    if current_pos < len(content):
        parts.append(('markdown', content[current_pos:]))
    
    # Modify only the markdown parts
    modified_parts = []
    for part_type, part_content in parts:
        if part_type == 'markdown':
            # Convert ## Project Title to # Project Title
            part_content = re.sub(r'^## (.*?)$', r'# \1', part_content, flags=re.MULTILINE)
            
            # Convert ### Section to ## Section
            part_content = re.sub(r'^### (.*?)$', r'## \1', part_content, flags=re.MULTILINE)
        
        modified_parts.append(part_content)
    
    # Join all parts back together
    modified_content = ''.join(modified_parts)
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

def convert_folder(folder_path):
    """
    Convert all markdown files in the given folder.
    """
    count = 0
    for filename in os.listdir(folder_path):
        if filename.endswith('.md'):
            file_path = os.path.join(folder_path, filename)
            convert_markdown_file(file_path)
            count += 1
            print(f"Converted: {filename}")
    
    print(f"\nCompleted! Converted {count} markdown files.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = input("Enter the folder path containing markdown files: ")
    
    if os.path.isdir(folder_path):
        convert_folder(folder_path)
    else:
        print(f"Error: '{folder_path}' is not a valid directory.")