import streamlit as st
from elevenlabs import ElevenLabs, VoiceSettings
from io import BytesIO

# Initialize ElevenLabs client
elevenlabs_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Define avatars with image + unique voice
avatars = {
    "Finance Director": {"img": "Finance.png", "voice": "pNInz6obpgDQGcFmaJgB"},
    "HR Director": {"img": "HR.png", "voice": "EXAVITQu4vr4xnSDxMaL"},
    "IT Director": {"img": "IT.png", "voice": "nPczCjzI2devNBz1zQrb"},
    "Marketing Director": {"img": "Marketing.png", "voice": "ODq5zmih8GrVes37Dizd"}
}

st.title("💬 Avatar Discussion Demo (Static Avatars + Different Voices)")

# Moderator input
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Loop through avatars for a single-turn discussion
    for role, info in avatars.items():
        try:
            # Generate GPT reply (replace with your GPT integration)
            reply = f"Here's a humorous take from {role} on {topic}."

            # Display avatar + text side by side
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(info["img"], width=120)
            with cols[1]:
                st.subheader(role)
                st.write(reply)

            # Convert GPT reply to TTS with unique voice
            audio = elevenlabs_client.generate(
                text=reply,
                voice=info["voice"],
                model="eleven_turbo_v2_5",  # Use the turbo model for low latency
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
                    speed=1.0
                )
            )

            # Play the generated audio
            st.audio(BytesIO(audio), format="audio/mp3")

        except Exception as e:
            st.error(f"Failed to generate speech for {role}: {e}")
