# QNG-Check – Abschätzung der Gebäudeökobilanz

## Projektbeschreibung

Dieses Projekt ist ein Web-Tool zur vereinfachten Abschätzung der Gebäudeökobilanz nach dem **QNG-Standard (Qualitätssiegel Nachhaltiges Gebäude)**.

Ziel ist es, frühzeitig im Planungsprozess eine Einschätzung zu ermöglichen, ob ein Gebäude die Anforderungen an:

* Primärenergiebedarf (QP,ne)
* Treibhauspotenzial (GWP)

erfüllt.

---

## Ziel des Projekts

* Übertragung komplexer Excel-Berechnungen in ein verständliches Webtool
* Schnelle Szenarioanalyse ermöglichen
* Transparenz über Einflussfaktoren schaffen

---

## Funktionsumfang

### Gebäudedaten

* Eingabe von:

  * Nettogrundfläche (beheizt + Tiefgarage)
  * Energiebezugsfläche (Aₙ nach GEG)
  * Bauweise
  * Energiestandard

### Szenarioanalyse

* Auswahl von:

  * Heizsystem
  * Lüftungssystem
  * PV-Fläche
  * Batteriespeicher
  * QNG-Level (PLUS / PREMIUM)

### Ergebnis

* Berechnung von:

  * QP,ne
  * GWP
* Vergleich mit QNG-Grenzwerten
* Grafische Darstellung (Balkendiagramm)
* Aufschlüsselung nach Teilbereichen

---

## Testing (Sprint 3)

Erste Teststrategie wurde definiert:

* Vergleich mit Referenzwerten aus dem Excel-Tool
* Variation von Parametern (z. B. PV-Fläche)
* Überprüfung der Grenzwerte (QNG-PLUS / PREMIUM)
* Plausibilitätsprüfung der Ergebnisse
* Test der automatischen Flächenberechnung

---

## Technologien

* Python / Django
* HTML / CSS
* GitHub / GitHub Actions

---

## Projektstatus

| Bereich          | Status       |
| ---------------- | ------------ |
| GUI              | umgesetzt    |
| Datenstruktur    | umgesetzt    |
| Berechnungslogik | erster Stand |
| Testing          | gestartet    |
| Validierung      | ausstehend   |

---

## Nächste Schritte

* Validierung mit realen QNG-Daten
* Erweiterung der Berechnungslogik
* Verbesserung der Benutzerführung
* Aufbau automatisierter Tests


---

## Was ist QNG?

Das Qualitätssiegel Nachhaltiges Gebäude (QNG) ist ein staatlicher Standard zur Bewertung der Nachhaltigkeit von Gebäuden.

Bewertet werden unter anderem:

* Energieeffizienz
* CO₂-Emissionen
* Ressourceneinsatz
