# Quick Start Guide — 15 Minuten bis zum laufenden Bot

## Schritt 1: Repository clonen

```bash
git clone https://github.com/TIllAd/HermesChatbot.git
cd HermesChatbot
```

## Schritt 2: Backend starten

```bash
cd backend

# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren
# Auf Linux/Mac:
source venv/bin/activate
# Auf Windows:
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Server starten
python app.py
```

Du solltest sehen:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Schritt 3: Frontend starten (neues Terminal)

```bash
cd frontend
npm install
npm start
```

Das öffnet automatisch `http://localhost:3000` im Browser.

## Schritt 4: Testen!

1. "Wo finde ich die Modulhandbücher?" → Bot antwortet
2. Feedback geben (Rate 1-5 Stars)
3. Sprache wechseln (DE → EN)

---

## Fertig! ✅

- Backend läuft auf `http://localhost:8000`
- Frontend läuft auf `http://localhost:3000`
- Logs anschauen: Terminal wo die Apps laufen

## Nächste Schritte

1. Weitere FAQs in `knowledge_base/*.json` hinzufügen
2. Push zu GitHub: `git add . && git commit && git push`
3. Deployment auf RRZE vorbereiten (siehe README.md)

---

**Probleme?**
- Python nicht gefunden? → `python3` statt `python` nutzen
- npm nicht gefunden? → Node.js installieren
- Port 8000/3000 schon in Nutzung? → `lsof -i :8000` zum Finden des Prozesses
