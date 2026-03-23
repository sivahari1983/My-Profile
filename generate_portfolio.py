"""
Portfolio Generator - Extract and parse professional profile from PDF documents
"""

import pdfplumber
import re
from typing import Dict, List, Any


class PortfolioGenerator:
    """Extract structured portfolio data from PDF documents"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""
        self.lines = []
    
    def extract_text(self) -> str:
        """Extract all text from PDF file"""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                text = ""
                for page in pdf.pages:
                    text += page.extract_text() or ""
                self.text = text
                self.lines = [line.strip() for line in text.split('\n') if line.strip()]
                return text
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def parse_profile(self) -> Dict[str, Any]:
        """Main orchestrator - parse profile and extract all sections"""
        self.extract_text()
        
        return {
            'contact': self._extract_contact(),
            'summary': self._extract_summary(),
            'expertise': self._extract_expertise(),
            'experience': self._extract_experience(),
            'education': self._extract_education(),
            'skills': self._extract_skills(),
            'languages': self._extract_languages(),
            'certifications': self._extract_certifications(),
            'projects': self._extract_projects()
        }
    
    def _extract_contact(self) -> Dict[str, str]:
        """Extract contact information"""
        contact = {}
        
        # Email
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        email_match = re.search(email_pattern, self.text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\d{3,}[-.\s]?\d{3,}[-.\s]?\d{3,}'
        phone_match = re.search(phone_pattern, self.text)
        if phone_match:
            contact['phone'] = phone_match.group(0)
        
        # LinkedIn
        linkedin_pattern = r'(?:linkedin\.com/in/|linkedin:\s*)[\w\-]+'
        linkedin_match = re.search(linkedin_pattern, self.text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(0)
        
        # Location/City
        location_keywords = ['location', 'based in', 'city', 'residing']
        for i, line in enumerate(self.lines):
            for keyword in location_keywords:
                if keyword.lower() in line.lower():
                    if i + 1 < len(self.lines):
                        contact['location'] = self.lines[i + 1]
                    break
        
        return contact
    
    def _extract_summary(self) -> str:
        """Extract professional summary"""
        summary_keywords = ['professional summary', 'summary', 'objective', 'about', 'profile']
        
        for i, line in enumerate(self.lines):
            for keyword in summary_keywords:
                if keyword.lower() in line.lower():
                    # Get next few lines as summary
                    summary_lines = []
                    for j in range(i + 1, min(i + 4, len(self.lines))):
                        if self.lines[j] and not self._is_header(self.lines[j]):
                            summary_lines.append(self.lines[j])
                        else:
                            break
                    return ' '.join(summary_lines) if summary_lines else ""
        return ""
    
    def _extract_expertise(self) -> Dict[str, List[str]]:
        """Extract expertise/skills grouped by category"""
        expertise = {}
        expertise_found = False
        current_category = None
        
        expertise_keywords = ['expertise', 'core competencies', 'technical skills', 'skills & expertise']
        
        for i, line in enumerate(self.lines):
            # Look for expertise section header
            if any(keyword.lower() in line.lower() for keyword in expertise_keywords):
                expertise_found = True
                continue
            
            if expertise_found:
                # Stop at next major section
                if self._is_major_header(line):
                    break
                
                # Check if line is a category (capitalized, may contain skill keywords)
                if line and not line.startswith('•') and len(line) > 3:
                    skills = [s.strip() for s in line.split('•') if s.strip()]
                    if len(skills) > 0:
                        # First part is category, rest are skills
                        if len(skills) == 1:
                            current_category = skills[0]
                        else:
                            if not current_category:
                                current_category = 'Technical Skills'
                            expertise[current_category] = skills
        
        return expertise
    
    def _extract_experience(self) -> List[Dict[str, str]]:
        """Extract work experience entries"""
        experience = []
        experience_found = False
        
        experience_keywords = ['experience', 'work experience', 'professional experience', 'employment']
        
        for i, line in enumerate(self.lines):
            if any(keyword.lower() in line.lower() for keyword in experience_keywords):
                experience_found = True
                continue
            
            if experience_found:
                if self._is_major_header(line):
                    break
                
                # Check for date patterns (2020-2022, 2020 – Present, etc.)
                if self._contains_date(line):
                    job_entry = {
                        'title': '',
                        'company': '',
                        'period': '',
                        'description': ''
                    }
                    
                    # Extract period
                    date_pattern = r'\d{4}\s*[-–]\s*(?:\d{4}|Present|Now|Current)'
                    date_match = re.search(date_pattern, line)
                    if date_match:
                        job_entry['period'] = date_match.group(0)
                    
                    # Get title and company from surrounding lines
                    for j in range(max(0, i - 2), i):
                        if self.lines[j] and not self._contains_date(self.lines[j]):
                            if not job_entry['title']:
                                job_entry['title'] = self.lines[j]
                            else:
                                job_entry['company'] = self.lines[j]
                    
                    # Get description from next lines
                    desc_lines = []
                    for j in range(i + 1, min(i + 3, len(self.lines))):
                        if self.lines[j] and not self._contains_date(self.lines[j]):
                            desc_lines.append(self.lines[j])
                    job_entry['description'] = ' '.join(desc_lines)
                    
                    if job_entry['title']:
                        experience.append(job_entry)
        
        return experience
    
    def _extract_education(self) -> List[Dict[str, str]]:
        """Extract education entries"""
        education = []
        education_keywords = ['education', 'qualification', 'degree', 'university', 'school']
        
        for i, line in enumerate(self.lines):
            if any(keyword.lower() in line.lower() for keyword in education_keywords):
                # Extract next few lines as education info
                for j in range(i + 1, min(i + 3, len(self.lines))):
                    if self.lines[j] and self.lines[j].strip():
                        education.append({
                            'degree': self.lines[j],
                            'institution': self.lines[j + 1] if j + 1 < len(self.lines) else ''
                        })
                break
        
        return education
    
    def _extract_skills(self) -> List[str]:
        """Extract technical skills"""
        skills = []
        skills_keywords = ['technical skills', 'programming', 'tools', 'frameworks', 'languages:', 'skills:']
        
        for i, line in enumerate(self.lines):
            if any(keyword.lower() in line.lower() for keyword in skills_keywords):
                # Extract skills from current and next lines
                for j in range(i + 1, min(i + 5, len(self.lines))):
                    line_skills = [s.strip() for s in self.lines[j].split('•') if s.strip() and s.strip() not in skills]
                    skills.extend(line_skills)
                    if self._is_major_header(self.lines[j]):
                        break
        
        # Clean up skills - remove duplicates and sort
        return sorted(list(set(skills)))[:20]  # Limit to top 20
    
    def _extract_languages(self) -> List[str]:
        """Extract languages"""
        languages = []
        language_keywords = ['languages', 'language proficiency', 'fluent']
        
        for i, line in enumerate(self.lines):
            if any(keyword.lower() in line.lower() for keyword in language_keywords):
                for j in range(i + 1, min(i + 4, len(self.lines))):
                    if self._is_major_header(self.lines[j]):
                        break
                    lang_list = [l.strip() for l in re.split('[,•\n]', self.lines[j]) if l.strip()]
                    languages.extend(lang_list)
        
        return languages[:10]  # Limit to 10 languages
    
    def _extract_certifications(self) -> List[Dict[str, str]]:
        """Extract certifications"""
        certifications = []
        cert_keywords = ['certification', 'certified', 'license', 'aws', 'azure', 'gcp', 'ckad', 'cka']
        
        for i, line in enumerate(self.lines):
            for keyword in cert_keywords:
                if keyword.lower() in line.lower() and len(line) > 5:
                    year_match = re.search(r'\d{4}', line)
                    certifications.append({
                        'title': line,
                        'year': year_match.group(0) if year_match else '',
                        'status': 'Certified'
                    })
                    break
        
        return certifications[:15]  # Limit to 15 certifications
    
    def _extract_projects(self) -> List[Dict[str, str]]:
        """Extract projects"""
        projects = []
        project_keywords = ['project', 'built', 'developed', 'created']
        
        for i, line in enumerate(self.lines):
            if any(keyword.lower() in line.lower() for keyword in project_keywords):
                description_lines = []
                for j in range(i + 1, min(i + 3, len(self.lines))):
                    if self.lines[j] and not self._is_major_header(self.lines[j]):
                        description_lines.append(self.lines[j])
                
                if description_lines:
                    projects.append({
                        'title': line,
                        'description': ' '.join(description_lines),
                        'status': 'Complete'
                    })
        
        return projects[:10]  # Limit to 10 projects
    
    def _contains_date(self, line: str) -> bool:
        """Check if line contains date pattern"""
        date_pattern = r'\d{4}\s*[-–]\s*(?:\d{4}|Present|Now|Current|Today)'
        return bool(re.search(date_pattern, line))
    
    def _is_header(self, line: str) -> bool:
        """Check if line appears to be a section header"""
        if len(line) > 50:
            return False
        if line.isupper() or (line and line[0].isupper() and line.count(' ') < 4):
            return True
        return False
    
    def _is_major_header(self, line: str) -> bool:
        """Check if line is a major section header"""
        major_headers = ['EXPERIENCE', 'EDUCATION', 'SKILLS', 'CERTIFICATION', 'PROJECT', 
                        'EXPERTISE', 'LANGUAGE', 'SUMMARY', 'CONTACT', 'ABOUT']
        return any(header in line.upper() for header in major_headers)
