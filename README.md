# QNG-Check – Abschätzung der Gebäudeökobilanz

## Projektbeschreibung

QNG-Check ist eine Webanwendung zur vereinfachten Abschätzung der Gebäudeökobilanz nach den Anforderungen des **Qualitätssiegels Nachhaltiges Gebäude (QNG)**.

Die Anwendung unterstützt Planende dabei, bereits in frühen Planungsphasen verschiedene Gebäudeszenarien zu bewerten und hinsichtlich ihrer Nachhaltigkeit zu vergleichen.

Bewertet werden insbesondere:

* Primärenergiebedarf (QP,ne)
* Treibhauspotenzial (GWP)

sowie deren Einhaltung der QNG-Grenzwerte für **QNG-PLUS** und **QNG-PREMIUM**.

---

## Was ist QNG?

Das Qualitätssiegel Nachhaltiges Gebäude (QNG) ist ein staatlicher Standard zur Bewertung der Nachhaltigkeit von Gebäuden.

Bewertet werden unter anderem:

* Energieeffizienz
* CO₂-Emissionen
* Ressourceneinsatz
* Lebenszyklusbetrachtung

Die Einhaltung der QNG-Anforderungen ist unter anderem Voraussetzung für verschiedene Förderprogramme im nachhaltigen Bauen.

---

## Beispielansicht

### Gebäudedaten

![Gebäudedaten](qngapp/static/images/buildingneu.jpg)

### Szenario & Ergebnis

![Szenario](qngapp/static/images/scenarioneu.jpg)

### Projekt & Vergleich

![Projekt](qngapp/static/images/project.jpg)

![Beispiel](qngapp/static/images/beispiel.jpg)

![Vergleich](qngapp/static/images/vergleich.jpg)

---

## Ziel des Projekts

* Übertragung komplexer Excel-Berechnungen in eine benutzerfreundliche Webanwendung
* Unterstützung bei der Variantenuntersuchung nachhaltiger Gebäude
* Transparente Darstellung von Einflussfaktoren auf QP,ne und GWP
* Vereinfachung der frühen QNG-Bewertung

---

## Funktionsumfang

### Gebäudedaten

Erfassung von:

* Projektname
* Gebäudeart (Einfamilienhaus / Mehrfamilienhaus)
* Nettogrundfläche beheizt
* Nettogrundfläche Tiefgarage
* Gesamt-Nettogrundfläche (automatisch berechnet)
* Energiebezugsfläche Aₙ nach GEG
* Bauweise
* Energiestandard

### Szenarioanalyse

Auswahl von:

* Heizsystem
* Lüftungssystem
* Photovoltaikfläche
* Batteriespeicher
* QNG-Level (PLUS / PREMIUM)

### Ergebnisdarstellung

* Berechnung von QP,ne
* Berechnung von GWP
* Vergleich mit den QNG-Grenzwerten
* Grafische Ergebnisdarstellung
* Aufschlüsselung der Teilbeiträge
* Automatische Hervorhebung der besten Werte
* PDF-Bericht exportieren

### Projektverwaltung

* Projekte speichern
* Projekte anzeigen
* Projekte löschen
* Doppelte Projektnamen verhindern
* Weitere Szenarien zu bestehenden Projekten hinzufügen
* Szenarien speichern
* Szenarien löschen

### Szenariovergleich

* Vergleich mehrerer Szenarien eines Projekts
* Ranking der Varianten
* Hervorhebung der besten Variante
* Direkte Gegenüberstellung aller Kennwerte
* Automatische Bewertung der Szenarien

---

## Automatisierte Tests

Zur Qualitätssicherung wurden automatisierte Tests implementiert.

Getestet werden unter anderem:

* Berechnungslogik für QP,ne und GWP
* Einfluss von Photovoltaikflächen
* Einfluss von Tiefgaragenflächen
* QNG-Grenzwerte für PLUS und PREMIUM
* Statusermittlung erfüllt / nicht erfüllt
* Datenbankbeziehungen zwischen Building, Scenario und Result
* Projekt- und Szenarioverwaltung
* Fehlerfälle und Weiterleitungen

Tests ausführen:

```bash
python manage.py test
```

---

## Verwendete Technologien

### Backend

* Python
* Django 5

### Frontend

* HTML
* CSS
* JavaScript

### Datenbank

* SQLite

### Reporting

* ReportLab (PDF-Export)

### Versionsverwaltung & Qualitätssicherung

* Git
* GitHub
* GitHub Actions
* Pull Requests
* Branch Protection Rules

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

## Deployment

Die Anwendung kann lokal über den Django-Entwicklungsserver gestartet werden.

```bash
python manage.py runserver
```

Alle benötigten Abhängigkeiten werden über die Datei `requirements.txt` bereitgestellt.

---

## Projektstatus (Sprint 6)

| Bereich                 | Status    |
| ----------------------- | --------- |
| GUI                     | umgesetzt |
| Datenstruktur           | umgesetzt |
| Berechnungslogik        | umgesetzt |
| Projektverwaltung       | umgesetzt |
| Szenarioverwaltung      | umgesetzt |
| Szenariovergleich       | umgesetzt |
| Automatisierte Tests    | umgesetzt |
| Workflow-Stabilisierung | umgesetzt |
| Dokumentation           | umgesetzt |
| PDF-Export              | umgesetzt |

---


## Autoren

**Güllühan Bakir**
**Leon Balliet**

Technische Hochschule Augsburg

Studiengang Digitaler Baumeister
