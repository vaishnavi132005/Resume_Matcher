import re

SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "JavaScript": ["javascript", "js", "node.js", "nodejs"],
    "C++": ["c++"],
    "SQL": ["sql", "mysql", "postgresql", "sqlite"],
    "Machine Learning": ["machine learning", "ml", "scikit-learn", "sklearn"],
    "Deep Learning": ["deep learning", "neural network", "neural networks"],
    "NLP": ["nlp", "natural language processing", "bert", "spacy"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Data Analysis": ["data analysis", "data analytics", "eda"],
    "Power BI": ["power bi", "powerbi"],
    "Excel": ["excel"],
    "Tableau": ["tableau"],
    "React": ["react", "reactjs", "react.js"],
    "HTML": ["html", "html5"],
    "CSS": ["css", "css3", "tailwind"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "REST API": ["rest api", "restful", "rest apis"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Git": ["git", "github"],
    "Linux": ["linux"],
    "MongoDB": ["mongodb"],
    "Data Visualization": ["data visualization", "matplotlib", "seaborn"],
}


def extract_skills(text):
    text = text.lower()
    found = []
    for skill, aliases in SKILLS.items():
        for alias in aliases:
            pattern = r"(?<![a-z0-9+#])" + re.escape(alias) + r"(?![a-z0-9+#])"
            if re.search(pattern, text):
                found.append(skill)
                break
    return found
