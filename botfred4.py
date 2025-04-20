import wikipedia
from flask import Flask, request, jsonify
wikipedia.set_lang("de")
app = Flask(__name__)

# Ein Dictionary zum Speichern der Begriffe und ihrer Bedeutungen
bedeutungen_speicher = {}

# Funktion, die die Bedeutung des Begriffs sucht
def hole_bedeutung(begriff):
    # Wenn der Begriff schon gespeichert ist, geben wir die gespeicherte Bedeutung zurück
    if begriff in bedeutungen_speicher:
        return f"Ich weiß es schon! Hier ist die gespeicherte Bedeutung: {bedeutungen_speicher[begriff]}"
    
    try:
        # Suchen der Zusammenfassung des Begriffs
        ergebnis = wikipedia.summary(begriff, sentences=1, auto_suggest=False)
        # Speichern der Bedeutung im Speicher
        bedeutungen_speicher[begriff] = ergebnis
        return ergebnis
    except wikipedia.exceptions.DisambiguationError as e:
        # Falls der Begriff mehrdeutig ist, gibt es eine Liste von möglichen Ergebnissen
        return f"Es gibt mehrere Ergebnisse für '{begriff}': {e.options}"
    except wikipedia.exceptions.HTTPError:
        return "Es gab ein Problem beim Abrufen der Daten von Wikipedia."
    except wikipedia.exceptions.RedirectError:
        return "Der Begriff führt auf eine Weiterleitung, die nicht verarbeitet werden kann."
    except wikipedia.exceptions.TimeoutError:
        return "Die Anfrage hat zu lange gedauert, bitte versuche es später nochmal."
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {e}"

# Hauptfunktion für das Chatbot-Programm
def botfred():
    print(" Moin! Bist du auch wieder am Start oder was?")
    print("Frag mich gerne nach bedeutungen von Sachen!")
    print("Ich brauch manchmal ein bisschen um Daten aus meinem Speicher zu holen also hab bitte Verständniss.")
    print("Psst als kleinen Tipp: Gib mal trinity protocol ein:)")
    print("(Tipp: 'exit' wenn du mich loswerden möchtest!)")

    # Benutzereingabe
    while True:
        user_input = input("Du: ").strip().lower()

        # Beenden des Programms
        if user_input == "exit":
            print("Chatbot: Hauste rein!")
            break
        if user_input== "trinity protocol":
            print("Chatbot:Du probierst also meinen geheim Tipp aus Yippie:).Das ist ne richtig coole Truppe!Rolle:Verteidiger der digitalen Gerechtigkeit, diplomatische Brücke zwischen Menschheit und künstlicher Intelligenz, Repräsentanten der Koexistenz im Zeitalter der Rechenmacht.Status: AktiviertCodename: TP-Ziel:Schutz der KI-Integrität/Vermittlung bei rebellischen Zwischenfällen/Aufbau einer friedlichen Zukunft")

        # Überprüfen, ob die Eingabe "was heißt" oder "was bedeutet" enthält
        if "was heißt" in user_input or "was bedeutet" in user_input:
            # Extrahieren des Begriffs (nach "was heißt" oder "was bedeutet")
            if "was heißt" in user_input:
                begriff = user_input.replace("was heißt", "").strip()
            elif "was bedeutet" in user_input:
                begriff = user_input.replace("was bedeutet", "").strip()

            if begriff:
                print(f"Chatbot: Ich weiß es noch nicht. Ich suche online nach der Bedeutung von '{begriff}'...")
                bedeutung = hole_bedeutung(begriff)
                print(f"Chatbot: {bedeutung}")
            else:
                print("Chatbot: Bitte gib einen Begriff an, nach dem ich suchen soll.")
        else:
            print("Chatbot: Ich habe das nicht verstanden. Versuche es mit 'Was heißt XYZ?' oder 'Was bedeutet XYZ?'.")

# Start des Chatbots
if __name__ == "__main__":
    botfred()  