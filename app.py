"""
Streamlit app for Resume Skill Extractor
"""

import streamlit as st
import os
import tempfile
from src.resume_parser import ResumeParser
from src.skill_extractor import SkillExtractor
from src.github_analyzer import GitHubAnalyzer

# Page config
st.set_page_config(
    page_title="Resume Skill Extractor",
    page_icon="📄",
    layout="wide"
)

# Initialize components
@st.cache_resource
def get_components():
    return {
        'parser': ResumeParser(),
        'extractor': SkillExtractor(),
        'github': GitHubAnalyzer()
    }

components = get_components()

# Title
st.title("📄 AI-Powered Resume Skill Extractor")
st.markdown("Extract skills from resumes and analyze GitHub profiles using Claude AI")

# Sidebar
st.sidebar.header("About")
st.sidebar.info(
    "This tool uses Claude API to extract technical skills from resumes "
    "and analyze GitHub profiles to rank candidates."
)

# Main tabs
tab1, tab2, tab3 = st.tabs(["📄 Single Resume", "📊 Batch Processing", "💻 GitHub Analysis"])

# Tab 1: Single Resume Analysis
with tab1:
    st.header("Upload a Resume")
    
    uploaded_file = st.file_uploader(
        "Choose a resume file (PDF or DOCX)", 
        type=['pdf', 'docx'],
        key="single"
    )
    
    if uploaded_file:
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        if st.button("🔍 Extract Skills", key="extract_single"):
            with st.spinner("Analyzing resume..."):
                # Parse resume
                text = components['parser'].parse_file(tmp_path)
                
                if text:
                    st.success(f"✅ Extracted {len(text)} characters from resume")
                    
                    # Extract skills
                    skills = components['extractor'].extract_skills(text)
                    
                    # Display results
                    total_skills = sum(len(items) for items in skills.values())
                    st.metric("Total Skills Found", total_skills)
                    
                    # Display by category
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Programming Languages")
                        if skills['programming_languages']:
                            for skill in skills['programming_languages']:
                                st.markdown(f"• {skill}")
                        else:
                            st.text("None found")
                        
                        st.subheader("Frameworks")
                        if skills['frameworks']:
                            for skill in skills['frameworks']:
                                st.markdown(f"• {skill}")
                        else:
                            st.text("None found")
                        
                        st.subheader("Tools")
                        if skills['tools']:
                            for skill in skills['tools']:
                                st.markdown(f"• {skill}")
                        else:
                            st.text("None found")
                    
                    with col2:
                        st.subheader("Databases")
                        if skills['databases']:
                            for skill in skills['databases']:
                                st.markdown(f"• {skill}")
                        else:
                            st.text("None found")
                        
                        st.subheader("Cloud Platforms")
                        if skills['cloud_platforms']:
                            for skill in skills['cloud_platforms']:
                                st.markdown(f"• {skill}")
                        else:
                            st.text("None found")
                        
                        st.subheader("Other Technical Skills")
                        if skills['other_technical_skills']:
                            for skill in skills['other_technical_skills']:
                                st.markdown(f"• {skill}")
                        else:
                            st.text("None found")
                else:
                    st.error("❌ Failed to extract text from resume")
        
        # Cleanup
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

# Tab 2: Batch Processing
with tab2:
    st.header("Batch Process Multiple Resumes")
    
    uploaded_files = st.file_uploader(
        "Choose multiple resume files (PDF or DOCX)", 
        type=['pdf', 'docx'],
        accept_multiple_files=True,
        key="batch"
    )
    
    if uploaded_files:
        st.info(f"📁 {len(uploaded_files)} files uploaded")
        
        if st.button("🔍 Process All Resumes", key="extract_batch"):
            results = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {i+1}/{len(uploaded_files)}: {uploaded_file.name}")
                
                # Save to temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_path = tmp_file.name
                
                # Parse and extract
                text = components['parser'].parse_file(tmp_path)
                
                if text:
                    skills = components['extractor'].extract_skills(text)
                    total_skills = sum(len(items) for items in skills.values())
                    
                    results.append({
                        'filename': uploaded_file.name,
                        'total_skills': total_skills,
                        'skills': skills
                    })
                
                # Cleanup
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Processing complete!")
            
            # Display results
            st.subheader("📊 Batch Results")
            
            # Summary
            total_processed = len(results)
            total_all_skills = sum(r['total_skills'] for r in results)
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Resumes Processed", total_processed)
            col2.metric("Total Skills Found", total_all_skills)
            col3.metric("Avg Skills/Resume", round(total_all_skills/total_processed, 1) if total_processed > 0 else 0)
            
            # Individual results
            for result in results:
                with st.expander(f"📄 {result['filename']} - {result['total_skills']} skills"):
                    cols = st.columns(3)
                    
                    for i, (category, items) in enumerate(result['skills'].items()):
                        with cols[i % 3]:
                            st.markdown(f"**{category.replace('_', ' ').title()}**")
                            if items:
                                for item in items:
                                    st.markdown(f"• {item}")
                            else:
                                st.text("None")

# Tab 3: GitHub Analysis
with tab3:
    st.header("Analyze GitHub Profile")
    
    github_username = st.text_input("Enter GitHub username", placeholder="e.g., torvalds")
    
    if st.button("🔍 Analyze Profile", key="analyze_github"):
        if github_username:
            with st.spinner(f"Analyzing {github_username}'s GitHub profile..."):
                analysis = components['github'].analyze_profile(github_username)
                
                if analysis:
                    profile = analysis['profile']
                    repos = analysis['repositories']
                    score = analysis['score']
                    
                    # Profile info
                    st.subheader(f"👤 {profile['username']}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Repositories", profile['public_repos'])
                    col2.metric("Followers", profile['followers'])
                    col3.metric("Stars", repos['total_stars'])
                    col4.metric("Score", f"{score['total_score']}/100")
                    
                    # Rating
                    st.metric("Rating", score['rating'])
                    
                    # Languages
                    st.subheader("💻 Languages")
                    if repos['languages']:
                        lang_cols = st.columns(min(len(repos['languages']), 4))
                        for i, (lang, count) in enumerate(sorted(repos['languages'].items(), key=lambda x: x[1], reverse=True)):
                            with lang_cols[i % 4]:
                                st.metric(lang, f"{count} repos")
                    
                    # Top repos
                    st.subheader("🌟 Top Repositories")
                    for repo in repos['top_repos'][:3]:
                        with st.expander(f"📦 {repo['name']} - ⭐ {repo['stars']}"):
                            if repo['description']:
                                st.write(repo['description'])
                            st.write(f"**Language:** {repo['language'] or 'N/A'}")
                            st.write(f"**Stars:** {repo['stars']} | **Forks:** {repo['forks']}")
                            st.write(f"[View on GitHub]({repo['url']})")
                else:
                    st.error(f"❌ Could not find GitHub user: {github_username}")
        else:
            st.warning("⚠️ Please enter a GitHub username")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by Dana Martinez | Powered by Claude AI & GitHub API")