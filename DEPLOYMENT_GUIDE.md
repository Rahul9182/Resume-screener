# 🚀 Deployment Guide

Complete guide for deploying your Resume Screener application to production.

## Table of Contents
1. [Deployment Options](#deployment-options)
2. [Streamlit Cloud (Easiest)](#streamlit-cloud)
3. [Local Network](#local-network-deployment)
4. [Cloud Platforms](#cloud-platforms)
5. [Docker Deployment](#docker-deployment)
6. [Production Considerations](#production-considerations)

---

## Deployment Options Comparison

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| Streamlit Cloud | ⭐ Easy | Free | Public demos, portfolios |
| Local Network | ⭐⭐ Medium | Free | Internal company use |
| Heroku | ⭐⭐ Medium | Free tier available | Small teams |
| AWS/GCP/Azure | ⭐⭐⭐ Hard | Pay-as-you-go | Enterprise |
| Docker | ⭐⭐⭐ Hard | Depends on host | Flexible deployment |

---

## Streamlit Cloud

### Prerequisites
- GitHub account
- Your code in a GitHub repository

### Step 1: Prepare Your Repository

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Resume Screener"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/resume-screener.git
git branch -M main
git push -u origin main
```

### Step 2: Create .streamlit/config.toml

Create `.streamlit/config.toml` in your repository:

```toml
[server]
headless = true
port = $PORT
enableCORS = false
enableXsrfProtection = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

### Step 3: Update requirements.txt

Ensure your `requirements.txt` includes:
```
streamlit>=1.28.0
pandas>=2.1.0
openpyxl>=3.1.0
PyPDF2>=3.0.0
pdfplumber>=0.10.0
python-docx>=1.1.0
spacy>=3.7.0
nltk>=3.8.0
python-dateutil>=2.8.0
phonenumbers>=8.13.0
```

### Step 4: Add packages.txt for spaCy Model

Create `packages.txt`:
```
python3-dev
```

### Step 5: Create setup.sh for Post-Deployment

Create `setup.sh`:
```bash
#!/bin/bash
python -m spacy download en_core_web_sm
```

### Step 6: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Choose branch (main)
6. Set main file path: `app.py`
7. Click "Deploy"

Wait 5-10 minutes for deployment to complete!

### Your App URL
```
https://yourusername-resume-screener-app-xyz123.streamlit.app
```

---

## Local Network Deployment

### For Company Internal Use

**Step 1: Find Your IP Address**

```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
# or
hostname -I
```

Look for your local IP (e.g., `192.168.1.100`)

**Step 2: Run with Network Access**

```bash
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
```

**Step 3: Access from Other Computers**

```
http://YOUR_IP:8501
# Example: http://192.168.1.100:8501
```

**Step 4: Configure Firewall**

Allow port 8501:

**Windows:**
```bash
netsh advfirewall firewall add rule name="Streamlit" dir=in action=allow protocol=TCP localport=8501
```

**Linux:**
```bash
sudo ufw allow 8501/tcp
```

**Step 5: Keep Running (Optional)**

Use screen or tmux:
```bash
# Install screen
sudo apt-get install screen  # Linux
brew install screen          # macOS

# Start screen session
screen -S resume_screener

# Run app
streamlit run app.py --server.address=0.0.0.0

# Detach: Ctrl+A, then D
# Reattach: screen -r resume_screener
```

---

## Cloud Platforms

### Heroku Deployment

**Step 1: Install Heroku CLI**
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

**Step 2: Create Required Files**

Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

python -m spacy download en_core_web_sm
```

**Step 3: Deploy**
```bash
# Login
heroku login

# Create app
heroku create your-resume-screener

# Deploy
git push heroku main

# Open app
heroku open
```

### AWS EC2 Deployment

**Step 1: Launch EC2 Instance**
- Choose Ubuntu Server 22.04 LTS
- Instance type: t2.small (minimum)
- Configure security group: Allow port 8501

**Step 2: Connect and Setup**
```bash
# Connect via SSH
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone your repository
git clone https://github.com/yourusername/resume-screener.git
cd resume-screener

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run with nohup
nohup streamlit run app.py --server.address=0.0.0.0 --server.port=8501 &
```

**Step 3: Access Your App**
```
http://YOUR_EC2_PUBLIC_IP:8501
```

---

## Docker Deployment

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_sm

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p uploads output

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

### Create docker-compose.yml

```yaml
version: '3.8'

services:
  resume-screener:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./uploads:/app/uploads
      - ./output:/app/output
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t resume-screener .

# Run container
docker run -p 8501:8501 resume-screener

# Or use docker-compose
docker-compose up -d
```

### Docker Hub Deployment

```bash
# Tag image
docker tag resume-screener yourusername/resume-screener:latest

# Push to Docker Hub
docker push yourusername/resume-screener:latest

# Pull and run on any server
docker pull yourusername/resume-screener:latest
docker run -d -p 8501:8501 yourusername/resume-screener:latest
```

---

## Production Considerations

### 1. Environment Variables

Create `.env` file:
```bash
# Database (if using)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=resumes
DB_USER=admin
DB_PASSWORD=secure_password

# API Keys (if needed)
OPENAI_API_KEY=your_key_here

# Application
MAX_UPLOAD_SIZE=200
LOG_LEVEL=INFO
```

Load in app:
```python
from dotenv import load_dotenv
import os

load_dotenv()
max_size = os.getenv('MAX_UPLOAD_SIZE', 200)
```

### 2. Logging

Add logging configuration:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 3. Error Handling

Wrap main functions:
```python
try:
    # Your code
    process_resume(file)
except Exception as e:
    logger.error(f"Error processing: {str(e)}")
    st.error("An error occurred. Please try again.")
```

### 4. Performance Optimization

```python
# Cache heavy operations
@st.cache_data
def load_skills_database():
    # Load skills
    return skills

# Use session state
if 'data' not in st.session_state:
    st.session_state.data = load_data()
```

### 5. Security

**a. Authentication (Optional)**
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    "resume_screener",
    "auth_key",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show app
    main_app()
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

**b. HTTPS**
Use reverse proxy (Nginx):
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 6. Database Integration (Optional)

For permanent storage:
```python
import sqlite3

def save_to_database(resume_data):
    conn = sqlite3.connect('resumes.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO resumes (name, email, phone, experience, skills)
        VALUES (?, ?, ?, ?, ?)
    ''', (resume_data['name'], resume_data['email'], ...))
    
    conn.commit()
    conn.close()
```

### 7. Monitoring

Use Streamlit Cloud metrics or integrate:
```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### 8. Backup Strategy

```bash
# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup_$DATE.tar.gz output/ uploads/
# Upload to S3 or backup server
```

---

## Maintenance

### Regular Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart application
# (Method depends on deployment type)
```

### Monitoring Checklist

- [ ] Check application logs daily
- [ ] Monitor CPU/memory usage
- [ ] Track number of processed resumes
- [ ] Check error rates
- [ ] Verify data backups
- [ ] Test with sample resumes weekly

---

## Troubleshooting Production Issues

### High Memory Usage
```python
# Add memory limits
import resource
resource.setrlimit(resource.RLIMIT_AS, (2 * 1024**3, -1))  # 2GB limit
```

### Slow Processing
- Process resumes in batches
- Use caching
- Optimize regex patterns
- Consider async processing

### File Upload Issues
- Increase upload limits
- Check disk space
- Verify file permissions

---

## Support & Resources

- **Streamlit Forums**: https://discuss.streamlit.io/
- **Documentation**: https://docs.streamlit.io/
- **GitHub Issues**: Create issues in your repository

---

**🎉 Your Resume Screener is now production-ready!**