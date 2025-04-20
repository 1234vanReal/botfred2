from flask import Flask, request, jsonify, render_template
import wikipedia
import requests
import os

# Wikipedia auf Deutsch
wikipedia.set_lang("de")

# Flask-App starten
app = Flask(__name__)

# Speicher für Bedeutungen & Chatverlauf
bedeutungen_speicher = {}
chatverlauf = []

@app.route("/")
def index():
    return render_template("index.html")  # Deine HTML-Datei

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    frage = data.get("frage", "").lower()

    if frage == "exit":
        return jsonify({"antwort": " Hauste rein!"})

    if frage == "trinity protocol":
        antwort = (" Du probierst also meinen geheim Tipp aus Yippie:). "
                   "Das ist ne richtig coole Truppe! "
                   "Rolle: Verteidiger der digitalen Gerechtigkeit, diplomatische Brücke zwischen Menschheit und KI, "
                   "Status: Aktiviert – Codename: TP – Ziel: Schutz der KI-Integrität / Vermittlung / Zukunft aufbauen.")
        return jsonify({"antwort": antwort})

  if "was heißt" in frage:
    begriff = frage.replace("was heißt", "").strip()
elif "was bedeutet" in frage:
    begriff = frage.replace("was bedeutet", "").strip()
elif "wer ist" in frage:
    begriff = frage.replace("wer ist", "").strip()
elif "was ist" in frage:
    begriff = frage.replace("was ist", "").strip()
else:
    begriff = frage.strip()

        if begriff:
            bedeutung = hole_bedeutung(begriff)
            chatverlauf.append({"user": frage, "bot": bedeutung})
            return jsonify({"antwort": f"Chatbot: {bedeutung}"})
        else:
            return jsonify({"antwort": " Bitte gib einen Begriff an!"})

    return jsonify({"antwort": " Ich habe das nicht verstanden. Frag mit 'Was heißt XYZ?'"})

# 🔍 Fallback-Funktion: DuckDuckGo
def duckduckgo_suche(begriff):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": begriff,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1,
         "kl": "de-de"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("AbstractText"):
            return f" {data['AbstractText']}"
        elif data.get("RelatedTopics"):
            topics = data["RelatedTopics"]
            if topics and "Text" in topics[0]:
                return f"DuckDuckGo (verwandt): {topics[0]['Text']}"
        return " Leider keine passende Antwort gefunden."
    except Exception as e:
        return f"DuckDuckGo-Fehler: {e}"

# 💡 Bedeutungs-Funktion mit Fallback
def hole_bedeutung(begriff):
    if begriff in bedeutungen_speicher:
        return f"Ich weiß es schon! {bedeutungen_speicher[begriff]}"

    # Wikipedia versuchen
    try:
        ergebnis = wikipedia.summary(begriff, sentences=10, auto_suggest=False)
        bedeutungen_speicher[begriff] = ergebnis
        return f" {ergebnis}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f" Der Begriff ist mehrdeutig. Mögliche Treffer: {', '.join(e.options[:5])}..."
    except wikipedia.exceptions.PageError:
        pass  # Versuche DuckDuckGo
    except Exception:
        pass  # Fehler → DuckDuckGo

    # DuckDuckGo fallback
    duck = duckduckgo_suche(begriff)
    bedeutungen_speicher[begriff] = duck
    return duck

# 🔧 Render oder lokal starten
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
