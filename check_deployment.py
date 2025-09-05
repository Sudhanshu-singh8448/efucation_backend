#!/usr/bin/env python3
"""
Pre-deployment verification script
Checks if the project is ready for Render deployment
"""

import os
import sys
import json
from pathlib import Path

def check_file_exists(file_path, required=True):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {file_path} exists")
        return True
    else:
        status = "❌" if required else "⚠️"
        print(f"{status} {file_path} {'missing (required)' if required else 'missing (optional)'}")
        return not required

def check_gitignore():
    """Check .gitignore file"""
    if not os.path.exists('.gitignore'):
        print("❌ .gitignore file missing")
        return False
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    # Check for essential patterns (more flexible matching)
    patterns_to_check = [
        ('venv', ['venv/', 'venv', '.venv']),
        ('__pycache__', ['__pycache__/', '__pycache__']),
        ('*.pyc', ['*.pyc', '*.py[cod]']),
        ('.env', ['.env']),
        ('*.log', ['*.log'])
    ]
    
    missing_patterns = []
    
    for pattern_name, pattern_variants in patterns_to_check:
        found = any(variant in content for variant in pattern_variants)
        if not found:
            missing_patterns.append(pattern_name)
    
    if missing_patterns:
        print(f"⚠️ .gitignore missing patterns: {', '.join(missing_patterns)}")
        return False
    else:
        print("✅ .gitignore properly configured")
        return True

def check_requirements():
    """Check requirements.txt for duplicates"""
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt missing")
        return False
    
    with open('requirements.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith('#')]
    
    packages = []
    for line in lines:
        if '==' in line or '>=' in line:
            package_name = line.split('==')[0].split('>=')[0].strip()
            packages.append(package_name)
    
    duplicates = [pkg for pkg in set(packages) if packages.count(pkg) > 1]
    
    if duplicates:
        print(f"⚠️ Duplicate packages in requirements.txt: {', '.join(duplicates)}")
        return False
    else:
        print("✅ requirements.txt properly configured")
        return True

def check_environment_variables():
    """Check if required environment variables are configured"""
    required_vars = ['MONGODB_URI']
    missing_vars = []
    
    # Check render.yaml for environment variables
    if os.path.exists('render.yaml'):
        print("✅ render.yaml exists")
        with open('render.yaml', 'r') as f:
            content = f.read()
        
        for var in required_vars:
            if var not in content:
                missing_vars.append(var)
    else:
        print("❌ render.yaml missing")
        return False
    
    if missing_vars:
        print(f"⚠️ Missing environment variables in render.yaml: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Environment variables properly configured")
        return True

def check_project_structure():
    """Check if project structure is correct"""
    required_files = [
        'app.py',
        'database.py',
        'gunicorn_config.py',
        'requirements.txt',
        'render.yaml'
    ]
    
    required_dirs = [
        'services',
        'data'
    ]
    
    all_good = True
    
    for file in required_files:
        if not check_file_exists(file):
            all_good = False
    
    for dir in required_dirs:
        if not check_file_exists(dir):
            all_good = False
    
    # Check services __init__.py
    if not check_file_exists('services/__init__.py'):
        all_good = False
    
    return all_good

def check_unwanted_files():
    """Check for files that shouldn't be in the repository"""
    unwanted_patterns = ['venv', '__pycache__', '*.pyc', '*.log']
    unwanted_found = []
    
    for root, dirs, files in os.walk('.'):
        # Skip .git directory
        if '.git' in root:
            continue
            
        for pattern in unwanted_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                pattern_name = pattern[:-1]
                if pattern_name in dirs:
                    unwanted_found.append(f"{root}/{pattern_name}/")
            else:
                # File pattern
                if pattern.startswith('*.'):
                    extension = pattern[2:]
                    matching_files = [f for f in files if f.endswith(f'.{extension}')]
                    for file in matching_files:
                        unwanted_found.append(f"{root}/{file}")
                else:
                    if pattern in files:
                        unwanted_found.append(f"{root}/{pattern}")
    
    if unwanted_found:
        print("⚠️ Unwanted files/directories found:")
        for item in unwanted_found[:10]:  # Show first 10
            print(f"   {item}")
        if len(unwanted_found) > 10:
            print(f"   ... and {len(unwanted_found) - 10} more")
        return False
    else:
        print("✅ No unwanted files found")
        return True

def main():
    """Main verification function"""
    print("🔍 Checking project for Render deployment readiness...\n")
    
    checks = [
        ("Project Structure", check_project_structure),
        ("Requirements.txt", check_requirements),
        (".gitignore", check_gitignore),
        ("Environment Variables", check_environment_variables),
        ("Unwanted Files", check_unwanted_files)
    ]
    
    all_passed = True
    
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}:")
        if not check_func():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 Project is ready for Render deployment!")
        return 0
    else:
        print("❌ Project has issues that need to be fixed before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())
