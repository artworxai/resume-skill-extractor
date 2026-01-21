"""
skill_extractor.py

Uses Claude API to extract skills from resume text.
This is the core AI-powered component of the system.
"""

import os
import json
from typing import List, Dict
from anthropic import Anthropic
from dotenv import load_dotenv


class SkillExtractor:
    """Extract technical skills from resume text using Claude API."""
    
    def __init__(self):
        """Initialize the skill extractor with Claude API."""
        # Load environment variables
        load_dotenv()
        
        # Get API key
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables. "
                "Please set it in your .env file."
            )
        
        # Initialize Claude client
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def extract_skills(self, resume_text: str) -> Dict[str, List[str]]:
        """
        Extract skills from resume text using Claude API.
        
        Args:
            resume_text (str): The resume text to analyze
            
        Returns:
            Dict[str, List[str]]: Dictionary with categorized skills
        """
        # Create the prompt for Claude
        prompt = self._create_extraction_prompt(resume_text)
        
        try:
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract response
            response_text = message.content[0].text
            
            # Parse the JSON response
            skills = self._parse_skills_response(response_text)
            
            return skills
            
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            return {
                "programming_languages": [],
                "frameworks": [],
                "tools": [],
                "databases": [],
                "cloud_platforms": [],
                "other_technical_skills": []
            }
    
    def _create_extraction_prompt(self, resume_text: str) -> str:
        """
        Create a detailed prompt for skill extraction.
        
        Args:
            resume_text (str): The resume text
            
        Returns:
            str: The formatted prompt
        """
        prompt = f"""You are an expert technical recruiter. Analyze this resume and extract all technical skills.

Resume Text:
{resume_text}

Please identify and categorize the technical skills found in this resume. Return your response as a JSON object with the following structure:

{{
    "programming_languages": ["Python", "JavaScript", etc.],
    "frameworks": ["React", "Django", "TensorFlow", etc.],
    "tools": ["Git", "Docker", "VS Code", etc.],
    "databases": ["PostgreSQL", "MongoDB", etc.],
    "cloud_platforms": ["AWS", "Azure", "Google Cloud", etc.],
    "other_technical_skills": ["Machine Learning", "REST APIs", etc.]
}}

Rules:
1. Only include skills that are explicitly mentioned or clearly implied in the resume
2. Use standard names for technologies (e.g., "JavaScript" not "JS")
3. Do not invent or assume skills that aren't present
4. If a category has no skills, use an empty array []
5. Return ONLY the JSON object, no additional text

Extract the skills now:"""
        
        return prompt
    
    def _parse_skills_response(self, response: str) -> Dict[str, List[str]]:
        """
        Parse Claude's response into structured skills data.
        
        Args:
            response (str): The raw response from Claude
            
        Returns:
            Dict[str, List[str]]: Parsed skills dictionary
        """
        try:
            # Try to parse as JSON
            # Sometimes Claude adds extra text, so we need to extract just the JSON
            
            # Find JSON content (between first { and last })
            start = response.find('{')
            end = response.rfind('}')
            
            if start != -1 and end != -1:
                json_str = response[start:end+1]
                skills = json.loads(json_str)
                return skills
            else:
                print("Warning: Could not find JSON in response")
                return self._get_empty_skills_dict()
                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {str(e)}")
            print(f"Response was: {response[:200]}...")
            return self._get_empty_skills_dict()
    
    def _get_empty_skills_dict(self) -> Dict[str, List[str]]:
        """Return an empty skills dictionary."""
        return {
            "programming_languages": [],
            "frameworks": [],
            "tools": [],
            "databases": [],
            "cloud_platforms": [],
            "other_technical_skills": []
        }
    
    def print_skills_summary(self, skills: Dict[str, List[str]]):
        """
        Print a formatted summary of extracted skills.
        
        Args:
            skills (Dict[str, List[str]]): The skills dictionary
        """
        print("\n" + "=" * 60)
        print("EXTRACTED SKILLS SUMMARY")
        print("=" * 60)
        
        for category, items in skills.items():
            # Format category name (e.g., "programming_languages" -> "Programming Languages")
            category_name = category.replace('_', ' ').title()
            
            print(f"\n{category_name}:")
            if items:
                for item in items:
                    print(f"  • {item}")
            else:
                print("  (none found)")
        
        # Calculate total
        total_skills = sum(len(items) for items in skills.values())
        print(f"\n{'-' * 60}")
        print(f"Total Skills Found: {total_skills}")
        print("=" * 60)


def main():
    """Example usage of SkillExtractor."""
    
    # Example resume text (you would normally get this from resume_parser.py)
    example_resume = """
    John Doe
    Software Engineer
    
    Experience:
    - Built web applications using React and Node.js
    - Deployed services to AWS using Docker
    - Worked with PostgreSQL and MongoDB databases
    - Implemented CI/CD pipelines with GitHub Actions
    
    Skills:
    - Programming: Python, JavaScript, TypeScript
    - Frameworks: React, Express, Django
    - Tools: Git, Docker, VS Code
    - Cloud: AWS (EC2, S3, Lambda)
    """
    
    try:
        # Initialize extractor
        extractor = SkillExtractor()
        
        print("Testing Claude API skill extraction...")
        print(f"Using model: {extractor.model}")
        
        # Extract skills
        skills = extractor.extract_skills(example_resume)
        
        # Print results
        extractor.print_skills_summary(skills)
        
    except ValueError as e:
        print(f"Error: {str(e)}")
        print("\nMake sure you:")
        print("1. Created a .env file (copy from .env.template)")
        print("2. Added your ANTHROPIC_API_KEY to the .env file")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    main()
