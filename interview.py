import streamlit as st
from openai import OpenAI
from PIL import Image
from pathlib import Path

# -------------------------------
# OpenAI Client
# -------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------
# Rollen + Avatare + Voice
# -------------------------------
avatars = {
    "Finance Director": {"voice": "fable", "image": "Finance.png"},
    "HR Director": {"voice": "sage", "image": "HR.png"},
    "IT Director": {"voice": "verse", "image": "IT.png"},
    "Marketing Director": {"voice": "shimmer", "image": "Marketing.png"}
}

st.title("💬 Avatar Discussion Demo (Cloud-ready Audio)")

# -------------------------------
# Moderator Input
# -------------------------------
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    for role, data in avatars.items():
        # GPT-Response
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are {role}. Keep your answer short, witty and clear."},
                {"role": "user", "content": f"Discuss the topic: {topic}"}
            ]
        )
        reply = response.choices[0].message.content

        # Layout: Avatar + Text
        col1, col2 = st.columns([1, 4])
        with col1:
            try:
                st.image(Image.open(data["image"]), width=100)
            except FileNotFoundError:
                st.warning(f"⚠️ Image for {role} not found.")
        with col2:
            st.subheader(role)
            st.write(reply)

        # ---------------------------
        # TTS: MP3 speichern & abspielen
        # ---------------------------
        try:
            audio_response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=data["voice"],
                input=reply
            )

            mp3_filename = f"{role.replace(' ', '_')}_reply.mp3"
            # MP3 schreiben
            with open(mp3_filename, "wb") as f:
                f.write(audio_response.read())

            # Abspielen über Dateipfad (funktioniert zuverlässig in Streamlit Cloud)
            st.audio(mp3_filename, format="audio/mp3")

        except Exception as e:
            st.error(f"Audio generation failed for {role}: {e}")
