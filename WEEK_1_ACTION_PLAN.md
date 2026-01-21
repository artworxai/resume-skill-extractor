# Week 1 Action Plan: Resume Agent for Recruiters
**Date:** January 15, 2026  
**Intern:** Dana Martinez  
**Supervisor:** Golda Velez  
**Project:** Agentic AI Resume Processing System

---

## 🎯 PROJECT GOAL
Build a production-ready AI agent that helps recruiters by:
1. Processing batches of resumes
2. Parsing and extracting skills
3. Analyzing candidate GitHub profiles
4. Ranking candidates based on qualifications
5. Detecting certificates/credentials (email, LinkedIn, GitHub)

## 📋 WEEK 1 TASKS

### Day 1-2: Environment Setup & Research
- [x] Create project workspace
- [ ] Set up Python virtual environment
- [ ] Install initial dependencies (anthropic, python-dotenv, PyPDF2)
- [ ] Get Claude API key from Anthropic
- [ ] Review Cooperation-org repositories:
  - linked-claims-extractor (for understanding their LLM extraction patterns)
  - LinkedCreds (for understanding credential/skill structures)
  - projects repo (for understanding the overall architecture)
- [ ] Study how recruiters currently evaluate resumes (research 15-20 min)

### Day 3-4: Build MVP (Minimum Viable Product)
**Goal:** Process ONE resume and extract skills

Components to build:
1. **Resume Parser** - Extract text from PDF/DOCX
2. **Skill Extractor** - Use Claude API to identify technical skills
3. **Simple Output** - Print results to console

### Day 5: GitHub Integration Planning
- [ ] Research GitHub API basics
- [ ] Understand what data is available (repos, languages, stars, contributions)
- [ ] Plan how to score/rank candidates based on GitHub activity

---

## 🛠️ TECHNICAL STACK

### Required Tools:
- **Python 3.9+** - Primary language
- **Claude API (Sonnet 4.5)** - For intelligent extraction
- **PyPDF2 / python-docx** - For resume parsing
- **GitHub API / PyGithub** - For profile analysis
- **python-dotenv** - For managing API keys

### Project Structure:
```
resume-agent/
├── src/
│   ├── __init__.py
│   ├── resume_parser.py      # Extract text from resumes
│   ├── skill_extractor.py    # Use Claude to extract skills
│   ├── github_analyzer.py    # Analyze GitHub profiles
│   ├── candidate_ranker.py   # Rank candidates
│   └── certificate_finder.py # Find credentials
├── tests/
│   └── test_resume_parser.py
├── sample_data/
│   └── sample_resumes/       # Test resumes (PDFs)
├── .env                      # API keys (NEVER commit this!)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 MVP IMPLEMENTATION PLAN

### Phase 1: Simple Resume Parser (Days 1-2)
**Input:** Single PDF resume  
**Output:** Extracted text  
**Key Learning:** Working with file formats

### Phase 2: Skill Extraction with Claude (Days 3-4)
**Input:** Resume text  
**Output:** Structured list of skills (Python, JavaScript, Machine Learning, etc.)  
**Key Learning:** Prompt engineering with Claude API

### Phase 3: Batch Processing (Day 5)
**Input:** Folder of 5-10 resumes  
**Output:** CSV/JSON with all extracted data  
**Key Learning:** Scaling the solution

---

## 💡 KEY QUESTIONS TO ANSWER THIS WEEK

1. **What skills are most important to extract?**
   - Programming languages (Python, JavaScript, Java, etc.)
   - Frameworks (React, Django, TensorFlow, etc.)
   - Tools (Git, Docker, AWS, etc.)
   - Soft skills? (Maybe later)

2. **How should we structure the output?**
   - JSON format for programmatic access?
   - CSV for recruiters to open in Excel?
   - Both?

3. **What makes a "good" GitHub profile?**
   - Number of repositories?
   - Stars received?
   - Contribution frequency?
   - Languages used?
   - Quality of README files?

4. **Where do we find certificates?**
   - In resume text directly
   - LinkedIn profile (requires LinkedIn API or scraping)
   - GitHub profile badges/README
   - Email domain verification

---

## 📖 LEARNING RESOURCES

### Anthropic Claude API:
- [Anthropic API Docs](https://docs.anthropic.com)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)

### GitHub API:
- [GitHub REST API](https://docs.github.com/en/rest)
- [PyGithub Documentation](https://pygithub.readthedocs.io/)

### Resume Parsing:
- PyPDF2 for PDFs
- python-docx for Word documents
- Consider: pdfplumber for better PDF extraction

---

## 🎓 SUCCESS CRITERIA FOR WEEK 1

By end of Week 1, you should have:
1. ✅ Working development environment
2. ✅ Successfully parsed at least 1 resume
3. ✅ Extracted skills using Claude API
4. ✅ Basic understanding of GitHub API
5. ✅ Clear plan for Week 2 (batch processing + ranking)

---

## 🤝 COMMUNICATION WITH GOLDA

**Update schedule:** End of Week 1 (Friday or Monday)

**What to share:**
- What you built (even if basic)
- Challenges you faced
- Questions about direction
- Demo of the skill extraction (show her the output!)

**Questions to ask Golda:**
1. What format do recruiters prefer for the output?
2. Are there specific skills/technologies they care most about?
3. Should we integrate with any existing LinkedTrust systems?
4. What's the timeline for having a "client demo ready" version?

---

## 📌 IMPORTANT NOTES

- **Start simple!** Don't try to build everything at once
- **Use Claude API aggressively** - It's your main tool
- **Test with real resumes** - Ask friends/use your own resume
- **Document as you go** - Write comments in your code
- **Git commit often** - Small commits with clear messages
- **Don't worry about perfection** - This is MVP phase

---

## 🔐 SECURITY REMINDERS

- NEVER commit API keys to GitHub
- Use `.env` file for secrets
- Add `.env` to `.gitignore` immediately
- Use environment variables in your code

---

## NEXT STEPS (After this document)

1. Read through this entire plan
2. Set up your Python environment
3. Install Claude API library: `pip install anthropic`
4. Test Claude API with a simple "Hello World" script
5. Find or create 2-3 sample resumes for testing
6. Start building!

**Remember:** You're not expected to know everything. This is a learning experience. When stuck, search for examples, ask questions, and iterate!

Good luck! 🚀
