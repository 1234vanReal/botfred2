from flask import Flask, request, jsonify, render_template
import wikipedia
import requests
import os
import nltk
from nltk.tokenize import word_tokenize

# Nur beim ersten Start nötig:
nltk.download('punkt')

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
        bild_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Artificial_intelligence.jpg/640px-Artificial_intelligence.jpg"
        return jsonify({"antwort": antwort, "bild_url": bild_url})

    # 🧠 NLP-Fragetyp erkennen
    typ = frage_typ_bestimmen(frage)
    print(f"🧠 Fragetyp erkannt: {typ}")

    if typ in ["definition", "person", "erklärung"]:
        begriff = extrahiere_begriff(frage)
        bedeutung = hole_bedeutung(begriff)
        bild_url = hole_bild_url(begriff)

        chatverlauf.append({"user": frage, "bot": bedeutung})
        return jsonify({"antwort": bedeutung, "bild_url": bild_url})

    elif typ == "zeit":
        return jsonify({"antwort": "Ich versuche herauszufinden, wann das war... 🕰 (Feature kommt bald!)"})

    elif typ == "ort":
        return jsonify({"antwort": "Ich suche den Ort... 🌍 (Wird noch entwickelt!)"})

    return jsonify({"antwort": "Ich bin mir nicht sicher, was du meinst – kannst du es anders formulieren?"})


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
        for bild in bilder:
            if bild.lower().endswith((".jpg", ".jpeg", ".png")):
                if not any(x in bild.lower() for x in ["logo", "icon", "wikimedia", "flag", "symbol", "svg"]):
                    return bild
    except Exception as e:
        print(f"❌ Fehler beim Bildholen für '{begriff}': {e}")
        return None
    return None

# 🧠 Fragetyp-Bestimmung mit NLP
def frage_typ_bestimmen(frage):
    frage = frage.lower()
    tokens = word_tokenize(frage)

    if frage.startswith("was ist") or "was bedeutet" in frage or "was heißt" in frage:
        return "definition"
    elif frage.startswith("wer ist") or frage.startswith("wer war"):
        return "person"
    elif frage.startswith("wann"):
        return "zeit"
    elif frage.startswith("wo"):
        return "ort"
    elif frage.startswith("wie funktioniert") or frage.startswith("wie macht man"):
        return "erklärung"
    else:
        return "unbekannt"

# 🧠 Begriff automatisch aus der Frage extrahieren (simple Variante)
def extrahiere_begriff(frage):
    tokens = word_tokenize(frage)
    relevante_worte = [w for w in tokens if w.isalpha() and w.lower() not in ["was", "ist", "wer", "wie", "wann", "wo", "heißt", "bedeutet", "macht", "man", "die", "der", "das"]]
    if relevante_worte:
        return " ".join(relevante_worte[-2:])  # z. B. "künstliche intelligenz"
    return frage.strip()

#  Lokaler Start
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
