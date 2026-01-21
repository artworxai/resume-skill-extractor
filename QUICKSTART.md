# 🚀 QUICK START GUIDE
**First Day Setup - 30 Minutes**

## Step 1: Transfer Files to Your Laptop (5 min)

I've created a complete project starter for you. Copy the entire `resume-agent` folder to your laptop:

```
resume-agent/
├── README.md
├── WEEK_1_ACTION_PLAN.md  ← Read this first!
├── requirements.txt
├── .env.template
├── .gitignore
├── test_claude_connection.py
├── src/
│   ├── __init__.py
│   ├── resume_parser.py
│   └── skill_extractor.py
├── tests/
└── sample_data/
    └── sample_resumes/
```

## Step 2: Set Up Python Environment (10 min)

```bash
# Navigate to project folder
cd resume-agent

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Get Your Claude API Key (5 min)

1. Go to https://console.anthropic.com/
2. Sign in or create an account
3. Navigate to "API Keys"
4. Create a new key
5. Copy the key (starts with "sk-ant-...")

## Step 4: Configure Your Environment (2 min)

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your API key
# Use any text editor (VS Code, Notepad, etc.)
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx...
GITHUB_TOKEN=your_github_token_here
```

## Step 5: Test Everything Works (3 min)

```bash
# Test Claude API connection
python test_claude_connection.py

# If successful, test skill extraction
python src/skill_extractor.py
```

You should see:
- ✅ SUCCESS messages
- A list of extracted skills from the example resume

## Step 6: Read the Documentation (5 min)

Open and read these files:
1. `README.md` - Project overview
2. `WEEK_1_ACTION_PLAN.md` - Your detailed roadmap

---

## 🎯 Your First Coding Task (After Setup)

Once setup is complete, your first task is:

**Build a simple script that:**
1. Takes your own resume (Dana_Martinez_Federal_Resume_2026.docx)
2. Extracts the text using `resume_parser.py`
3. Extracts skills using `skill_extractor.py`
4. Prints the results

This will take 30-60 minutes and will teach you:
- How to use the existing modules
- How Claude API works
- How to debug issues
- What the output looks like

---

## 📞 When You're Stuck

1. **Read the error message carefully** - It usually tells you exactly what's wrong
2. **Check your .env file** - 90% of early issues are API key problems
3. **Google the error** - Someone has probably solved it before
4. **Ask me (Claude) for help** - Describe what you're trying to do and paste the error

---

## ✅ Today's Success Criteria

By end of today, you should have:
- [ ] Project files on your laptop
- [ ] Python virtual environment created
- [ ] All dependencies installed
- [ ] Claude API key configured
- [ ] Successfully run `test_claude_connection.py`
- [ ] Successfully extracted skills from example resume

**Time Estimate: 30-60 minutes total**

---

## 📅 Tomorrow's Goal

Create a script that processes YOUR resume and prints out all your skills!

Good luck! You've got this! 🎉
