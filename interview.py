import streamlit as st
from openai import OpenAI
from elevenlabs import ElevenLabs, Voice, VoiceSettings
from io import BytesIO

# -----------------------------
# Initialize API clients
# -----------------------------
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
elevenlabs_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# -----------------------------
# Define avatars
# -----------------------------
avatars = {
    "Finance Director": {"img": "Finance.png", "voice_id": "pNInz6obpgDQGcFmaJgB"},
    "HR Director": {"img": "HR.png", "voice_id": "EXAVITQu4vr4xnSDxMaL"},
    "IT Director": {"img": "IT.png", "voice_id": "nPczCjzI2devNBz1zQrb"},
    "Marketing Director": {"img": "Marketing.png", "voice_id": "ODq5zmih8GrVes37Dizd"}
}

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("💬 Avatar Discussion Demo (GPT + ElevenLabs TTS)")

topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Loop through avatars
    for role, info in avatars.items():
        try:
            # -----------------------------
            # Generate GPT reply
            # -----------------------------
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are {role}. Respond in a humorous but realistic way."},
                    {"role": "user", "content": f"Discuss the topic: {topic}"}
                ]
            )
            reply = response.choices[0].message.content

            # -----------------------------
            # Display avatar + text
            # -----------------------------
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(info["img"], width=120)
            with cols[1]:
                st.subheader(role)
                st.write(reply)

            # -----------------------------
            # Retrieve ElevenLabs voice by ID
            # -----------------------------
            voice = Voice.retrieve(info["voice_id"], client=elevenlabs_client)

            # -----------------------------
            # Convert GPT reply to TTS
            # -----------------------------
            audio = elevenlabs_client.text_to_speech.convert(
                text=reply,
                voice=voice,
                model="eleven_turbo_v2_5",
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
                    speed=1.0
                )
            )

            st.audio(BytesIO(audio), format="audio/mp3")

        except Exception as e:
            st.error(f"Error for {role}: {e}")
