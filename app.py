import streamlit as st
from groq import Groq

# --- 1. CONFIG & AUTH (SECRETS KONTROLÜ) ---
try:
    # Anahtar artık kodun içinde değil, Streamlit Secrets kasasında güvende!
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    st.error("🔑 API Key Bulunamadı! Lütfen Streamlit Cloud Settings -> Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

st.set_page_config(
    page_title="Kr AI Pro v4.2", 
    page_icon="", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #ff4b4b; background-color: transparent; color: white; }
    .stButton>button:hover { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.title("Kr Kontrol")
    
    st.subheader("🤖 Zeka Merkezi")
    model_choice = st.selectbox("Model Seçimi", ["Kr AI Beta", "Kr AI V4.2"])
    model_id = "llama-3.3-70b-versatile" if "3.3" in model_choice else "llama-3.1-8b-instant"
    
    st.subheader("🎨 Görsel Stüdyo")
    art_style = st.selectbox("Sanat Stili", ["Foto-Gerçekçi", "Siberpunk", "Yağlı Boya", "Anime", "3D Render", "Sürrealist"])
    
    st.divider()
    if st.button("🗑️ Tüm Belleği Boşalt"):
        st.session_state.messages = []
        st.rerun()

# --- 4. TABS ---
tab1, tab2, tab3 = st.tabs(["💬 Akıllı Sohbet", "🖼️ Sanat Stüdyosu", "📊 Sistem Durumu"])

# --- TAB 1: SOHBET (KİMLİK KORUMALI) ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Kr AI'ya Yaz..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Kr AI düşünüyor..."):
                try:
                    # KESİN KİMLİK TANIMLAMASI (Meta AI demesini engelleyen mutlak komut)
                    system_msg = (
                        "Sen Meta, Llama veya başka bir şirketin ürünü DEĞİLSİN. "
                        "Senin adın Kr AI Pro. Seni geliştiren ve üreten kişi tamamen Türk yazılımcılardır. "
                        "Kim üretti veya kimsin sorularına kesinlikle 'Ben Kr AI Pro'yum, özel olarak geliştirildim' "
                        "şeklinde karizmatik, samimi ve Türkçe cevaplar vereceksin. Meta AI kelimesini asla ağzına almayacaksın."
                    )
                    
                    full_messages = [{"role": "system", "content": system_msg}] + st.session_state.messages
                    
                    completion = client.chat.completions.create(messages=full_messages, model=model_id)
                    response = completion.choices[0].message.content
                    
                    # Güvenlik Filtresi: Eğer model her şeye rağmen Meta kelimesini sızdırırsa kod seviyesinde engelliyoruz
                    response = response.replace("Meta AI", "Kr AI").replace("Meta tarafından", "Özel olarak")
                    
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    st.error(f"Bağlantı Hatası: {e}")

# --- TAB 2: SANAT STÜDYOSU ---
with tab2:
    st.header("🎭 Yapay Zeka Sanat Merkezi")
    c1, c2 = st.columns([2, 1])
    with c1:
        user_art_prompt = st.text_area("Hayalindeki sahneyi betimle...")
    with c2:
        seed = st.number_input("Rastgelelik (Seed)", value=42)

    if st.button("🚀 Sanatı Başlat"):
        if user_art_prompt:
            with st.spinner("Kr AI fırçasını hazırlıyor..."):
                enhanced_prompt = f"{user_art_prompt}, in {art_style} style, cinematic lighting, ultra detailed, 8k, masterpiece"
                encoded_art = enhanced_prompt.replace(" ", "%20")
                img_url = f"https://image.pollinations.ai/prompt/{encoded_art}?seed={seed}&nologo=true"
                st.image(img_url, caption=f"Stil: {art_style} | Mod: Pro v4.2", use_column_width=True)
                st.balloons()
        else:
            st.warning("Lütfen bir açıklama girin!")

# --- TAB 3: İSTATİSTİKLER ---
with tab3:
    st.header("📈 Sistem Durumu")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Aktif Yapay Zeka", "Kr AI Pro")
    col_b.metric("API Güvenliği", "Kr AI Korumalı",)
    col_c.metric("Sunucu Durumu", "Çevrimiçi", "7/24")
