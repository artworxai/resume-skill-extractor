"""
github_analyzer.py

Analyze candidate GitHub profiles for technical assessment.
"""

import os
from typing import Dict, Optional
from github import Github
from dotenv import load_dotenv


class GitHubAnalyzer:
    """Analyze GitHub profiles to assess candidate technical skills."""
    
    def __init__(self):
        """Initialize GitHub analyzer with API token."""
        load_dotenv()
        
        # GitHub token is optional but recommended for higher rate limits
        token = os.getenv('GITHUB_TOKEN')
        
        if token and token != 'your_github_token_here':
            self.github = Github(token)
            print("✓ Using authenticated GitHub API (higher rate limits)")
        else:
            self.github = Github()
            print("⚠ Using unauthenticated GitHub API (limited rate)")
    
    def analyze_profile(self, username: str) -> Optional[Dict]:
        """
        Analyze a GitHub user's profile.
        
        Args:
            username (str): GitHub username
            
        Returns:
            Optional[Dict]: Profile analysis or None if user not found
        """
        try:
            user = self.github.get_user(username)
            
            print(f"\n{'='*60}")
            print(f"ANALYZING GITHUB PROFILE: {username}")
            print(f"{'='*60}\n")
            
            # Get basic profile info
            profile_info = {
                'username': username,
                'name': user.name,
                'bio': user.bio,
                'company': user.company,
                'location': user.location,
                'email': user.email,
                'blog': user.blog,
                'public_repos': user.public_repos,
                'followers': user.followers,
                'following': user.following,
            }
            
            # Analyze repositories
            repos_analysis = self._analyze_repositories(user)
            
            # Calculate score
            score = self._calculate_score(profile_info, repos_analysis)
            
            return {
                'profile': profile_info,
                'repositories': repos_analysis,
                'score': score
            }
            
        except Exception as e:
            print(f"❌ Error analyzing GitHub profile '{username}': {str(e)}")
            return None
    
    def _analyze_repositories(self, user) -> Dict:
        """
        Analyze user's repositories.
        
        Args:
            user: GitHub user object
            
        Returns:
            Dict: Repository analysis
        """
        repos = list(user.get_repos())
        
        if not repos:
            return {
                'total_repos': 0,
                'languages': {},
                'total_stars': 0,
                'total_forks': 0,
                'top_repos': []
            }
        
        # Aggregate data
        languages = {}
        total_stars = 0
        total_forks = 0
        
        # Get top repos by stars
        repos_sorted = sorted(repos, key=lambda r: r.stargazers_count, reverse=True)
        top_repos = []
        
        for repo in repos:
            # Count languages
            if repo.language:
                languages[repo.language] = languages.get(repo.language, 0) + 1
            
            # Sum stats
            total_stars += repo.stargazers_count
            total_forks += repo.forks_count
        
        # Get top 5 repos
        for repo in repos_sorted[:5]:
            top_repos.append({
                'name': repo.name,
                'description': repo.description,
                'language': repo.language,
                'stars': repo.stargazers_count,
                'forks': repo.forks_count,
                'url': repo.html_url
            })
        
        return {
            'total_repos': len(repos),
            'languages': languages,
            'total_stars': total_stars,
            'total_forks': total_forks,
            'top_repos': top_repos
        }
    
    def _calculate_score(self, profile: Dict, repos: Dict) -> Dict:
        """
        Calculate overall GitHub score for candidate.
        
        Args:
            profile (Dict): Profile information
            repos (Dict): Repository analysis
            
        Returns:
            Dict: Scoring breakdown
        """
        score = 0
        breakdown = {}
        
        # Repositories (up to 30 points)
        repo_count = repos['total_repos']
        repo_score = min(30, repo_count * 2)
        breakdown['repositories'] = repo_score
        score += repo_score
        
        # Stars received (up to 25 points)
        stars = repos['total_stars']
        if stars > 100:
            star_score = 25
        elif stars > 50:
            star_score = 20
        elif stars > 20:
            star_score = 15
        elif stars > 5:
            star_score = 10
        else:
            star_score = stars
        breakdown['stars'] = star_score
        score += star_score
        
        # Language diversity (up to 20 points)
        lang_count = len(repos['languages'])
        lang_score = min(20, lang_count * 4)
        breakdown['language_diversity'] = lang_score
        score += lang_score
        
        # Followers (up to 15 points)
        followers = profile['followers']
        follower_score = min(15, followers // 2)
        breakdown['followers'] = follower_score
        score += follower_score
        
        # Forks (up to 10 points)
        forks = repos['total_forks']
        if forks > 20:
            fork_score = 10
        elif forks > 10:
            fork_score = 7
        elif forks > 5:
            fork_score = 5
        else:
            fork_score = min(5, forks)
        breakdown['forks'] = fork_score
        score += fork_score
        
        return {
            'total_score': score,
            'max_score': 100,
            'percentage': round(score, 1),
            'breakdown': breakdown,
            'rating': self._get_rating(score)
        }
    
    def _get_rating(self, score: float) -> str:
        """Get rating based on score."""
        if score >= 80:
            return "⭐ Exceptional"
        elif score >= 60:
            return "🌟 Strong"
        elif score >= 40:
            return "✨ Good"
        elif score >= 20:
            return "💫 Moderate"
        else:
            return "📝 Beginner"
    
    def print_analysis(self, analysis: Dict):
        """
        Print formatted analysis results.
        
        Args:
            analysis (Dict): Analysis results
        """
        if not analysis:
            return
        
        profile = analysis['profile']
        repos = analysis['repositories']
        score = analysis['score']
        
        print(f"\n{'='*60}")
        print("GITHUB PROFILE ANALYSIS")
        print(f"{'='*60}")
        
        # Profile info
        print(f"\n👤 Profile:")
        print(f"  Username: {profile['username']}")
        if profile['name']:
            print(f"  Name: {profile['name']}")
        if profile['company']:
            print(f"  Company: {profile['company']}")
        if profile['location']:
            print(f"  Location: {profile['location']}")
        if profile['bio']:
            print(f"  Bio: {profile['bio']}")
        
        # Stats
        print(f"\n📊 Statistics:")
        print(f"  Public Repositories: {profile['public_repos']}")
        print(f"  Followers: {profile['followers']}")
        print(f"  Following: {profile['following']}")
        print(f"  Total Stars Received: {repos['total_stars']}")
        print(f"  Total Forks: {repos['total_forks']}")
        
        # Languages
        print(f"\n💻 Languages Used ({len(repos['languages'])}):")
        for lang, count in sorted(repos['languages'].items(), 
                                   key=lambda x: x[1], reverse=True):
            print(f"  • {lang}: {count} repos")
        
        # Top repos
        if repos['top_repos']:
            print(f"\n🌟 Top Repositories:")
            for repo in repos['top_repos']:
                print(f"\n  📦 {repo['name']}")
                if repo['description']:
                    print(f"     {repo['description']}")
                print(f"     Language: {repo['language'] or 'N/A'}")
                print(f"     ⭐ {repo['stars']} stars | 🍴 {repo['forks']} forks")
                print(f"     {repo['url']}")
        
        # Score
        print(f"\n{'='*60}")
        print("CANDIDATE SCORE")
        print(f"{'='*60}")
        print(f"\n🎯 Overall Score: {score['total_score']}/{score['max_score']} ({score['percentage']}%)")
        print(f"   Rating: {score['rating']}")
        
        print(f"\n📈 Score Breakdown:")
        for category, points in score['breakdown'].items():
            category_name = category.replace('_', ' ').title()
            print(f"  • {category_name}: {points}")
        
        print(f"\n{'='*60}")


def main():
    """Example usage of GitHubAnalyzer."""
    analyzer = GitHubAnalyzer()
    
    # Example: Analyze a GitHub profile
    # Replace with actual GitHub username
    username = input("\nEnter GitHub username to analyze: ").strip()
    
    if username:
        analysis = analyzer.analyze_profile(username)
        
        if analysis:
            analyzer.print_analysis(analysis)
        else:
            print(f"\n❌ Could not analyze profile for '{username}'")
    else:
        print("\n⚠ No username provided")
        print("\nExample usage:")
        print("  python -m src.github_analyzer")
        print("  Enter username: torvalds")


if __name__ == "__main__":
    main()