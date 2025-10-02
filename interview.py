import streamlit as st
from openai import OpenAI
from elevenlabs import ElevenLabs
import io
from pathlib import Path

# =======================
# Load API keys
# =======================
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
tts_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# =======================
# Define avatars (with ElevenLabs voice IDs and local images)
# =======================
avatars = {
    "Finance Director": {
        "voice_id": "pNInz6obpgDQGcFmaJgB",
        "image": "Finance.png"  # stored in main directory
    },
    "HR Director": {
        "voice_id": "EXAVITQu4vr4xnSDxMaL",
        "image": "HR.png"
    },
    "IT Director": {
        "voice_id": "ErXwobaYiN019PkySvjV",
        "image": "IT.png"
    },
    "Marketing Director": {
        "voice_id": "MF3mGyEYCl7XYWbV9V6O",
        "image": "Marketing.png"
    }
}

st.title("💬 Avatar Discussion Demo")

# =======================
# Moderator Input
# =======================
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Display avatars in grid
    cols_per_row = 2  # Number of avatars per row
    avatar_items = list(avatars.items())

    for i in range(0, len(avatar_items), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, (role, info) in zip(cols, avatar_items[i:i + cols_per_row]):
            # Display avatar image
            img_path = Path(info["image"])
            if img_path.exists():
                col.image(str(img_path), width=120)
            else:
                col.write("No image found")

            col.subheader(role)

            # Generate GPT response
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are {role}. Respond in a humorous but realistic way."},
                    {"role": "user", "content": f"Discuss the topic: {topic}"}
                ]
            )
            reply = response.choices[0].message.content
            col.write(reply)

            # Convert text to speech
            audio_stream = tts_client.text_to_speech.convert(
                voice_id=info["voice_id"],
                model_id="eleven_multilingual_v2",
                text=reply
            )
            audio_bytes = b"".join([chunk for chunk in audio_stream if chunk])
            col.audio(io.BytesIO(audio_bytes), format="audio/mp3")
