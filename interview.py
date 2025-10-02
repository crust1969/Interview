import streamlit as st
from openai import OpenAI
from gtts import gTTS
from PIL import Image
from io import BytesIO

# -------------------------------
# OpenAI Client
# -------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------------
# Rollen + Avatare
# -------------------------------
avatars = {
    "Finance Director": {"image": "Finance.png"},
    "HR Director": {"image": "HR.png"},
    "IT Director": {"image": "IT.png"},
    "Marketing Director": {"image": "Marketing.png"}
}

st.title("💬 Avatar Discussion Demo (GPT + gTTS)")

# -------------------------------
# Moderator Input
# -------------------------------
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    for role, data in avatars.items():
        # ---------------------------
        # GPT-Response kurz & knackig
        # ---------------------------
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are {role}. Keep your answer short, witty and clear."},
                {"role": "user", "content": f"Discuss the topic: {topic}"}
            ]
        )
        reply = response.choices[0].message.content

        # ---------------------------
        # Layout: Avatar + Text
        # ---------------------------
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
        # gTTS: Text-to-Speech (kostenlos)
        # ---------------------------
        try:
            tts = gTTS(reply, lang='en')
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"Audio generation failed for {role}: {e}")
