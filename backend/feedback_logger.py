import sqlite3
import json
from datetime import datetime
from pathlib import Path

class FeedbackLogger:
    def __init__(self, db_path="chatbot_feedback.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                query TEXT,
                answer TEXT,
                rating INTEGER,
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def log(self, feedback_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO feedback (user_id, query, answer, rating, category)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            feedback_data.get('user_id'),
            feedback_data.get('query'),
            feedback_data.get('answer'),
            feedback_data.get('rating'),
            feedback_data.get('category')
        ))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM feedback')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(rating) FROM feedback')
        avg_rating = cursor.fetchone()[0] or 0
        
        cursor.execute('SELECT category, COUNT(*) as count FROM feedback GROUP BY category')
        by_category = dict(cursor.fetchall())
        
        conn.close()
        
        return {
            "total_feedback": total,
            "avg_rating": round(avg_rating, 2),
            "by_category": by_category
        }
