import fitz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
import sys

try:
   
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("NLTK data 'punkt' not found. Downloading...")
    try:
        nltk.download('punkt', quiet=True)
    except Exception:
        print("ERROR: Could not download NLTK 'punkt'. Please check internet.")
        sys.exit(1)


SKILL_DB = [
    "python", "java", "sql", "javascript", "react", "node.js", 
    "aws", "docker", "kubernetes", "tensorflow", "agile", "management", 
    "communication", "leadership", "scrum", "excel", "testing", "ai", 
    "cloud", "networking"
]

def extract_text(file_path):
    """Extracts raw text from PDF files using PyMuPDF."""
    try:
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except:
        return ""

def extract_skills_knowledge_base(text):
    """(Extraction Phase) Matches skills against the defined knowledge base."""
    text = text.lower()
    found_skills = []
    
    for skill in SKILL_DB:
        if skill in text:
            found_skills.append(skill)
            
    return list(set(found_skills))

def calculate_score(resume_text, jd_text):
    """(Matching Phase) Calculates Match % using the TF-IDF vector algorithm."""
    if not resume_text or not jd_text:
        return 0
        
    
    clean_resume = " ".join(word_tokenize(resume_text.lower()))
    clean_jd = " ".join(word_tokenize(jd_text.lower()))
    
    text_list = [clean_resume, clean_jd]
    
    
    vectorizer = TfidfVectorizer(stop_words='english')
    matrix = vectorizer.fit_transform(text_list)
    
    
    score = cosine_similarity(matrix)[0][1]
    
    return round(score * 100, 2)