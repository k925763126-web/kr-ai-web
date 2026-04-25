import streamlit as st
from groq import Groq
from streamlit_mic_recorder import speech_to_text

# --- 1. AYARLAR ---
GROQ_API_KEY = "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" 
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Kr AI Pro", page_icon="", layout="centered")

# --- 2. HAFIZA VE MOD SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Yan Menü (Sidebar)
with st.sidebar:
    st.title("⚙️ Ayarlar")
    # Mod Seçimi
    app_mode = st.radio("Bir Mod Seçin:", ["Normal Sohbet", "Resim Oluşturucu"])
    
    st.divider()
    
    # Sohbeti Temizle Butonu
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()

st.title(f" Kr AI ({app_mode})")

# Mesajları Ekranda Göster (Sadece Normal Modda)
if app_mode == "Normal Sohbet":
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 3. GİRİŞ ALANI ---
text_input = st.chat_input("Mesajınızı veya Resim Hayalinizi Yazın...")

# --- 4. İŞLEME MANTIĞI ---
if text_input:
    
    # --- MOD 1: NORMAL SOHBET ---
    if app_mode == "Normal Sohbet":
        st.session_state.messages.append({"role": "user", "content": text_input})
        with st.chat_message("user"):
            st.markdown(text_input)

        with st.chat_message("assistant"):
            try:
                messages_to_send = [{"role": "system", "content": "Sen Kr AI'sın. Samimi ve kısa cevap ver."}]
                for m in st.session_state.messages:
                    if m["content"].strip():
                        messages_to_send.append(m)

                completion = client.chat.completions.create(
                    messages=messages_to_send,
                    model="llama-3.1-8b-instant",
                )
                
                response_text = completion.choices[0].message.content
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Hata: {e}")

    # --- MOD 2: RESİM OLUŞTURUCU ---
    elif app_mode == "Resim Oluşturucu":
        with st.chat_message("user"):
            st.markdown(f"🖼️ Şunun resmini yap: {text_input}")
        
        with st.chat_message("assistant"):
            with st.spinner("Resminiz çiziliyor..."):
                # Ücretsiz resim oluşturma servisi (Pollinations)
                # Yazılan metni URL'ye uygun hale getiriyoruz
                prompt_url = text_input.replace(" ", "%20")
                image_url = f"https://image.pollinations.ai/prompt/{prompt_url}?width=1024&height=1024&nologo=true"
                
                st.image(image_url, caption=f"Kr AI Tasarımı: {text_input}")
                st.success("Resim Oluşturuldu!")
