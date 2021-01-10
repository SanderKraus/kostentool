# Flask-Kostentool-RWTH

Hier habt ihr ein Starter-Template, um euer Projekt zu bootstrappen.

## Docker

Das Docker-Image bauen:

```sh
docker build -t flask_app .
```

Den Container starten:

```sh
docker run -p 80:80 flask_app
```

Seite läuft auf http://localhost:80

## Installation

### Erster Schritt

Erstellen eines Virtualenvironment im Projektordner.

### Zweiter Schritt

Installiere alle packages mit pip:

```sh
pip install -r requirements.txt
```

### (optionaler) Zweiter Schritt

Installiere alle packages, Linter und Autoformatter, passend zu den .vscode-Settings:

```sh
pip install -r requirements-dev.txt
```

### Dritter Schritt

Vor dem ersten Starten:

Erstellt eine <strong>app.db</strong> im Projektordner und dann =>

```sh
flask db init
flask db migrate -m "inital migration"
flask db upgrade
```

Bei jeder Änderung der Datenbank-Modelle:

```sh
flask db migrate
flask db upgrade
```

## App starten

Um die Flask-App zu starten:

```sh
flask run
```

## TODOS

1. "Passwort vergessen" einrichten
2. Zugang Admin-Seite nur für Superuser
3. Oder Rollensystem und Nutzer können ihre eigenen Daten in der Admin-View verändern
4. Business-Logik implentieren
