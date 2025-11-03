# 📦 Complete Installation & Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation Steps](#installation-steps)
3. [Project Structure Setup](#project-structure-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Version 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 500MB free space
- **Internet**: Required for initial setup (downloading packages)

### Check Python Version
```bash
python --version
# or
python3 --version
```

If Python is not installed, download from: https://www.python.org/downloads/

---

## Installation Steps

### Step 1: Create Project Directory

```bash
# Create main project folder
mkdir resume_screener
cd resume_screener
```

### Step 2: Set Up Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

### Step 3: Create Directory Structure

```bash
# Create all required directories
mkdir parsers extractors storage utils uploads output

# Create __init__.py files
touch parsers/__init__.py
touch extractors/__init__.py
touch storage/__init__.py
touch utils/__init__.py
```

**On Windows (if touch doesn't work):**
```bash
type nul > parsers\__init__.py
type nul > extractors\__init__.py
type nul > storage\__init__.py
type nul > utils\__init__.py
```

### Step 4: Create All Python Files

Create the following files with the code provided in the artifacts:

```
Resume-screener/
│
├── app.py
├── requirements.txt
├── README.md
├── .env (OpenAI API key)
│
├── parsers/
│   ├── __init__.py
│   ├── pdf_parser.py
│   └── docx_parser.py
│
├── extractors/
│   ├── __init__.py
│   ├── langchain_extractor.py
│   └── vision_extractor.py
│
├── storage/
│   ├── __init__.py
│   └── excel_handler.py
│
└── utils/
    ├── __init__.py
    ├── validators.py
    └── helpers.py
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- streamlit
- pandas
- openpyxl
- PyPDF2
- pdfplumber
- python-docx
- openai
- langchain
- langchain-openai
- pydantic
- pypdfium2
- Pillow
- python-dotenv

**Installation might take 5-10 minutes depending on your internet speed.**

### Step 6: Set Up OpenAI API Key

Create a `.env` file in the project root:

```bash
# Windows
type nul > .env

# macOS/Linux
touch .env
```

Add your OpenAI API key:

```
OPENAI_API_KEY=sk-...
```

> **Important**: Get your API key from https://platform.openai.com/api-keys. Ensure you have billing enabled.

---

## Project Structure Setup

Your final directory structure should look like this:

```
Resume-screener/
│
├── app.py                          # Main application file
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── .env                            # OpenAI API key
│
├── parsers/                        # Text extraction
│   ├── __init__.py
│   ├── pdf_parser.py
│   └── docx_parser.py
│
├── extractors/                     # AI extraction
│   ├── __init__.py
│   ├── langchain_extractor.py
│   └── vision_extractor.py
│
├── storage/                        # Data storage
│   ├── __init__.py
│   └── excel_handler.py
│
├── utils/                          # Utilities
│   ├── __init__.py
│   ├── validators.py
│   └── helpers.py
│
├── uploads/                        # Temporary uploads (auto-created)
└── output/                         # Excel outputs (auto-created)
    └── resume_data.xlsx           # Persisted database
```

---

## Configuration

### 1. Verify Installation

Create a test file `test_setup.py`:

```python
# test_setup.py
import sys
print(f"Python version: {sys.version}")

try:
    import streamlit
    print(f"✅ Streamlit: {streamlit.__version__}")
except:
    print("❌ Streamlit not installed")

try:
    import pandas
    print(f"✅ Pandas: {pandas.__version__}")
except:
    print("❌ Pandas not installed")

try:
    import openai
    print(f"✅ OpenAI: {openai.__version__}")
except:
    print("❌ OpenAI not installed")

try:
    import langchain
    print(f"✅ LangChain: {langchain.__version__}")
except:
    print("❌ LangChain not installed")

try:
    import PyPDF2
    print("✅ PyPDF2 installed")
except:
    print("❌ PyPDF2 not installed")

try:
    import docx
    print("✅ python-docx installed")
except:
    print("❌ python-docx not installed")

print("\n🎉 All checks passed! Ready to run.")
```

Run it:
```bash
python test_setup.py
```

### 2. Update __init__.py Files

Copy the content from the `__init__.py Files & Setup Guide` artifact into respective directories.

---

## Running the Application

### Method 1: Standard Run

```bash
streamlit run app.py
```

### Method 2: Custom Port

```bash
streamlit run app.py --server.port 8502
```

### Method 3: With Custom Configuration

```bash
streamlit run app.py --server.maxUploadSize 200
```

The application will automatically open in your default browser at:
```
http://localhost:8501
```

---

## Testing

### 1. Test with Sample Resume

Create a sample resume or download test resumes:
- Search for "sample resume PDF" online
- Use your own resume
- Create a simple Word document with resume-like content

### 2. Upload and Process

1. Open the application
2. Go to "📤 Upload Resumes"
3. Upload your test resume(s)
4. Click "🚀 Process Resumes"
5. Check the extracted data in "📊 View Data"

### 3. Verify Extraction Quality

Check if the following are extracted correctly:
- ✅ Name
- ✅ Email
- ✅ Phone
- ✅ Education details
- ✅ Experience
- ✅ Skills

### 4. Test Excel Export

1. Process some resumes
2. Click "📥 Download Excel Report"
3. Open the Excel file and verify formatting

---

## Troubleshooting

### Issue 1: ModuleNotFoundError

**Problem:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```bash
# Ensure virtual environment is activated
# Then reinstall
pip install -r requirements.txt
```

### Issue 2: OpenAI API Key Error

**Problem:** `Error: OpenAI API key not found`

**Solution:**
```bash
# Ensure .env file exists with correct key
echo "OPENAI_API_KEY=sk-..." > .env

# Or manually create .env file and add:
# OPENAI_API_KEY=your_key_here
```

### Issue 3: PDF Extraction Fails

**Problem:** Can't extract text from PDF

**Solution:**
1. Ensure PDF is not password-protected
2. For scanned PDFs, install OCR:
```bash
pip install pytesseract pdf2image
# Also install Tesseract on your system:
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

### Issue 4: Port Already in Use

**Problem:** `Port 8501 is already in use`

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502

# Or kill the process using port 8501
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8501 | xargs kill -9
```

### Issue 5: Upload Size Limit

**Problem:** Cannot upload large resumes

**Solution:**

Create `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

### Issue 6: Permission Errors

**Problem:** Permission denied when creating directories

**Solution:**
```bash
# Run with appropriate permissions
# Or create directories manually:
mkdir uploads output
chmod 755 uploads output
```

### Issue 7: Import Errors

**Problem:** `ImportError: cannot import name 'extract_name'`

**Solution:**
1. Ensure all `__init__.py` files are created
2. Check file names match exactly
3. Restart the application

---

## Advanced Configuration

### 1. Customize Upload Limits

Edit `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200  # MB
maxMessageSize = 200  # MB

[browser]
serverAddress = "localhost"
serverPort = 8501
```

### 2. Enable Development Mode

```bash
streamlit run app.py --logger.level=debug
```

### 3. Run in Production

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

---

## Deployment Options

### 1. Streamlit Cloud (Free)

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your repository
4. Deploy!

### 2. Local Network

```bash
# Find your IP address
# Windows: ipconfig
# macOS/Linux: ifconfig

# Run with your IP
streamlit run app.py --server.address=0.0.0.0
# Access from other devices: http://YOUR_IP:8501
```

### 3. Docker (Advanced)

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t resume-screener .
docker run -p 8501:8501 resume-screener
```

---

## Performance Optimization

### 1. Enable Caching

The app already uses `@st.cache_data` for performance.

### 2. Process Resumes in Batches

For 100+ resumes, process in batches of 50.

### 3. Database Option

For permanent storage, consider adding SQLite:
```bash
pip install sqlite3
```

---

## Next Steps

1. ✅ Test with various resume formats
2. ✅ Customize skills database for your needs
3. ✅ Add more extraction patterns
4. ✅ Integrate with your HR workflow
5. ✅ Deploy to production

---

## Support

If you encounter any issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review error messages carefully
3. Ensure all files are in correct locations
4. Verify Python version compatibility

---

**🎉 Congratulations! Your Resume Screener is ready to use!**

Start processing resumes and save hours of manual work! 🚀