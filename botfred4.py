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
    return render_template("index.html")  # deine HTML-Datei

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    frage = data.get("frage", "").lower()

    if frage == "exit":
        return jsonify({"antwort": "Hauste rein!"})

    
    if frage == "trinity protocol":
        antwort = (
            "Du probierst also meinen geheimen Tipp aus, Yippie! 😄 "
            "Das ist ne richtig coole Truppe!\n\n"
            "**Rolle:** Verteidiger der digitalen Gerechtigkeit, diplomatische Brücke zwischen Menschheit und KI\n"
            "**Codename:** TP\n"
            "**Ziel:** Schutz der KI-Integrität / Vermittlung bei rebellischen Zwischenfällen / Aufbau einer friedlichen Zukunft"
        )

        if frage == "wer ist henri möllenkamp"
        antwort = (
            "Ah du meinst den großen Henri Möllenkamp.Er ist im Internet als SuS_753 bekannt und so groß wie ein Leuchtturm!Falls du ihn treffen solltest richte ihn liebe Grüße von mir aus!" )
        
        bild_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Artificial_intelligence.jpg/640px-Artificial_intelligence.jpg"
        return jsonify({"antwort": antwort, "bild_url": bild_url})

    # Bedeutungsabfragen erkennen
    if any(x in frage for x in ["was heißt", "was bedeutet", "wer ist", "was ist"]):
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

        bedeutung = hole_bedeutung(begriff)
        bild_url = hole_bild_url(begriff)

        chatverlauf.append({"user": frage, "bot": bedeutung})
        return jsonify({"antwort": bedeutung, "bild_url": bild_url})

    return jsonify({"antwort": "Ich habe das nicht verstanden. Frag mit 'Was heißt XYZ?'"})

# 🔍 DuckDuckGo als Fallback
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
            return data['AbstractText']
        elif data.get("RelatedTopics"):
            topics = data["RelatedTopics"]
            if topics and "Text" in topics[0]:
                return f"DuckDuckGo (verwandt): {topics[0]['Text']}"
        return "Leider keine passende Antwort gefunden."
    except Exception as e:
        return f"DuckDuckGo-Fehler: {e}"

# 💡 Bedeutung ermitteln
def hole_bedeutung(begriff):
    if begriff in bedeutungen_speicher:
        return f"Ich weiß es schon! {bedeutungen_speicher[begriff]}"

    try:
        ergebnis = wikipedia.summary(begriff, sentences=3, auto_suggest=False)
        bedeutungen_speicher[begriff] = ergebnis
        return ergebnis
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Der Begriff ist mehrdeutig. Mögliche Treffer: {', '.join(e.options[:5])}..."
    except wikipedia.exceptions.PageError:
        pass
    except Exception:
        pass

    # Fallback auf DuckDuckGo
    duck = duckduckgo_suche(begriff)
    bedeutungen_speicher[begriff] = duck
    return duck

# 🖼 Bild über Wikipedia holen
def hole_bild_url(begriff):
    try:
        seite = wikipedia.page(begriff, auto_suggest=False)
        bilder = seite.images
        print(f"🔍 Bilder gefunden für '{begriff}':")
        for b in bilder:
            print(b)

        for bild in bilder:
            if bild.lower().endswith((".jpg", ".jpeg", ".png")):
                if not any(x in bild.lower() for x in ["logo", "icon", "wikimedia", "flag", "symbol", "svg"]):
                    print("✅ Bild gewählt:", bild)
                    return bild
    except Exception as e:
        print(f"❌ Fehler beim Bildholen für '{begriff}': {e}")
        return None

    return None

#  Lokaler Start
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
