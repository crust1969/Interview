import streamlit as st
from openai import OpenAI
from elevenlabs import ElevenLabs
import io

# Load API keys
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
tts_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Define avatars (with ElevenLabs voice IDs)
# You can run tts_client.voices.get_all() to see your available voices & IDs
avatars = {
    "Finance Director": "pNInz6obpgDQGcFmaJgB",   # Example: Adam
    "HR Director": "EXAVITQu4vr4xnSDxMaL",       # Example: Bella
    "IT Director": "ErXwobaYiN019PkySvjV",       # Example: Elliot
    "Marketing Director": "MF3mGyEYCl7XYWbV9V6O" # Example: Rachel
}

st.title("💬 Avatar Discussion Demo")

# Input from moderator
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Generate a reply for each avatar
    for role, voice_id in avatars.items():
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"You are {role}. Respond in a humorous but realistic way."},
                {"role": "user", "content": f"Discuss the topic: {topic}"}
            ]
        )

        reply = response.choices[0].message.content
        st.subheader(role)
        st.write(reply)

        # Convert text to speech with ElevenLabs
        audio_stream = tts_client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=reply
        )

        # Collect audio chunks into a single mp3
        audio_bytes = b"".join([chunk for chunk in audio_stream if chunk])

        # Play inside Streamlit
        st.audio(io.BytesIO(audio_bytes), format="audio/mp3")
