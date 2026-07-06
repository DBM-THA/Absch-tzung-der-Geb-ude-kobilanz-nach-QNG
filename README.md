# QNG-Check – Abschätzung der Gebäudeökobilanz

## Projektbeschreibung

QNG-Check ist eine Webanwendung zur vereinfachten Abschätzung der Gebäudeökobilanz nach den Anforderungen des **Qualitätssiegels Nachhaltiges Gebäude (QNG)**.

Die Anwendung unterstützt Planende dabei, bereits in frühen Planungsphasen verschiedene Gebäudeszenarien zu erstellen, zu vergleichen und hinsichtlich ihrer Nachhaltigkeit zu bewerten.

Bewertet werden insbesondere:

- Primärenergiebedarf (QP,ne)
- Treibhauspotenzial (GWP)

sowie deren Einhaltung der QNG-Grenzwerte für **QNG-PLUS** und **QNG-PREMIUM**.

---

# Was ist QNG?

Das Qualitätssiegel Nachhaltiges Gebäude (QNG) ist ein staatlicher Standard zur Bewertung der Nachhaltigkeit von Gebäuden.

Bewertet werden unter anderem:

- Energieeffizienz
- CO₂-Emissionen
- Ressourceneinsatz
- Lebenszyklusbetrachtung

Die Einhaltung der QNG-Anforderungen ist Voraussetzung für verschiedene Förderprogramme im nachhaltigen Bauen.

---

# Beispielansicht

### Gebäudedaten

![Gebäudedaten](qngapp/static/images/buildingneu.jpg)

### Szenario & Ergebnis

![Szenario](qngapp/static/images/scenarioneu.jpg)

### Projektverwaltung

![Projekt](qngapp/static/images/project.jpg)

### Szenariovergleich

![Vergleich](qngapp/static/images/vergleich.jpg)

### PDF-Bericht

![PDF](qngapp/static/images/beispiel.jpg)

---

# Ziel des Projekts

- Übertragung komplexer Excel-Berechnungen in eine benutzerfreundliche Webanwendung
- Unterstützung bei der Variantenuntersuchung nachhaltiger Gebäude
- Vergleich verschiedener Gebäudeszenarien
- Transparente Darstellung der Berechnungsergebnisse
- Vereinfachung der frühen QNG-Bewertung

---

# Funktionsumfang

## Gebäudedaten

Erfassung von:

- Projektname
- Gebäudeart (Einfamilienhaus / Mehrfamilienhaus)
- Nettogrundfläche beheizt
- Nettogrundfläche Tiefgarage
- Gesamt-Nettogrundfläche (automatisch berechnet)
- Energiebezugsfläche Aₙ nach GEG
- Bauweise
- Energiestandard

---

## Szenarioanalyse

Auswahl von:

- Heizsystem
- Lüftungssystem
- Photovoltaikfläche
- Batteriespeicher
- QNG-Level (PLUS / PREMIUM)

---

## Ergebnisdarstellung

- Berechnung von QP,ne
- Berechnung von GWP
- Vergleich mit den jeweiligen Grenzwerten
- Balkendiagramme mit Grenzwerten
- Prozentuale Abweichungen
- Aufschlüsselung aller Teilbeiträge

---

## Projektverwaltung

- Projekte speichern
- Projekte bearbeiten
- Projekte löschen
- Doppelte Projektnamen verhindern
- Weitere Szenarien zu bestehenden Projekten hinzufügen

---

## Szenariovergleich

- Vergleich beliebig vieler Szenarien
- Automatisches Ranking
- Hervorhebung der besten Variante
- Direkter Vergleich aller Kennwerte

---

## PDF-Bericht

Für jedes Projekt kann automatisch ein strukturierter PDF-Bericht erzeugt werden.

Der Bericht enthält:

- Projektdaten
- Beste Variante
- Übersicht aller Szenarien
- Ranking
- Zusammenfassung der Ergebnisse

---

# Automatisierte Tests

Zur Qualitätssicherung wurden umfangreiche automatisierte Tests implementiert.

Getestet werden unter anderem:

- Berechnungslogik
- QNG-Grenzwerte
- Einfluss verschiedener Eingabeparameter
- Projektverwaltung
- Szenarioverwaltung
- Szenariovergleich
- PDF-Export
- Datenbankbeziehungen
- Fehlerfälle
- Weiterleitungen

Tests ausführen:

```bash
python manage.py test
```

---

# Verwendete Technologien

## Backend

- Python
- Django 5

## Frontend

- HTML
- CSS
- JavaScript

## Datenbank

- SQLite

## Reporting

- ReportLab

## Qualitätssicherung

- Django Test Framework
- GitHub Actions

## Versionsverwaltung

- Git
- GitHub
- Pull Requests
- Branch Protection Rules

---

# Installation

Repository klonen

```bash
git clone https://github.com/DBM-THA/Absch-tzung-der-Geb-ude-kobilanz-nach-QNG.git
```

Projekt öffnen

```bash
cd Absch-tzung-der-Geb-ude-kobilanz-nach-QNG
```

Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Migrationen ausführen

```bash
python manage.py migrate
```

Server starten

```bash
python manage.py runserver
```

Anwendung öffnen

```text
http://127.0.0.1:8000
```

---

# Deployment

Die Anwendung kann sowohl lokal als auch innerhalb einer Docker-Umgebung ausgeführt werden.

### Docker

Docker-Image erstellen:

```bash
docker build -t qng-check .
```

Docker-Container starten:

```bash
docker run -p 8000:8000 qng-check
```

Alternativ kann die Anwendung mit Docker Compose gestartet werden:

```bash
docker compose up --build
```

Nach dem Start ist die Anwendung erreichbar unter:

```text
http://localhost:8000
```

Das Docker-Image kann außerdem auf Docker Hub veröffentlicht und von dort auf einen Server heruntergeladen und gestartet werden.

---

# Projektstatus

| Bereich | Status |
|---------|--------|
| Benutzeroberfläche | ✅ |
| Berechnungslogik | ✅ |
| Datenbank | ✅ |
| Projektverwaltung | ✅ |
| Szenarioverwaltung | ✅ |
| Szenariovergleich | ✅ |
| Ranking | ✅ |
| PDF-Bericht | ✅ |
| Automatisierte Tests | ✅ |
| Dokumentation | ✅ |
| Docker-Deployment | ✅ |

---

# Autoren

**Güllühan Bakir**

**Leon Balliet**

Technische Hochschule Augsburg

Studiengang Digitaler Baumeister
