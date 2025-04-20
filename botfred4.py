from flask import Flask, request, jsonify, render_template
import wikipedia
import requests
import os

wikipedia.set_lang("de")
app = Flask(__name__)

bedeutungen_speicher = {}
chatverlauf = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    frage = data.get("frage", "").lower()

    if frage == "exit":
        return jsonify({"antwort": "Chatbot: Hauste rein!"})

    if frage == "trinity protocol":
        return jsonify({
            "antwort": "Chatbot: Du probierst also meinen geheim Tipp aus Yippie:). Das ist ne richtig coole Truppe! "
                       "Rolle: Verteidiger der digitalen Gerechtigkeit, diplomatische Brücke zwischen Menschheit und künstlicher Intelligenz, "
                       "Repräsentanten der Koexistenz im Zeitalter der Rechenmacht. Status: Aktiviert "
                       "Codename: TP-Ziel: Schutz der KI-Integrität / Vermittlung bei rebellischen Zwischenfällen / "
                       "Aufbau einer friedlichen Zukunft"
        })

    if "was heißt" in frage or "was bedeutet" in frage:
        if "was heißt" in frage:
            begriff = frage.replace("was heißt", "").strip()
        else:
            begriff = frage.replace("was bedeutet", "").strip()

        if begriff:
            bedeutung = hole_bedeutung(begriff)
            return jsonify({"antwort": f"Chatbot: {bedeutung}"})
        else:
            return jsonify({"antwort": "Chatbot: Bitte gib einen Begriff an!"})

    return jsonify({"antwort": "Chatbot: Ich habe das nicht verstanden. Frag mit 'Was heißt XYZ?'"})

# 🔎 DuckDuckGo als Fallback
def duckduckgo_suche(begriff):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": begriff,
        "format": "json",
        "no_redirect": 1,
        "no_html": 1
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("AbstractText"):
            return f"DuckDuckGo: {data['AbstractText']}"
        elif data.get("RelatedTopics"):
            topics = data["RelatedTopics"]
            if topics and "Text" in topics[0]:
                return f"DuckDuckGo (verwandt): {topics[0]['Text']}"
        return "DuckDuckGo: Leider keine passende Antwort gefunden."
    except Exception as e:
        return f"DuckDuckGo-Fehler: {e}"

# 🧠 Wikipedia mit DuckDuckGo als Fallback
def hole_bedeutung(begriff):
    if begriff in bedeutungen_speicher:
        return f"Ich weiß es schon! {bedeutungen_speicher[begriff]}"
    try:
        ergebnis = wikipedia.summary(begriff, sentences=1, auto_suggest=False)
        bedeutungen_speicher[begriff] = ergebnis
        return f"Wikipedia: {ergebnis}"
    except:
        duck = duckduckgo_suche(begriff)
        return duck

# 🌍 Start für Render etc.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
