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
# Session State: History
# -------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -------------------------------
# Moderator Input
# -------------------------------
topic = st.text_input("Moderator: Enter a discussion topic or follow-up question:")

# -------------------------------
# Start or Continue Discussion
# -------------------------------
if st.button("Ask Question") and topic:
    st.session_state.history.append({"role": "Moderator", "content": topic})

    st.markdown(f"### 🗣️ Moderator:")
    st.write(topic)

    # Each avatar responds
    for role, data in avatars.items():
        # ---------------------------
        # Build conversation context (last 6 messages)
        # ---------------------------
        messages = [{"role": "system", "content": f"You are {role}. Keep your answers short, witty, and clear."}]
        for msg in st.session_state.history[-6:]:
            if msg["role"] == "Moderator":
                messages.append({"role": "user", "content": f"{msg['role']}: {msg['content']}"})
            else:
                messages.append({"role": "assistant", "content": f"{msg['role']}: {msg['content']}"})

        # Add new moderator question
        messages.append({"role": "user", "content": f"The moderator asks: {topic}"})

        # ---------------------------
        # GPT generates reply
        # ---------------------------
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        reply = response.choices[0].message.content

        # Store in history
        st.session_state.history.append({"role": role, "content": reply})

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
        # gTTS: Text-to-Speech
        # ---------------------------
        try:
            tts = gTTS(reply, lang='en')
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"Audio generation failed for {role}: {e}")

# -------------------------------
# Show conversation history
# -------------------------------
if st.session_state.history:
    st.divider()
    st.subheader("🧭 Discussion History")
    for msg in st.session_state.history:
        st.markdown(f"**{msg['role']}:** {msg['content']}")
