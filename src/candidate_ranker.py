"""
candidate_ranker.py

Rank candidates based on resume skills and GitHub profiles.
"""

from typing import List, Dict, Optional
from .batch_processor import BatchProcessor
from .github_analyzer import GitHubAnalyzer


class CandidateRanker:
    """Rank candidates by combining resume and GitHub data."""
    
    def __init__(self):
        """Initialize the candidate ranker."""
        self.batch_processor = BatchProcessor()
        self.github_analyzer = GitHubAnalyzer()
    
    def rank_candidates(self, resume_dir: str, github_usernames: Dict[str, str]) -> List[Dict]:
        """
        Rank candidates based on resumes and GitHub profiles.
        
        Args:
            resume_dir (str): Directory containing resumes
            github_usernames (Dict[str, str]): Map of filename to GitHub username
            
        Returns:
            List[Dict]: Ranked candidates
        """
        print("\n" + "="*60)
        print("CANDIDATE RANKING SYSTEM")
        print("="*60)
        
        # Step 1: Process all resumes
        print("\n📄 Step 1: Processing resumes...")
        resume_results = self.batch_processor.process_directory(resume_dir)
        
        # Step 2: Analyze GitHub profiles
        print("\n💻 Step 2: Analyzing GitHub profiles...")
        candidates = []
        
        for resume in resume_results:
            if resume['status'] != 'success':
                continue
            
            filename = resume['filename']
            github_username = github_usernames.get(filename)
            
            candidate = {
                'filename': filename,
                'resume_skills': resume['skills'],
                'total_skills': resume['total_skills'],
                'github_username': github_username,
                'github_analysis': None,
                'github_score': 0,
                'combined_score': 0
            }
            
            # Analyze GitHub if username provided
            if github_username:
                print(f"\n  Analyzing GitHub: {github_username}")
                github_analysis = self.github_analyzer.analyze_profile(github_username)
                
                if github_analysis:
                    candidate['github_analysis'] = github_analysis
                    candidate['github_score'] = github_analysis['score']['total_score']
            
            # Calculate combined score
            candidate['combined_score'] = self._calculate_combined_score(candidate)
            
            candidates.append(candidate)
        
        # Step 3: Sort by combined score
        candidates_ranked = sorted(candidates, 
                                   key=lambda x: x['combined_score'], 
                                   reverse=True)
        
        return candidates_ranked
    
    def _calculate_combined_score(self, candidate: Dict) -> float:
        """
        Calculate combined score from resume and GitHub.
        
        Weighting:
        - Resume skills: 40%
        - GitHub score: 60%
        
        Args:
            candidate (Dict): Candidate data
            
        Returns:
            float: Combined score (0-100)
        """
        # Resume score (normalize to 100)
        # Assume 50 skills = 100 points
        resume_score = min(100, (candidate['total_skills'] / 50) * 100)
        
        # GitHub score (already 0-100)
        github_score = candidate['github_score']
        
        # Combined weighted score
        combined = (resume_score * 0.4) + (github_score * 0.6)
        
        return round(combined, 1)
    
    def print_rankings(self, candidates: List[Dict]):
        """
        Print formatted candidate rankings.
        
        Args:
            candidates (List[Dict]): Ranked candidates
        """
        print("\n" + "="*60)
        print("CANDIDATE RANKINGS")
        print("="*60)
        
        for i, candidate in enumerate(candidates, 1):
            print(f"\n{'='*60}")
            print(f"RANK #{i} - {candidate['filename']}")
            print(f"{'='*60}")
            
            print(f"\n🎯 Combined Score: {candidate['combined_score']}/100")
            print(f"  📄 Resume Skills: {candidate['total_skills']} skills")
            print(f"  💻 GitHub Score: {candidate['github_score']}/100")
            
            # Top skills from resume
            print(f"\n💡 Top Skills:")
            for category, skills in candidate['resume_skills'].items():
                if skills:
                    print(f"  • {category.replace('_', ' ').title()}: {', '.join(skills[:3])}")
            
            # GitHub highlights
            if candidate['github_analysis']:
                gh = candidate['github_analysis']
                profile = gh['profile']
                repos = gh['repositories']
                
                print(f"\n🔗 GitHub Profile:")
                print(f"  Username: {candidate['github_username']}")
                print(f"  Repos: {profile['public_repos']}")
                print(f"  Stars: {repos['total_stars']}")
                print(f"  Languages: {', '.join(list(repos['languages'].keys())[:5])}")
        
        print(f"\n{'='*60}")
        print(f"Total Candidates Ranked: {len(candidates)}")
        print(f"{'='*60}\n")


def main():
    """Example usage of CandidateRanker."""
    ranker = CandidateRanker()
    
    # Example: Map resume filenames to GitHub usernames
    github_map = {
        'Dana W. Martinez Resume.docx': 'artworxai',
        # Add more mappings as needed
    }
    
    # Rank candidates
    candidates = ranker.rank_candidates('sample_data/sample_resumes', github_map)
    
    # Print rankings
    ranker.print_rankings(candidates)


if __name__ == "__main__":
    main()