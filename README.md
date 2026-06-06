# QNG-Check

Webanwendung zur vereinfachten Abschätzung der Gebäudeökobilanz nach den Anforderungen des Qualitätssiegels Nachhaltiges Gebäude (QNG).

Entwickelt im Rahmen des Moduls Digitalisierungsprojekt an der Technischen Hochschule Augsburg.

---

## Projektbeschreibung

QNG-Check ermöglicht die schnelle Bewertung verschiedener Gebäudeszenarien hinsichtlich:

- Primärenergiebedarf (QP,ne)
- Treibhauspotenzial (GWP)
- QNG-PLUS
- QNG-PREMIUM

Die Anwendung unterstützt den Vergleich unterschiedlicher Varianten für:

- Bauweise
- Energiestandard
- Heizsystem
- Lüftungssystem
- Photovoltaikfläche
- Batteriespeicher

---

## Funktionen

### Gebäudedaten

- Projektname erfassen
- Bauweise auswählen
- Energiestandard auswählen
- Nettogrundflächen eingeben
- Automatische Berechnung der Gesamt-NRF

### Szenarien

- Heizsystem auswählen
- Lüftungssystem auswählen
- PV-Fläche eingeben
- Batteriespeicher festlegen
- QNG-Level auswählen

### Ergebnisdarstellung

- Berechnung von QP,ne
- Berechnung von GWP
- Vergleich mit QNG-Grenzwerten
- Statusanzeige „erfüllt“ oder „nicht erfüllt“
- Aufschlüsselung der Teilbeiträge

### Projektverwaltung

- Projekte speichern
- Szenarien speichern
- Szenarien löschen
- Projektübersicht anzeigen

### Szenariovergleich

- Mehrere Szenarien auswählen
- Direkter Vergleich in Tabellenform
- Beste QP,ne-Werte hervorheben
- Beste GWP-Werte hervorheben

---

## Verwendete Technologien

### Backend

- Python
- Django 5

### Frontend

- HTML
- CSS
- JavaScript

### Datenbank

- SQLite

### Versionsverwaltung

- Git
- GitHub

### Qualitätssicherung

- Unit Tests
- GitHub Actions
- Pull Requests
- Branch Protection Rules

---

## Installation

Repository klonen:

```bash
git clone https://github.com/DBM-THA/Absch-tzung-der-Geb-ude-kobilanz-nach-QNG.git
```

Projektordner öffnen:

```bash
cd Absch-tzung-der-Geb-ude-kobilanz-nach-QNG
```

Abhängigkeiten installieren:

```bash
pip install -r requirements.txt
```

Migrationen ausführen:

```bash
python manage.py migrate
```

Server starten:

```bash
python manage.py runserver
```

Anwendung öffnen:

```text
http://127.0.0.1:8000
```

---

## Tests ausführen

Alle automatisierten Tests starten:

```bash
python manage.py test
```

Getestet werden unter anderem:

- Berechnungslogik
- QNG-Grenzwerte
- Projektverwaltung
- Szenarioverwaltung
- Fehlerfälle
- Datenbankbeziehungen

---

## Deployment

Die Anwendung kann lokal mit Django betrieben werden.

Start:

```bash
python manage.py runserver
```

Für Produktivumgebungen wird empfohlen:

- Gunicorn
- Nginx
- PostgreSQL

---

## Projektstruktur

```text
qng_project/
│
├── qngapp/
│   ├── models.py
│   ├── views.py
│   ├── calculations.py
│   ├── tests.py
│   └── templates/
│
├── static/
│
├── manage.py
│
└── requirements.txt
```

---

## Autoren

Güllühan Bakir

Leon Balliet

Technische Hochschule Augsburg

Studiengang Digitaler Baumeister
