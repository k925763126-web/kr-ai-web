import streamlit as st
from groq import Groq
from streamlit_mic_recorder import speech_to_text

# 1. BAĞLANTI (Anahtarını Secrets kısmına eklediysen st.secrets["GROQ_API_KEY"] yapabilirsin)
# Eğer doğrudan yazacaksan:
client = Groq(api_key="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")

st.set_page_config(page_title="Kr AI Pro", page_icon="👑")
st.title("👑 Kr AI Canlı")

# Hafıza kontrolü
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları Ekranda Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- GİRİŞ ALANI ---
voice_input = speech_to_text(language='tr', start_prompt="🎙️", stop_prompt="🛑", key='stt')
text_input = st.chat_input("Kr AI'ya yazın...")

# Hangi giriş doluysa onu seç, ikisi de boşsa None döndür
user_query = None
if voice_input and voice_input.strip():
    user_query = voice_input
elif text_input and text_input.strip():
    user_query = text_input

# --- İŞLEME VE YANIT ---
if user_query:
    # 1. Kullanıcı mesajını hafızaya ekle
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # 2. Yapay zekadan yanıt al
    with st.chat_message("assistant"):
        try:
            # Sadece dolu mesajları filtreleyerek gönderiyoruz (Hata önleyici)
            valid_messages = [{"role": "system", "content": "Sen Kr AI'sın. Türkçe ve samimi cevap ver."}]
            for m in st.session_state.messages:
                if m["content"]: # Boş içerikleri atla
                    valid_messages.append(m)

            completion = client.chat.completions.create(
                messages=valid_messages,
                model="llama3-8b-8192",
            )
            
            ans = completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
            
            # Tarayıcıdan seslendirme
            st.components.v1.html(f"""
                <script>
                var msg = new SpeechSynthesisUtterance('{ans.replace("'", "")}');
                msg.lang = 'tr-TR';
                window.speechSynthesis.speak(msg);
                </script>
            """, height=0)

        except Exception as e:
            st.error(f"Groq Hatası: {e}")
