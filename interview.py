import streamlit as st
from openai import OpenAI
from io import BytesIO

# Initialize OpenAI client
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define avatars with image + unique voice
avatars = {
    "Finance Director": {"img": "Finance.png", "voice": "alloy"},
    "HR Director": {"img": "HR.png", "voice": "verse"},
    "IT Director": {"img": "IT.png", "voice": "aria"},
    "Marketing Director": {"img": "Marketing.png", "voice": "bella"}
}

st.title("💬 Avatar Discussion Demo (Static Avatars + Different Voices)")

# Moderator input
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Loop through avatars for a single-turn discussion
    for role, info in avatars.items():
        try:
            # Generate GPT reply
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"You are {role}. Respond in a humorous but realistic way."},
                    {"role": "user", "content": f"Discuss the topic: {topic}"}
                ]
            )
            reply = response.choices[0].message.content

            # Display avatar + text side by side
            cols = st.columns([1, 3])
            with cols[0]:
                st.image(info["img"], width=120)
            with cols[1]:
                st.subheader(role)
                st.write(reply)

            # Convert GPT reply to TTS with unique voice
            try:
                tts = openai_client.audio.speech.create(
                    model="gpt-4o-mini-tts",
                    voice=info["voice"],
                    input=reply
                )

                # Correct handling for bytes
                if hasattr(tts, "read"):
                    audio_bytes = tts.read()
                elif hasattr(tts, "getbuffer"):
                    audio_bytes = tts.getbuffer()
                else:
                    audio_bytes = tts  # fallback

                st.audio(BytesIO(audio_bytes), format="audio/mp3")

            except Exception as e:
                st.error(f"TTS failed for {role}: {e}")

        except Exception as e:
            st.error(f"GPT reply failed for {role}: {e}")
