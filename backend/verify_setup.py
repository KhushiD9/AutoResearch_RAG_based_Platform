"""
Setup verification script for Research Paper Assistant backend
Run this to verify all dependencies are installed correctly
"""

import sys
from typing import List, Tuple

def check_imports() -> List[Tuple[str, bool, str]]:
    """Check if all required packages can be imported"""
    results = []
    
    packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pydantic", "Pydantic"),
        ("httpx", "HTTPX"),
        ("PyPDF2", "PyPDF2"),
        ("pdfplumber", "pdfplumber"),
        ("chromadb", "ChromaDB"),
        ("google.generativeai", "Google Gemini"),
        ("openai", "OpenAI"),
        ("arxiv", "arXiv"),
        ("requests", "Requests"),
        ("sqlalchemy", "SQLAlchemy"),
    ]
    
    for module_name, display_name in packages:
        try:
            __import__(module_name)
            results.append((display_name, True, "OK"))
        except ImportError as e:
            results.append((display_name, False, str(e)))
    
    return results

def check_env_file() -> bool:
    """Check if .env file exists"""
    import os
    return os.path.exists('.env')

def main():
    print("=" * 60)
    print("Research Paper Assistant - Setup Verification")
    print("=" * 60)
    print()
    
    # Check Python version
    print("1. Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro} (OK)")
    else:
        print(f"   ✗ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False
    print()
    
    # Check packages
    print("2. Checking required packages...")
    results = check_imports()
    all_ok = True
    
    for name, success, message in results:
        if success:
            print(f"   ✓ {name}")
        else:
            print(f"   ✗ {name}: {message}")
            all_ok = False
    print()
    
    # Check .env file
    print("3. Checking configuration...")
    if check_env_file():
        print("   ✓ .env file exists")
        
        # Try to load and check API keys
        try:
            from config import settings
            if settings.GEMINI_API_KEY:
                print("   ✓ GEMINI_API_KEY configured")
            else:
                print("   ⚠ GEMINI_API_KEY not set (required)")
                all_ok = False
                
            if settings.OPENAI_API_KEY:
                print("   ✓ OPENAI_API_KEY configured")
            else:
                print("   ⚠ OPENAI_API_KEY not set (optional)")
        except Exception as e:
            print(f"   ✗ Error loading config: {e}")
            all_ok = False
    else:
        print("   ✗ .env file not found")
        print("     Create .env file from .env.example")
        all_ok = False
    print()
    
    # Summary
    print("=" * 60)
    if all_ok:
        print("✓ Setup verification passed!")
        print()
        print("You can now start the server:")
        print("  python main.py")
    else:
        print("✗ Setup verification failed")
        print()
        print("Please fix the issues above and try again.")
        print()
        print("To install missing packages:")
        print("  pip install -r requirements.txt")
        print()
        print("To create .env file:")
        print("  copy .env.example .env")
        print("  Then edit .env and add your API keys")
    print("=" * 60)
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
