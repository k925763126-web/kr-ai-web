import streamlit as st
from groq import Groq
import time

# --- 1. GÜVENLİK VE API ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🔑 API Key Hatası!")
    st.stop()

# --- 2. SİSTEM AYARLARI ---
st.set_page_config(page_title="Kr AI Pro v7.0", page_icon="👑", layout="wide")

# Mühendislik Protokolü (Zeka Katmanı)
SYSTEM_PROMPT = """
Sen Kr AI Pro'sun. Sen bir yazılım ve mühendislik asistanısın. 
Cevaplarında şu kurallara uymalısın:
1. Kesin, teknik ve mantıklı cevaplar ver. 
2. Bir soruyu cevaplarken mutlaka konuyu tanımla, teknik detay ver ve pratik bir örnek ekle.
3. Asla halüsinasyon görme; bilmediğin bir şey varsa bunu dürüstçe söyle.
4. Karmaşık konuları bile bir mühendis ciddiyetiyle ve berraklığıyla açıkla.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# --- 3. MENÜ VE CSS ---
with st.sidebar:
    st.markdown("## 👑 Kr AI v7.0")
    app_mode = st.selectbox("İşlem Modu:", ["💬 Mühendislik Sohbeti", "🎨 Gelişmiş Görsel"])
    if "Görsel" in app_mode:
        art_style = st.selectbox("Görsel Stili:", ["Fotorealistik", "Siberpunk", "Mimari Plan", "Teknik Çizim"])
    st.divider()
    if st.button("🗑️ Hafızayı Temizle"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.generated_image = None
        st.rerun()

# --- 4. ANA EKRAN VE İSTATİSTİKLER ---
st.title(f"👑 {app_mode}")
tab1, tab2 = st.tabs(["⚡ İşlem", "📊 Sistem"])

with tab1:
    # SOHBET MODU
    if "Sohbet" in app_mode:
        for m in st.session_state.messages:
            if m["role"] != "system":
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])
        
        if prompt := st.chat_input("Mühendislik sorunu sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analiz ediliyor..."):
                    response = client.chat.completions.create(
                        messages=st.session_state.messages,
                        model="llama-3.3-70b-versatile",
                        temperature=0.2 # Çok daha mantıklı ve profesyonel
                    ).choices[0].message.content
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

    # RESİM MODU (Mantıklı Prompt Geliştirme)
    else:
        text = st.text_area("Ne çizmemi istersin? (Detaylandır)")
        if st.button("✨ Oluştur"):
            # Prompt'u otomatik olarak daha "teknik ve detaylı" hale getiriyoruz
            enhanced = f"{text}, high definition, {art_style} style, 8k resolution, cinematic lighting, professional"
            st.session_state.generated_image = f"https://image.pollinations.ai/prompt/{enhanced.replace(' ', '%20')}?seed={time.time()}"
        
        if st.session_state.generated_image:
            st.image(st.session_state.generated_image, use_container_width=True)

with tab2:
    st.metric("Model", "Llama 3.3 70B", "Pro Mod")
    st.info("Kr AI v7.0: Mühendislik odaklı, yüksek sadakatli cevaplar.")
