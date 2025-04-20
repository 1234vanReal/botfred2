from flask import Flask, request, jsonify, render_template
import wikipedia

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
        return jsonify({"antwort": "Chatbot: Du probierst also meinen geheim Tipp aus Yippie:).Das ist ne richtig coole Truppe!Rolle:Verteidiger der digitalen Gerechtigkeit, diplomatische Brücke zwischen Menschheit und künstlicher Intelligenz, Repräsentanten der Koexistenz im Zeitalter der Rechenmacht.Status: AktiviertCodename: TP-Ziel:Schutz der KI-Integrität/Vermittlung bei rebellischen Zwischenfällen/Aufbau einer friedlichen Zukunft"})

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

def hole_bedeutung(begriff):
    if begriff in bedeutungen_speicher:
        return f"Ich weiß es schon! {bedeutungen_speicher[begriff]}"
    try:
        ergebnis = wikipedia.summary(begriff, sentences=1, auto_suggest=False)
        bedeutungen_speicher[begriff] = ergebnis
        return ergebnis
    except Exception as e:
        return f"Fehler: {e}"
        
          

    return jsonify({"antwort": antwort, "verlauf": chatverlauf})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
