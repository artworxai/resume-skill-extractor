"""
resume_parser.py

Extracts text from resume files (PDF and DOCX formats).
This is the first step in the resume processing pipeline.
"""

import os
from typing import Optional
import PyPDF2
from docx import Document


class ResumeParser:
    """Parse resume files and extract text content."""
    
    def __init__(self):
        """Initialize the resume parser."""
        self.supported_formats = ['.pdf', '.docx']
    
    def parse_file(self, file_path: str) -> Optional[str]:
        """
        Parse a resume file and extract text.
        
        Args:
            file_path (str): Path to the resume file
            
        Returns:
            Optional[str]: Extracted text, or None if parsing failed
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return None
        
        # Get file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        # Check if format is supported
        if ext not in self.supported_formats:
            print(f"Error: Unsupported file format: {ext}")
            print(f"Supported formats: {', '.join(self.supported_formats)}")
            return None
        
        try:
            if ext == '.pdf':
                return self._parse_pdf(file_path)
            elif ext == '.docx':
                return self._parse_docx(file_path)
        except Exception as e:
            print(f"Error parsing file: {str(e)}")
            return None
    
    def _parse_pdf(self, file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            file_path (str): Path to PDF file
            
        Returns:
            str: Extracted text
        """
        text = ""
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from each page
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        
        return text.strip()
    
    def _parse_docx(self, file_path: str) -> str:
        """
        Extract text from a DOCX file.
        
        Args:
            file_path (str): Path to DOCX file
            
        Returns:
            str: Extracted text
        """
        doc = Document(file_path)
        
        # Extract text from all paragraphs
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return text.strip()


def main():
    """Example usage of ResumeParser."""
    parser = ResumeParser()
    
    # Example: Parse a resume
    # TODO: Replace with path to an actual resume file
    resume_path = "sample_data/sample_resumes/sample_resume.pdf"
    
    if os.path.exists(resume_path):
        print(f"Parsing resume: {resume_path}")
        text = parser.parse_file(resume_path)
        
        if text:
            print("\n" + "=" * 60)
            print("EXTRACTED TEXT:")
            print("=" * 60)
            print(text[:500] + "..." if len(text) > 500 else text)
            print("=" * 60)
            print(f"\nTotal characters: {len(text)}")
        else:
            print("Failed to extract text from resume")
    else:
        print(f"Sample resume not found at: {resume_path}")
        print("\nTo test this parser:")
        print("1. Add a resume file to: sample_data/sample_resumes/")
        print("2. Update the 'resume_path' variable above")
        print("3. Run this script again")


if __name__ == "__main__":
    main()
