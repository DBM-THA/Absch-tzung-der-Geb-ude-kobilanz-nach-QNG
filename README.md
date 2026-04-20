# Absch-tzung-der-Geb-ude-kobilanz-nach-QNG
Python-basierter Web-Prototyp zur Abschätzung der Gebäudeökobilanz von Wohngebäuden nach QNG-Anforderungen.

## Projektziel
Ziel des Projekts ist die Entwicklung eines ersten digitalen Werkzeugs, mit dem zentrale Gebäudedaten und Variantenparameter eingegeben, verarbeitet und als vereinfachte Ergebniswerte dargestellt werden können.

## Sprint 2 – Aktueller Stand
Im zweiten Sprint wurde der Schritt von der ersten Idee zu einem kleinen funktionsfähigen System umgesetzt.

Aktuell vorhanden:
- minimales Django-Setup
- erste Benutzeroberfläche
- einfache Eingabe von Projekt- und Variantenparametern
- vereinfachte Python-Logik zur Berechnung
- Ausgabe von GWP, QP,ne und QNG-Status
- erste funktionierende End-to-End-Pipeline

## Konzept
### Goal
Entwicklung eines webbasierten Prototyps zur vereinfachten Abschätzung der Gebäudeökobilanz nach QNG-Anforderungen.

### Data Flow
Input → Processing → Output

- **Input:** Gebäudedaten und Variantenparameter
- **Processing:** vereinfachte regelbasierte Logik
- **Output:** GWP, QP,ne und QNG-Status

### Tech Decision
- Django als Web-Framework
- HTML/CSS für die Benutzeroberfläche
- Python für die Logik
- Excel-Tool als fachliche Grundlage
- GitHub für Versionsverwaltung und Sprint-Planung

## Erste Datenstruktur
### Gebäudedaten
- Projektname
- QNG-Zielniveau
- Brutto-Grundfläche des Gebäudes
- Gebäudenutzfläche nach GEG
- Gesamte Nettoraumfläche
- Beheizte Nettoraumfläche
- Tiefgarage vorhanden

### Szenariodaten
- Energiestandard
- Bauweise
- Heizungsanlage
- Lüftungsanlage
- Photovoltaikfläche
- Batteriespeicher
- Fläche der Tiefgarage

### Ergebnisdaten
- Treibhauspotenzial (GWP)
- Nicht erneuerbarer Primärenergiebedarf (QP,ne)
- QNG-Status
- Hinweise / Kommentare

## Projektstruktur
```text
manage.py
qng_project/
qngapp/
qngapp/templates/qngapp/index.html
