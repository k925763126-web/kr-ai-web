import streamlit as st
from groq import Groq
from streamlit_mic_recorder import speech_to_text

# --- 1. AYARLAR ---
# Buraya Groq sitesinden aldığın güncel gsk_... anahtarını yaz
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Kr AI Pro", page_icon="👑", layout="centered")

# --- 2. HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("👑 Kr AI Pro")
st.caption("7/24 Aktif | Llama 3.1 Bulut Sürümü")

# Eski mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. GİRİŞ ALANI (SES VE YAZI) ---
col1, col2 = st.columns([1, 5])
with col1:
    voice_input = speech_to_text(language='tr', start_prompt="🎙️", stop_prompt="🛑", key='stt')
with col2:
    text_input = st.chat_input("Bir şeyler yazın...")

# Giriş kontrolü
user_query = None
if voice_input and voice_input.strip():
    user_query = voice_input
elif text_input and text_input.strip():
    user_query = text_input

# --- 4. YANIT VE SESLENDİRME ---
if user_query:
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Yapay zekadan yanıt al
    with st.chat_message("assistant"):
        try:
            # Boş mesaj gitmemesi için filtreleme yapıyoruz
            messages_to_send = [{"role": "system", "content": "Sen Kr AI'sın. Samimi, zeki ve kısa Türkçe cevaplar ver."}]
            for m in st.session_state.messages:
                if m["content"].strip():
                    messages_to_send.append(m)

            # GÜNCEL MODEL: llama-3.1-8b-instant
            completion = client.chat.completions.create(
                messages=messages_to_send,
                model="llama-3.1-8b-instant",
                temperature=0.7
            )
            
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            
            # TARAYICI SESİ (JavaScript)
            # Sitenin açıldığı cihazın (telefon/PC) hoparlörünü kullanır
            js_code = f"""
                <script>
                window.speechSynthesis.cancel(); // Önceki sesi durdur
                var msg = new SpeechSynthesisUtterance('{response_text.replace("'", "").replace('"', '')}');
                msg.lang = 'tr-TR';
                msg.rate = 1.1; // Biraz daha hızlı ve doğal konuşma
                window.speechSynthesis.speak(msg);
                </script>
            """
            st.components.v1.html(js_code, height=0)

        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
