# Resume Agent for Recruiters

An AI-powered system to help recruiters process resumes, extract skills, analyze GitHub profiles, and rank candidates.

## 🎯 Project Overview

This agentic AI system automates the tedious parts of candidate screening by:
- Processing batches of resumes (PDF/DOCX)
- Extracting technical skills using Claude AI
- Analyzing candidate GitHub profiles
- Ranking candidates based on qualifications
- Detecting certificates and credentials

## 🚀 Quick Start

### 1. Set up your environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API keys

```bash
# Copy template
cp .env.template .env

# Edit .env and add your keys
# Get your Claude API key from: https://console.anthropic.com/
```

### 3. Test your setup

```bash
python test_claude_connection.py
```

If you see "✅ SUCCESS!", you're ready to start building!

## 📁 Project Structure

```
resume-agent/
├── src/                      # Source code
│   ├── resume_parser.py      # Extract text from resumes
│   ├── skill_extractor.py    # Extract skills with Claude
│   ├── github_analyzer.py    # Analyze GitHub profiles
│   ├── candidate_ranker.py   # Rank candidates
│   └── certificate_finder.py # Find credentials
├── tests/                    # Unit tests
├── sample_data/              # Test resumes
├── .env                      # API keys (DO NOT COMMIT!)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🛠️ Tech Stack

- **Python 3.9+** - Core language
- **Claude API (Sonnet 4.5)** - AI-powered extraction
- **PyPDF2** - PDF parsing
- **python-docx** - Word document parsing
- **PyGithub** - GitHub API integration

## 📚 Resources

- [Anthropic API Docs](https://docs.anthropic.com)
- [GitHub API Docs](https://docs.github.com/en/rest)
- [Week 1 Action Plan](WEEK_1_ACTION_PLAN.md)

## 👤 Intern

**Dana Martinez**  
Machine Learning Engineering Intern  
LinkedTrust | University of Arizona

**Supervisor:** Golda Velez

## 📅 Timeline

- **Week 1:** MVP - Single resume processing
- **Week 2:** Batch processing + GitHub integration
- **Week 3:** Ranking algorithm + certificates
- **Week 4:** Demo-ready product

## 🔐 Security

- Never commit `.env` file
- Never commit API keys
- Keep sensitive data in `.gitignore`

---

**Last Updated:** January 15, 2026
