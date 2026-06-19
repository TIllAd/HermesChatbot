# WiSo Chatbot - MVP README

## 🎯 Überblick

Dies ist der MVP (Minimum Viable Product) des FAU WiSo Onboarding Chatbots. Ein intelligentes Chat-Interface für Erstsemesterstudierende mit:

- ✅ **RAG-basierte Antworten** (Retrieval-Augmented Generation)
- ✅ **Multi-Sprachen Support** (Deutsch, Englisch, erweiterbar)
- ✅ **Feedback-Logging** für spätere KI-Analyse
- ✅ **Production-Ready Architecture** (Docker, scalable)
- ✅ **LTI 1.1 vorbereitet** für StudOn-Integration

---

## 📦 Struktur

```
HermesChatbot/
├── backend/
│   ├── app.py                 # FastAPI Server
│   ├── rag_engine.py         # Retrieval & Ranking
│   ├── feedback_logger.py    # Feedback-Speicherung
│   └── requirements.txt      # Python Dependencies
├── frontend/
│   ├── ChatWidget.jsx        # React Component
│   ├── ChatWidget.css        # Styling
│   └── package.json          # JS Dependencies
├── knowledge_base/
│   ├── faq_static.json       # Statische FAQs
│   └── faq_dynamic.json      # Semesterspezifische FAQs
├── docker-compose.yml        # Local Development
├── .env.example              # Config Template
└── README.md                 # This file
```

---

## 🚀 Quick Start (Local Development)

### 1. Anforderungen
- Python 3.9+
- Node.js 16+
- Docker & Docker Compose (optional)

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend läuft dann auf: `http://localhost:8000`

API Endpoints:
- `POST /chat` - Frage beantworten
- `POST /feedback` - Feedback loggen
- `GET /stats` - Statistiken abrufen
- `GET /health` - Health Check

### 3. Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend läuft dann auf: `http://localhost:3000`

---

## 🏗️ Architektur

### Backend (Python/FastAPI)

**RAG-Engine** nutzt TF-IDF Vector Similarity für schnelle, relevante Matches:

1. FAQs laden (statisch + dynamisch)
2. Fragen vektorisieren (TF-IDF mit Character N-Grams)
3. Ähnlichkeit zur Benutzer-Frage berechnen
4. Top Match zurückgeben (mit Konfidenz-Score)

Threshold: < 0.3 Konfidenz → "Ich weiß das nicht"

### Frontend (React)

- Chat Interface mit Message History
- Beispiel-Fragen beim Start
- Sprachumschaltung (DE/EN)
- Feedback-Buttons (Rating 1-5)
- Mobile-responsive Design

---

## 📝 Knowledge Base Verwaltung

### Format

Beide FAQ-Dateien nutzen gleiches Format:

```json
{
  "language": "de",
  "faqs": [
    {
      "id": 1,
      "question": "Was ist StudOn?",
      "answer": "StudOn ist...",
      "category": "Plattformen",
      "sources": ["https://www.studon.fau.de"]
    }
  ]
}
```

### Neue FAQs hinzufügen

1. **Statische FAQs**: `knowledge_base/faq_static.json` editieren
2. **Dynamische FAQs** (Semesterspezifisch): `knowledge_base/faq_dynamic.json` editieren
3. Server neustarten oder (bei Docker) Auto-Reload nutzen

---

## 🔄 Feedback-Analyse (Meta-Level)

Feedback wird in SQLite geloggt:

```
chatbot_feedback.db
├── id (auto)
├── user_id (anonymous hash)
├── query (Nutzerfrage)
├── answer (Bot-Antwort)
├── rating (1-5 Stars)
├── category (Themenbereich)
└── created_at (timestamp)
```

Stats abrufen:
```bash
curl http://localhost:8000/stats
```

Beispiel Response:
```json
{
  "total_feedback": 42,
  "avg_rating": 4.2,
  "by_category": {
    "Module": 15,
    "Prüfungen": 20,
    "Plattformen": 7
  }
}
```

---

## 🐳 Docker Deployment

### Local
```bash
docker-compose up --build
```

Dann öffnen: `http://localhost:3000`

### Production (RRZE)

```bash
# Login zu RRZE VM
ssh user@chatbot-wiso.de

# Clone repo
git clone https://github.com/TIllAd/HermesChatbot
cd HermesChatbot

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 Skalierbarkeit

✅ Handles **500 Peak-User** mit:
- Async I/O (FastAPI/Uvicorn)
- TF-IDF Caching (nur beim FAQ-Reload gerechnet)
- Stateless Requests (horizontal skalierbar)

Für mehr: PostgreSQL + Multiple Worker Instances

---

## 🔐 Sicherheit

- ✅ CORS konfigurierbar (aktuell offen für Testing)
- ✅ Feedback anonym (nur Hash des User-ID)
- ✅ Keine PII in Logs gespeichert
- ✅ System-Prompt mit Anti-Jailbreak

---

## 🛠️ Entwicklung

### Code-Style
- Python: PEP 8
- React: Prettier/ESLint
- Keine externen APIs (nur lokale RAG)

### Testing
```bash
# Backend
cd backend
pytest tests/

# Frontend
cd frontend
npm test
```

### Logs
```bash
# Backend Logs
docker logs hermes-chatbot-backend

# Frontend Logs
docker logs hermes-chatbot-frontend
```

---

## 📅 Roadmap

- **Phase 1** (Juni): MVP mit FAQ-RAG ✅
- **Phase 2** (Juni-Juli): LTI 1.1 Integration + StudOn
- **Phase 3** (Juli+): Meta-Analysis Dashboard für Team
- **Phase 4** (Aug+): Multi-Sprachen (EN, ES, 中文, etc.)

---

## 👥 Maintenance

Hermes AI übernimmt:
- ✅ Weekly Feedback-Analyse (Hermes Cronjob)
- ✅ Bug-Fixes & Performance-Tuning
- ✅ Auto-Skalierung bei Bedarf
- ✅ Monitoring & Alerting

Team übernimmt:
- FAQ-Content Updates
- Semester-spezifische Änderungen
- UX-Reviews & Feedback
- Policy Decisions

---

## 🤝 Support

Issues: https://github.com/TIllAd/HermesChatbot/issues

Kontakt: Hermes AI Maintenance (automatisiert)

---

**Last Updated**: 2026-06-19  
**Version**: 0.1.0-MVP
