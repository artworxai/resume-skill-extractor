"""
batch_processor.py

Process multiple resumes at once and generate a report.
"""

import os
import json
from datetime import datetime
from typing import List, Dict
from .resume_parser import ResumeParser
from .skill_extractor import SkillExtractor


class BatchProcessor:
    """Process multiple resumes and generate reports."""
    
    def __init__(self):
        """Initialize the batch processor."""
        self.parser = ResumeParser()
        self.extractor = SkillExtractor()
        self.results = []
    
    def process_directory(self, directory_path: str) -> List[Dict]:
        """
        Process all resumes in a directory.
        
        Args:
            directory_path (str): Path to directory containing resumes
            
        Returns:
            List[Dict]: List of results for each resume
        """
        if not os.path.exists(directory_path):
            print(f"Error: Directory not found: {directory_path}")
            return []
        
        # Get all resume files
        resume_files = []
        for filename in os.listdir(directory_path):
            if filename.endswith(('.pdf', '.docx')):
                resume_files.append(os.path.join(directory_path, filename))
        
        if not resume_files:
            print(f"No resume files found in {directory_path}")
            return []
        
        print(f"\n{'='*60}")
        print(f"BATCH PROCESSING: {len(resume_files)} RESUMES")
        print(f"{'='*60}\n")
        
        # Process each resume
        self.results = []
        for i, resume_path in enumerate(resume_files, 1):
            print(f"[{i}/{len(resume_files)}] Processing: {os.path.basename(resume_path)}")
            result = self._process_single_resume(resume_path)
            self.results.append(result)
            print(f"  ✓ Extracted {result['total_skills']} skills\n")
        
        return self.results
    
    def _process_single_resume(self, resume_path: str) -> Dict:
        """
        Process a single resume file.
        
        Args:
            resume_path (str): Path to resume file
            
        Returns:
            Dict: Processing results
        """
        filename = os.path.basename(resume_path)
        
        # Parse resume
        text = self.parser.parse_file(resume_path)
        
        if not text:
            return {
                'filename': filename,
                'status': 'failed',
                'error': 'Could not parse file',
                'total_skills': 0
            }
        
        # Extract skills
        skills = self.extractor.extract_skills(text)
        
        # Calculate total
        total_skills = sum(len(items) for items in skills.values())
        
        return {
            'filename': filename,
            'status': 'success',
            'text_length': len(text),
            'skills': skills,
            'total_skills': total_skills
        }
    
    def generate_summary(self) -> Dict:
        """
        Generate summary statistics from processed resumes.
        
        Returns:
            Dict: Summary statistics
        """
        if not self.results:
            return {}
        
        total_processed = len(self.results)
        successful = sum(1 for r in self.results if r['status'] == 'success')
        failed = total_processed - successful
        
        # Aggregate all skills
        all_skills = {
            'programming_languages': set(),
            'frameworks': set(),
            'tools': set(),
            'databases': set(),
            'cloud_platforms': set(),
            'other_technical_skills': set()
        }
        
        for result in self.results:
            if result['status'] == 'success':
                for category, items in result['skills'].items():
                    all_skills[category].update(items)
        
        # Convert sets to sorted lists
        all_skills = {k: sorted(list(v)) for k, v in all_skills.items()}
        
        return {
            'total_resumes': total_processed,
            'successful': successful,
            'failed': failed,
            'unique_skills': all_skills,
            'total_unique_skills': sum(len(v) for v in all_skills.values())
        }
    
    def save_results(self, output_path: str):
        """
        Save results to JSON file.
        
        Args:
            output_path (str): Path to save results
        """
        summary = self.generate_summary()
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'summary': summary,
            'individual_results': self.results
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_path}")
    
    def print_summary(self):
        """Print a formatted summary of results."""
        summary = self.generate_summary()
        
        print("\n" + "="*60)
        print("BATCH PROCESSING SUMMARY")
        print("="*60)
        
        print(f"\nResumes Processed: {summary['total_resumes']}")
        print(f"  ✓ Successful: {summary['successful']}")
        print(f"  ✗ Failed: {summary['failed']}")
        
        print(f"\nUnique Skills Across All Candidates: {summary['total_unique_skills']}")
        
        for category, items in summary['unique_skills'].items():
            if items:
                category_name = category.replace('_', ' ').title()
                print(f"\n{category_name} ({len(items)}):")
                for item in items:
                    print(f"  • {item}")
        
        print("\n" + "="*60)


def main():
    """Example usage of BatchProcessor."""
    processor = BatchProcessor()
    
    # Process all resumes in sample_data/sample_resumes
    results = processor.process_directory("sample_data/sample_resumes")
    
    if results:
        # Print summary
        processor.print_summary()
        
        # Save to file
        processor.save_results("batch_results.json")
        
        print("\n✨ Batch processing complete!")
    else:
        print("\n⚠ No resumes to process!")
        print("Add some resume files to: sample_data/sample_resumes/")


if __name__ == "__main__":
    main()