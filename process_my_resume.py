"""
Process Dana's actual resume and extract skills.
"""

from src.resume_parser import ResumeParser
from src.skill_extractor import SkillExtractor

def main():
    # Initialize components
    parser = ResumeParser()
    extractor = SkillExtractor()
    
    # Path to your resume
    resume_path = "sample_data/sample_resumes/Dana_Martinez_Federal_Resume_2026.docx"
    
    print("=" * 60)
    print("PROCESSING DANA'S RESUME")
    print("=" * 60)
    
    # Step 1: Parse the resume
    print("\n📄 Step 1: Extracting text from resume...")
    resume_text = parser.parse_file(resume_path)
    
    if not resume_text:
        print("❌ Failed to parse resume!")
        return
    
    print(f"✅ Extracted {len(resume_text)} characters")
    print(f"First 200 characters: {resume_text[:200]}...")
    
    # Step 2: Extract skills using Claude
    print("\n🤖 Step 2: Using Claude to extract skills...")
    skills = extractor.extract_skills(resume_text)
    
    # Step 3: Display results
    extractor.print_skills_summary(skills)
    
    print("\n✨ Done! These are YOUR skills according to Claude AI!")

if __name__ == "__main__":
    main()