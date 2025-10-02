import streamlit as st
from openai import OpenAI
from elevenlabs import ElevenLabs, play

# Load API keys
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
tts_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])

# Define avatars
avatars = {
    "Finance Director": "Adam",
    "HR Director": "Rachel",
    "IT Director": "Elliot",
    "Marketing Director": "Bella"
}

st.title("💬 Avatar Discussion Demo")

# Input from moderator
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Generate a reply for each avatar
    for role, voice in avatars.items():
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

        # Convert text to speech using ElevenLabs
        audio = tts_client.generate(text=reply, voice=voice, model="eleven_multilingual_v2")

        st.audio(audio, format="audio/mp3")
