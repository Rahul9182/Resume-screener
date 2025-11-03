"""
Installation and Setup Verification Script
Run this to check if everything is installed correctly

Usage: python test_installation.py
"""

import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("✅ Python version is compatible (3.8+)")
        return True
    else:
        print("❌ Python version is too old. Please upgrade to 3.8+")
        return False

def check_packages():
    """Check if all required packages are installed"""
    print_header("Package Installation Check")
    
    packages = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'openpyxl': 'OpenPyXL',
        'PyPDF2': 'PyPDF2',
        'pdfplumber': 'PDFPlumber',
        'docx': 'python-docx',
        'openai': 'OpenAI',
        'langchain': 'LangChain',
        'pydantic': 'Pydantic',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    
    for package, name in packages.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {name:20} - version {version}")
        except ImportError:
            print(f"❌ {name:20} - NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_spacy_model():
    """Check if spaCy model is downloaded"""
    print_header("spaCy Model Check")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("✅ spaCy model 'en_core_web_sm' is installed")
        
        # Test the model
        doc = nlp("John Doe works at Google")
        entities = [(ent.text, ent.label_) for ent in doc.ents]
        if entities:
            print(f"✅ Model is working correctly")
            print(f"   Test extraction: {entities}")
        return True
    except OSError:
        print("❌ spaCy model 'en_core_web_sm' is NOT installed")
        print("   Run: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        print(f"❌ Error loading spaCy model: {str(e)}")
        return False

def check_directory_structure():
    """Check if directory structure is correct"""
    print_header("Directory Structure Check")
    
    required_dirs = [
        'parsers',
        'extractors',
        'storage',
        'utils'
    ]
    
    optional_dirs = ['uploads', 'output']
    
    all_present = True
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/ exists")
            
            # Check for __init__.py
            init_file = Path(directory) / '__init__.py'
            if init_file.exists():
                print(f"   ✅ {directory}/__init__.py exists")
            else:
                print(f"   ⚠️  {directory}/__init__.py missing")
                all_present = False
        else:
            print(f"❌ {directory}/ missing")
            all_present = False
    
    for directory in optional_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/ exists")
        else:
            print(f"ℹ️  {directory}/ will be created automatically")
    
    return all_present

def check_required_files():
    """Check if all required Python files exist"""
    print_header("Required Files Check")
    
    required_files = {
        'app.py': 'Main application file',
        'requirements.txt': 'Dependencies file',
        'parsers/pdf_parser.py': 'PDF parser',
        'parsers/docx_parser.py': 'DOCX parser',
        'extractors/langchain_extractor.py': 'LangChain extractor',
        'extractors/vision_extractor.py': 'Vision extractor',
        'storage/excel_handler.py': 'Excel handler',
        'utils/validators.py': 'Validators',
        'utils/helpers.py': 'Helper functions'
    }
    
    all_present = True
    
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            if size > 50:  # File should have some content
                print(f"✅ {file_path:40} ({size} bytes)")
            else:
                print(f"⚠️  {file_path:40} (file is too small)")
                all_present = False
        else:
            print(f"❌ {file_path:40} - MISSING")
            all_present = False
    
    return all_present

def test_imports():
    """Test if modules can be imported"""
    print_header("Module Import Test")
    
    test_imports = [
        ('parsers.pdf_parser', 'extract_text_from_pdf'),
        ('parsers.docx_parser', 'extract_text_from_docx'),
        ('extractors.langchain_extractor', 'extract_with_langchain'),
        ('extractors.vision_extractor', 'extract_with_openai_vision'),
        ('storage.excel_handler', 'save_to_excel'),
        ('utils.validators', 'validate_resume_data'),
        ('utils.helpers', 'generate_resume_id')
    ]
    
    all_imported = True
    
    for module_name, function_name in test_imports:
        try:
            module = __import__(module_name, fromlist=[function_name])
            func = getattr(module, function_name)
            print(f"✅ {module_name}.{function_name}")
        except ImportError as e:
            print(f"❌ {module_name}.{function_name} - Import Error: {e}")
            all_imported = False
        except AttributeError as e:
            print(f"❌ {module_name}.{function_name} - Function not found: {e}")
            all_imported = False
        except Exception as e:
            print(f"❌ {module_name}.{function_name} - Error: {e}")
            all_imported = False
    
    return all_imported

def run_functional_test():
    """Run a basic functional test"""
    print_header("Functional Test")
    
    try:
        # Test text cleaning
        from utils.helpers import clean_text, generate_resume_id
        
        test_text = "  This   is    test   text  "
        cleaned = clean_text(test_text)
        print(f"✅ Text cleaning works: '{cleaned}'")
        
        # Test ID generation
        resume_id = generate_resume_id()
        print(f"✅ ID generation works: {resume_id}")
        
        # Test OpenAI API key
        from dotenv import load_dotenv
        import os
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"✅ OpenAI API key found in .env")
        else:
            print(f"⚠️  OpenAI API key not found in .env")
        
        return True
        
    except Exception as e:
        print(f"❌ Functional test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def print_summary(results):
    """Print final summary"""
    print_header("Summary")
    
    checks = [
        ("Python Version", results.get('python', False)),
        ("Packages", results.get('packages', False)),
        ("Directory Structure", results.get('dirs', False)),
        ("Required Files", results.get('files', False)),
        ("Module Imports", results.get('imports', False)),
        ("Functional Tests", results.get('functional', False))
    ]
    
    passed = sum(1 for _, status in checks if status)
    total = len(checks)
    
    for check_name, status in checks:
        icon = "✅" if status else "❌"
        print(f"{icon} {check_name}")
    
    print(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! Your setup is complete.")
        print("\n📝 Next steps:")
        print("   1. Run: streamlit run app.py")
        print("   2. Upload sample resumes")
        print("   3. Test the extraction")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\n📝 Common fixes:")
        print("   - Install missing packages: pip install -r requirements.txt")
        print("   - Set up OpenAI API key: echo 'OPENAI_API_KEY=sk-...' > .env")
        print("   - Create missing files from the artifacts")
        print("   - Check directory structure")

def main():
    """Run all checks"""
    print("=" * 60)
    print("  Resume Screener - Installation Verification")
    print("=" * 60)
    
    results = {}
    
    # Run all checks
    results['python'] = check_python_version()
    results['packages'] = check_packages()
    results['dirs'] = check_directory_structure()
    results['files'] = check_required_files()
    results['imports'] = test_imports()
    results['functional'] = run_functional_test()
    
    # Print summary
    print_summary(results)

if __name__ == "__main__":
    main()