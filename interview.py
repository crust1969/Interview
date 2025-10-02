import streamlit as st
import openai
import requests

# 👉 Setze deine Keys hier ein
OPENAI_API_KEY = "DEIN_OPENAI_KEY"
ELEVEN_API_KEY = "DEIN_ELEVENLABS_KEY"

openai.api_key = OPENAI_API_KEY

# Rollen-Definitionen
roles = {
    "Thomas (IT-Leiter)": "Technisch, nüchtern, redet über Schnittstellen und Sicherheit. Nerdig, manchmal zu detailliert.",
    "Sabine (HR-Leiterin)": "Empathisch, spricht über Mitarbeitende, Motivation und Weiterbildung. Blumig.",
    "Herr Krüger (Finanzchef)": "Kurz angebunden, fragt nach Kosten, ROI und Risiko. Trocken, streng, witzig.",
    "Markus (Vertriebsleiter)": "Begeistert, denkt an Umsatz und Kunden. Übertreibt gerne, will alles sofort verkaufen.",
    "Claudia (Marketing)": "Kreativ, voller Buzzwords, visionär. Oft wilde Ideen, manchmal abgehoben.",
    "Herr Meier (Produktion)": "Bodenständig, skeptisch, denkt an praktische Umsetzbarkeit."
}

# Stimmen (IDs aus ElevenLabs auswählen, z. B. 'Rachel', 'Adam' etc.)
voices = {
    "Thomas (IT-Leiter)": "voice_id_1",
    "Sabine (HR-Leiterin)": "voice_id_2",
    "Herr Krüger (Finanzchef)": "voice_id_3",
    "Markus (Vertriebsleiter)": "voice_id_4",
    "Claudia (Marketing)": "voice_id_5",
    "Herr Meier (Produktion)": "voice_id_6"
}

st.title("🎭 KI-Diskussionsrunde mit Avataren")
topic = st.text_input("Diskussionsthema eingeben:", "Soll unsere Firma KI im Kundenservice einsetzen?")

if st.button("Diskussion starten"):
    for role, style in roles.items():
        # Generiere Avatar-Text mit GPT
        prompt = f"Du bist {role}. {style}\nDiskussionsthema: {topic}\nAntwort:"
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # oder gpt-4o
            messages=[{"role": "system", "content": "Du bist ein Avatar in einer Diskussionsrunde."},
                      {"role": "user", "content": prompt}],
            max_tokens=180
        )
        text = response["choices"][0]["message"]["content"]
        
        st.subheader(role)
        st.write(text)

        # TTS mit ElevenLabs
        voice_id = voices[role]
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVEN_API_KEY
        }
        data = {"text": text, "voice_settings": {"stability": 0.6, "similarity_boost": 0.8}}
        audio = requests.post(url, headers=headers, json=data)

        # Abspielen
        audio_file = f"{role}.mp3"
        with open(audio_file, "wb") as f:
            f.write(audio.content)
        st.audio(audio_file, format="audio/mp3")
