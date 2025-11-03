# ⚡ Quick Start Guide - Resume Screener

Get up and running in 5 minutes!

## 🚀 Quick Install (Copy-Paste)

```bash
# 1. Create project and navigate
mkdir resume_screener && cd resume_screener

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. Create directory structure
mkdir parsers extractors storage utils uploads output

# 5. Create __init__.py files
# Windows:
type nul > parsers\__init__.py && type nul > extractors\__init__.py && type nul > storage\__init__.py && type nul > utils\__init__.py
# macOS/Linux:
touch parsers/__init__.py extractors/__init__.py storage/__init__.py utils/__init__.py

# 6. Install packages
pip install streamlit pandas openpyxl PyPDF2 pdfplumber python-docx openai langchain langchain-openai pydantic pypdfium2 Pillow python-dotenv

# 7. Create .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env

# 8. Run the app
streamlit run app.py
```

## 📝 File Checklist

Make sure you have created these files with the provided code:

```
✅ app.py
✅ requirements.txt
✅ README.md
✅ .env (OpenAI API key)
✅ parsers/pdf_parser.py
✅ parsers/docx_parser.py
✅ extractors/langchain_extractor.py
✅ extractors/vision_extractor.py
✅ storage/excel_handler.py
✅ utils/validators.py
✅ utils/helpers.py
```

## 🎯 Usage Flow

### Step 1: Launch Application
```bash
streamlit run app.py
```
Browser opens automatically at `http://localhost:8501`

### Step 2: Upload Resumes
1. Click on **"📤 Upload Resumes"** in sidebar
2. Drag & drop or click to upload PDF/DOCX files
3. Can upload multiple files at once
4. Click **"🚀 Process Resumes"**

### Step 3: View Results
1. Go to **"📊 View Data"** page
2. See all extracted information in table
3. Use filters to search:
   - **Search box**: Type name or email
   - **Experience slider**: Set min/max years
   - **Degree filter**: Select education level

### Step 4: Export Data
1. Click **"📥 Export Filtered Data"**
2. Download Excel file with:
   - All resume data
   - Summary statistics
   - Formatted tables

### Step 5: View Analytics
1. Go to **"📈 Analytics"** page
2. See:
   - Total resumes processed
   - Average experience
   - Education distribution chart
   - Top skills chart

## 💡 Pro Tips

### Tip 1: Bulk Processing
Upload 10-50 resumes at once for efficient processing.

### Tip 2: Better Extraction
Resumes with clear sections (Education, Experience, Skills) extract better.

### Tip 3: Filter & Export
Use filters to shortlist candidates, then export only those resumes.

### Tip 4: Data Persistence
Data automatically saves to `output/resume_data.xlsx` and persists across refreshes!

### Tip 5: OpenAPI Costs
- Vision API: ~$0.01 per resume (high accuracy)
- LangChain: ~$0.001 per resume (cost-effective)
- Automatically falls back if quota exceeded

## 🔧 Common Commands

```bash
# Start application
streamlit run app.py

# Start on different port
streamlit run app.py --server.port 8502

# Start in development mode
streamlit run app.py --logger.level=debug

# Clear cache and restart
streamlit cache clear
streamlit run app.py

# Deactivate virtual environment
deactivate
```

## 🎨 UI Overview

```
┌─────────────────────────────────────────────────┐
│  🤖 AI-Powered Resume Screener                 │
├──────────────┬──────────────────────────────────┤
│  Sidebar     │  Main Content Area              │
│              │                                 │
│  📤 Upload   │  [File Upload Area]            │
│  📊 View     │  [Progress Bar]                │
│  📈 Analytics│  [Processing Status]           │
│  ℹ️ About    │  [Results Table]               │
│              │  [Export Button]               │
│  Quick Stats │                                │
│  Total: 25   │                                │
│  Avg Exp: 5y │                                │
└──────────────┴──────────────────────────────────┘
```

## 📊 Extracted Data Example

```
Name              : John Doe
Email             : john.doe@email.com
Phone             : +91-9876543210
Degree            : B.Tech
College           : IIT Bombay
Graduation Year   : 2020
CGPA              : 8.5
Major             : Computer Science
Experience        : 3.5 years
Current Company   : Google
Designation       : Software Engineer
Previous Companies: Microsoft, Amazon
Technical Skills  : Python, Machine Learning, Docker
Programming Lang  : Python, Java, JavaScript
Soft Skills       : Leadership, Communication
```

## ⚠️ Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Module not found | `pip install -r requirements.txt` |
| OpenAI API error | Check `.env` file has valid API key |
| Port in use | `streamlit run app.py --server.port 8502` |
| PDF won't extract | Ensure PDF is not password-protected |
| Upload fails | Check file size < 200MB |

## 📞 Need Help?

1. **Check README.md** - Detailed documentation
2. **Check INSTALLATION_GUIDE.md** - Step-by-step setup
3. **Error messages** - Read carefully, they're helpful!
4. **Google the error** - Most issues have solutions online

## 🎉 You're Ready!

Your Resume Screener is now operational. Start uploading resumes and experience the power of AI automation!

**Happy Screening! 🚀**

---

## 📚 Additional Resources

- **Streamlit Docs**: https://docs.streamlit.io/
- **spaCy Docs**: https://spacy.io/usage
- **Pandas Docs**: https://pandas.pydata.org/docs/
- **Python Regex**: https://docs.python.org/3/library/re.html

## 🔄 Quick Update

To update the application:
```bash
git pull origin main  # if using git
pip install -r requirements.txt --upgrade
streamlit cache clear
streamlit run app.py
```

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**Python**: 3.8+  
**License**: MIT