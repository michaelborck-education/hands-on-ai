# check_imports.py - Check for old package imports and suggest replacements

import re
import os
from pathlib import Path
import argparse

OLD_IMPORT_PATTERNS = [
    r'^from\s+chatcraft',  # From imports
    r'^import\s+chatcraft',  # Direct imports
    r'chatcraft\.'  # Usage in code
]

REPLACEMENT = 'ailabkit'

def check_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            content = f.read()
        except UnicodeDecodeError:
            print(f"⚠️ Skipping {file_path} - Encoding issues")
            return False, []
    
    issues = []
    has_issues = False
    
    for i, line in enumerate(content.splitlines()):
        for pattern in OLD_IMPORT_PATTERNS:
            if re.search(pattern, line):
                # Replace chatcraft with ailabkit
                fixed_line = re.sub(r'chatcraft', REPLACEMENT, line)
                issues.append((i + 1, line, fixed_line))
                has_issues = True
    
    return has_issues, issues

def check_directory(directory, extensions=None, show_all=False):
    if extensions is None:
        extensions = ['.py', '.md', '.html', '.txt']
    
    all_issues = {}
    files_with_issues = 0
    total_issues = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            # Skip virtual environments and other special directories
            if any(part for part in Path(root).parts if part.startswith('.')):
                continue
                
            if any(file.endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                has_issues, issues = check_file(file_path)
                
                if has_issues:
                    all_issues[file_path] = issues
                    files_with_issues += 1
                    total_issues += len(issues)
                elif show_all:
                    print(f"✅ {file_path}")
    
    return files_with_issues, total_issues, all_issues

def report_issues(issues_dict, fix=False):
    for file_path, issues in issues_dict.items():
        print(f"\n🔍 {file_path}: {len(issues)} issue(s)")
        
        if fix:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                for _, old_line, new_line in issues:
                    content = content.replace(old_line, new_line)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"  ✅ Fixed {len(issues)} issue(s)")
            except Exception as e:
                print(f"  ❌ Error fixing file: {e}")
        else:
            for line_num, old_line, new_line in issues:
                print(f"  • Line {line_num}: {old_line.strip()}")
                print(f"    Should be: {new_line.strip()}")

def main():
    parser = argparse.ArgumentParser(description="Check for old 'chatcraft' imports and usages")
    parser.add_argument("--directory", "-d", type=str, default=".", 
                       help="Directory to check recursively (default: current directory)")
    parser.add_argument("--fix", action="store_true", 
                       help="Fix issues by replacing chatcraft with ailabkit")
    parser.add_argument("--all", action="store_true", 
                       help="Show all files, even those without issues")
    parser.add_argument("--extensions", "-e", type=str, default=".py,.md,.html,.txt",
                       help="Comma-separated list of file extensions to check (default: .py,.md,.html,.txt)")
    
    args = parser.parse_args()
    extensions = args.extensions.split(",")
    
    print(f"🔍 Checking for 'chatcraft' usage in {args.directory}")
    print(f"📄 Checking files with extensions: {', '.join(extensions)}")
    
    files_with_issues, total_issues, all_issues = check_directory(
        args.directory, extensions, args.all
    )
    
    if total_issues > 0:
        print(f"\n⚠️ Found {total_issues} issue(s) in {files_with_issues} file(s)")
        report_issues(all_issues, args.fix)
        
        if args.fix:
            print(f"\n✅ Fixed {total_issues} issue(s) in {files_with_issues} file(s)")
        else:
            print("\nTo automatically fix these issues, run with the --fix flag")
    else:
        print("\n✅ No issues found!")

if __name__ == "__main__":
    main()