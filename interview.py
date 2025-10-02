import streamlit as st
from openai import OpenAI
import io
from PIL import Image

# OpenAI Client initialisieren
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Rollen mit Avatar + Voice definieren
avatars = {
    "Finance Director": {"voice": "fable", "image": "Finance.png"},
    "HR Director": {"voice": "sage", "image": "HR.png"},
    "IT Director": {"voice": "verse", "image": "IT.png"},
    "Marketing Director": {"voice": "shimmer", "image": "Marketing.png"}
}

st.title("💬 Avatar Discussion Demo")

# Eingabe Thema
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    for role, data in avatars.items():
        # GPT-Response kurz & knackig
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are {role}. Keep your answer short, witty and clear."},
                {"role": "user", "content": f"Discuss the topic: {topic}"}
            ]
        )
        reply = response.choices[0].message.content

        # Layout: Bild links, Text rechts
        col1, col2 = st.columns([1, 4])
        with col1:
            try:
                st.image(Image.open(data["image"]), width=100)
            except FileNotFoundError:
                st.warning(f"⚠️ Image for {role} not found.")
        with col2:
            st.subheader(role)
            st.write(reply)

        # TTS mit OpenAI (BytesIO verhindert StorageError)
        audio_response = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=data["voice"],
            input=reply
        )

        audio_bytes = io.BytesIO(audio_response.read())
        st.audio(audio_bytes, format="audio/mp3")
