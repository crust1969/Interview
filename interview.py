import streamlit as st
from openai import OpenAI
import io
from pathlib import Path

# =======================
# Load API key
# =======================
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# =======================
# Define avatars (voices + local images)
# =======================
avatars = {
    "Finance Director": {
        "voice": "fable",   # weibliche Stimme
        "image": "Finance.png"
    },
    "HR Director": {
        "voice": "alloy",  # neutrale Stimme
        "image": "HR.png"
    },
    "IT Director": {
        "voice": "verse",  # männliche Stimme
        "image": "IT.png"
    },
    "Marketing Director": {
        "voice": "sage",   # weibliche Stimme
        "image": "Marketing.png"
    }
}

st.title("💬 Avatar Discussion Demo (OpenAI TTS)")

# =======================
# Moderator Input
# =======================
topic = st.text_input("Enter a discussion topic:")

if st.button("Start Discussion") and topic:
    st.write(f"**Moderator:** Today’s topic is: {topic}")

    # Display avatars in grid
    cols_per_row = 2
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

            # Generate GPT response (short and crisp)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are {role}. Respond to the topic in a short, "
                            "crisp, humorous, and realistic way. Limit to 2–3 sentences."
                        )
                    },
                    {"role": "user", "content": f"Discuss the topic: {topic}"}
                ]
            )
            reply = response.choices[0].message.content
            col.write(reply)

            # Convert text to speech with OpenAI
            audio_response = client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice=info["voice"],
                input=reply
            )

            # Audio zurückspielen
            audio_bytes = audio_response.read()
            col.audio(io.BytesIO(audio_bytes), format="audio/mp3")
