import json
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RAGEngine:
    def __init__(self, kb_path="../knowledge_base"):
        self.kb_path = kb_path
        self.faq_static = self._load_faq("faq_static.json")
        self.faq_dynamic = self._load_faq("faq_dynamic.json")
        self.vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
        self._build_vectors()
    
    def _load_faq(self, filename):
        path = Path(self.kb_path) / filename
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"faqs": []}
    
    def _build_vectors(self):
        all_questions = []
        self.qa_map = []
        
        for faq_set in [self.faq_static, self.faq_dynamic]:
            for qa in faq_set.get("faqs", []):
                all_questions.append(qa["question"])
                self.qa_map.append(qa)
        
        if all_questions:
            self.vectors = self.vectorizer.fit_transform(all_questions)
        else:
            self.vectors = None
    
    def query(self, question, language="de"):
        if self.vectors is None or len(self.qa_map) == 0:
            return "Entschuldigen Sie, die Wissensdatenbank ist noch nicht aufgebaut.", 0.0, []
        
        # Vektorisiere die Frage
        q_vector = self.vectorizer.transform([question])
        
        # Berechne Ähnlichkeiten
        similarities = cosine_similarity(q_vector, self.vectors)[0]
        
        # Top Match
        best_match_idx = np.argmax(similarities)
        confidence = float(similarities[best_match_idx])
        
        # Threshold für "Ich weiß das nicht"
        if confidence < 0.3:
            return "Entschuldigen Sie, diese Frage kann ich mit meinem Wissen nicht beantworten. Bitte kontaktieren Sie das Prüfungsamt oder die Studienberatung.", 0.0, []
        
        qa = self.qa_map[best_match_idx]
        return qa["answer"], confidence, qa.get("sources", [])
