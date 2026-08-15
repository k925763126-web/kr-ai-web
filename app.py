import streamlit as st
from groq import Groq
import time

# --- 1. GÜVENLİK VE API ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🔑 API Key Hatası! Lütfen Streamlit Secrets kısmına anahtarınızı ekleyin.")
    st.stop()

st.set_page_config(page_title="Kr AI Pro v9.0", page_icon="👑", layout="wide")

# --- 2. PREMIUM CSS ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #11141a; border-right: 1px solid #2d3139; }
    .stButton>button { width: 100%; border-radius: 12px; border: 1px solid #3e4451; background-color: #1e222b; color: #e2e8f0; }
    .stButton>button:hover { border-color: #ff4b4b; background-color: #ff4b4b; color: white; }
    .stTabs [data-baseweb="tab"] { background-color: #1e222b; color: #94a3b8; }
    .stTabs [aria-selected="true"] { background-color: #ff4b4b !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SİSTEM PROMPT VE HAFIZA ---
SYSTEM_PROMPT = "Sen Kr AI Pro'sun. Teknik, mantıklı, profesyonel bir mühendislik asistanısın. Karmaşık konuları basit ve teknik bir dille açıkla."

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# --- 4. YAN MENÜ ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>👑 Kr AI Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px;'>Altyapı: Groq Cloud v9.0</p>", unsafe_allow_html=True)
    
    app_mode = st.selectbox("İşlem Modu:", ["💬 Mühendislik Sohbeti", "🎨 Gelişmiş Görsel"])
    
    st.divider()
    
    # DOSYA EKLEME ÖZELLİĞİ
    st.markdown("### 📂 Dosya Analizi")
    uploaded_file = st.file_uploader("Bir dosya yükle (txt, py, md...)", type=["txt", "py", "md", "csv"])
    if uploaded_file is not None:
        if st.button("🚀 Dosyayı Sisteme İşle"):
            file_content = uploaded_file.read().decode("utf-8")
            st.session_state.messages.append({"role": "user", "content": f"Yüklenen dosya içeriği şöyledir:\n{file_content}"})
            st.success("Dosya içeriği hafızaya alındı!")

    st.divider()
    if st.button("🗑️ Hafızayı Temizle"):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.session_state.generated_image = None
        st.rerun()

# --- 5. ANA EKRAN ---
st.title(f"👑 {app_mode}")
tab1, tab2 = st.tabs(["⚡ İşlem Alanı", "📊 Sistem İstatistikleri"])

with tab1:
    if "Sohbet" in app_mode:
        for m in st.session_state.messages:
            if m["role"] != "system":
                with st.chat_message(m["role"]): st.markdown(m["content"])
        
        if prompt := st.chat_input("Sorunu yaz (Örn: Arduino nedir?)..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Kr AI analiz ediyor..."):
                    try:
                        # GÜNCELLENEN MODEL ALTYAPISI (Eski model kaldırıldığı için gpt-oss-120b'ye geçirildi)
                        resp = client.chat.completions.create(
                            messages=st.session_state.messages,
                            model="openai/gpt-oss-120b",
                            temperature=0.2
                        ).choices[0].message.content
                        st.markdown(resp)
                        st.session_state.messages.append({"role": "assistant", "content": resp})
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")

    else:
        text = st.text_area("Ne çizmemi istersin?")
        if st.button("✨ Oluştur"):
            enhanced = f"{text}, high definition, 8k, professional, cinematic"
            st.session_state.generated_image = f"https://image.pollinations.ai/prompt/{enhanced.replace(' ', '%20')}?seed={time.time()}"
        
        if st.session_state.generated_image:
            st.image(st.session_state.generated_image, use_container_width=True)

with tab2:
    st.metric("Model Altyapısı", "GPT OSS 120B", "Güncel & Aktif")
    st.info("Kr AI v9.0: Groq sistem güncellemelerine tamamen uyumlu hale getirildi.")
