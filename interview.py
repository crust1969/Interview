import streamlit as st
from openai import OpenAI
import io

# Load API key
openai_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Define avatars with local image files
avatars = {
    "Finance Director": "avatars/finance.png",
    "HR Director": "avatars/hr.png",
    "IT Director": "avatars/it.png",
    "Marketing Director": "avatars/marketing.png"
}

st.title("💬 Avatar Discussion Demo (Static Avatars)")

# Moderator input
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    for role, img_path in avatars.items():
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
            st.image(img_path, width=120)
        with cols[1]:
            st.subheader(role)
            st.write(reply)

        # Generate TTS with OpenAI
        try:
            tts = openai_client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="alloy",  # change to desired voice
                input=reply
            )
            audio_bytes = tts.read()  # get mp3 bytes
            st.audio(io.BytesIO(audio_bytes), format="audio/mp3")
        except Exception as e:
            st.error(f"TTS failed: {e}")
