import streamlit as st
from groq import Groq
from streamlit_mic_recorder import speech_to_text

# Groq Beyin Bağlantısı
client = Groq(api_key="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")

st.set_page_config(page_title="Kr AI Pro", layout="centered")
st.title("👑 Kr AI ")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

voice = speech_to_text(language='tr', start_prompt="🎙️", stop_prompt="🛑", key='stt')
text = st.chat_input("Kr AI'ya yazın...")
query = voice if voice else text

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "Sen Kr AI'sın. Türkçe ve samimi cevap ver."}] + st.session_state.messages,
            model="llama3-8b-8192",
        )
        ans = chat_completion.choices[0].message.content
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
        # Tarayıcıdan ses çıkması için JavaScript
        st.components.v1.html(f"<script>var msg = new SpeechSynthesisUtterance('{ans.replace(chr(39), '')}'); msg.lang = 'tr-TR'; window.speechSynthesis.speak(msg);</script>", height=0)
