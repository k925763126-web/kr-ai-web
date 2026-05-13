import streamlit as st
from groq import Groq

# --- 1. AYARLAR VE GÜVENLİK ---
# API Key'ini buraya yaz veya Streamlit Secrets kullan
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Kr AI Pro v3.1", layout="wide")

# --- 2. YAN MENÜ (PROFESYONEL KONTROL) ---
with st.sidebar:
    st.title("Kr AI Kontrol")
    st.info("V3.1")
    
    st.divider()
    
    # MOD SEÇİMİ
    app_mode = st.selectbox("🎯 İşlem Modu", ["Sohbet Modu", "Sanat Galerisi (Resim)"])
    
    # VERSİYON SEÇİMİ
    if app_mode == "Sohbet Modu":
        model_version = st.radio("🧠 Zeka Versiyonu", 
                                ["Kr AI Beta )", "Kr AI v3.3"])
        model_id = "llama-3.1-8b-instant" if "3.1" in model_version else "llama-3.3-70b-versatile"
    
    st.divider()
    
    # TEMİZLİK
    if st.button("🗑️ Geçmişi Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 3. HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. ANA EKRAN ---
st.title("Kr AI Pro")

if app_mode == "Sohbet Modu":
    # Sohbet Geçmişi
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Yazı Girişi
    if prompt := st.chat_input("Kr AI'ya bir soru sor..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                completion = client.chat.completions.create(
                    messages=[{"role": "system", "content": "Sen Kr AI Pro'sun. Çok zeki ve karizmatiksin."}] + st.session_state.messages,
                    model=model_id,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Sistem Hatası: {e}")

else:
    # RESİM MODU
    st.subheader("🎨 Hayalindekini Gerçeğe Dönüştür")
    img_prompt = st.text_area("Resim açıklamasını yaz (Örn: Geleceğin İstanbulu, siberpunk stil):")
    
    col1, col2 = st.columns(2)
    with col1:
        quality = st.select_slider("Görsel Kalitesi", options=["Normal", "HD", "Ultra HD"])
    with col2:
        aspect_ratio = st.selectbox("Görünüm Oranı", ["1:1 (Kare)", "16:9 (Geniş)", "9:16 (Dikey)"])

    if st.button("✨ Sanatı Oluştur", use_container_width=True):
        if img_prompt:
            with st.spinner("Kr AI çiziyor..."):
                # Gelişmiş prompt düzenleyici (kaliteyi artırmak için otomatik eklemeler yapar)
                final_prompt = f"{img_prompt}, high quality, 8k, detailed, masterpiece"
                encoded_prompt = final_prompt.replace(" ", "%20")
                
                # Resim URL Oluşturma
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
                
                st.image(image_url, use_column_width=True, caption="Kr AI tarafından üretildi")
                st.success("İşte başyapıtın!")
        else:
            st.warning("Lütfen bir açıklama yazın.")
