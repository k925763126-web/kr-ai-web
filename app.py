import streamlit as st
from groq import Groq

# --- 1. CONFIG & AUTH ---
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(
    page_title="Kr AI Platinum v4.0", 
    page_icon="", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (ESTETİK DOKUNUŞ) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 20px; border: 1px solid #ff4b4b; background-color: transparent; color: white; }
    .stButton>button:hover { background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & SETTINGS ---
with st.sidebar:
    st.image("https://img.icons8.com/fluent/100/000000/crown.png", width=80)
    st.title("PLATINUM CONTROL")
    
    st.subheader("🤖 Zeka Merkezi")
    model_choice = st.selectbox("Model Seçimi", 
                               ["Kr AI Beta", "Kr AI V 4.0"])
    model_id = "llama-3.3-70b-versatile" if "3.3" in model_choice else "llama-3.1-8b-instant"
    
    st.subheader("🎨 Görsel Stüdyo Ayarları")
    art_style = st.selectbox("Sanat Stili", 
                            ["Foto-Gerçekçi", "Siberpunk", "Yağlı Boya", "Anime", "3D Render", "Sürrealist"])
    
    st.divider()
    if st.button("🗑️ Tüm Belleği Boşalt"):
        st.session_state.messages = []
        st.rerun()

# --- 4. MAIN INTERFACE (TABS) ---
tab1, tab2, tab3 = st.tabs([" Akıllı Sohbet", " Sanat Stüdyosu", " İstatistikler"])

# --- TAB 1: SOHBET ---
with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Kr AI'ya Yaz.."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                # Güçlendirilmiş System Prompt
                system_msg = "Sen Kr AI Platinum'sun. Kullanıcıya en derin analizleri sunan, karizmatik ve otoriter bir yapay zekasın."
                full_messages = [{"role": "system", "content": system_msg}] + st.session_state.messages
                
                completion = client.chat.completions.create(messages=full_messages, model=model_id)
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")

# --- TAB 2: SANAT STÜDYOSU ---
with tab2:
    st.header("Yapay Zeka Sanat Merkezi")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        user_art_prompt = st.text_area("Hayalindeki sahneyi betimle...", placeholder="Örn: Mars üzerinde lüks bir malikane, gün batımı...")
    with c2:
        res = st.selectbox("Çözünürlük", ["1024x1024 (Kare)", "1280x720 (Geniş)"])
        seed = st.number_input("Rastgelelik (Seed)", value=42)

    if st.button("🚀 Sanatı Başlat"):
        if user_art_prompt:
            with st.spinner("Kr AI fırçasını hazırlıyor..."):
                # Stil ekleme mantığı
                enhanced_prompt = f"{user_art_prompt}, in {art_style} style, cinematic lighting, ultra detailed, 8k, masterpiece"
                encoded_art = enhanced_prompt.replace(" ", "%20")
                img_url = f"https://image.pollinations.ai/prompt/{encoded_art}?seed={seed}&nologo=true"
                
                st.image(img_url, caption=f"Stil: {art_style} | Mod: Platinum v4.0", use_column_width=True)
                st.balloons()
        else:
            st.warning("Lütfen bir açıklama girin!")

# --- TAB 3: İSTATİSTİKLER ---
with tab3:
    st.header(" Sistem Durumu")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Aktif Model", "Kr AI V4.0", "Güçlü")
    col_b.metric("Sunucu Durumu", "Çevrimiçi", "7/24")
    col_c.metric("Yanıt Süresi", "0.4s", "Optimal")
    
    st.info("Bu uygulama GitHub üzerinden Streamlit Cloud ile çalışmaktadır. Bilgisayar kapalı olsa bile bu link üzerinden erişilebilir.")
