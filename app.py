import streamlit as st
from groq import Groq

# --- 1. GÜVENLİK VE API BAĞLANTI KONTROLÜ ---
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    st.error("🔑 API Key Bulunamadı! Lütfen Streamlit Cloud Settings -> Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

# Sayfa Ayarları
st.set_page_config(page_title="Kr AI Pro", page_icon="", layout="wide")

# --- 2. PREMIUM CSS DOKUNUŞLARI ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #11141a;
        border-right: 1px solid #2d3139;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #3e4451;
        background-color: #1e222b;
        color: #e2e8f0;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        border-color: #ff4b4b;
        background-color: #ff4b4b;
        color: white;
        box-shadow: 0px 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e222b;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DİNAMİK HAFIZA SİSTEMİ (SOHBET VE RESİM İÇİN) ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None
if "image_caption" not in st.session_state:
    st.session_state.image_caption = ""

# --- 4. YAN MENÜ (YENİ NESİL MODERNEŞTİRİLMİŞ PANEL) ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>👑 Kr AI Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Sürüm: Platinum v4.9<br>7/24 Kesintisiz Bulut Sistemi</p>", unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🎯 Çalışma Modu")
    app_mode = st.selectbox(
        "Uygulama işlevini değiştirin:",
        ["💬 Normal Sohbet", "🎨 Resim Oluşturucu"],
        label_visibility="collapsed"
    )
    
    if "🎨 Resim" in app_mode:
        st.markdown("---")
        st.markdown("### 🎭 Görsel Stil")
        art_style = st.selectbox(
            "Yapay zeka çizim tarzı:",
            ["Foto-Gerçekçi", "Siberpunk", "Yağlı Boya", "Anime", "3D Render"],
            label_visibility="collapsed"
        )
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Sistem Araçları")
    if st.button("🗑️ Hafızayı Sıfırla", use_container_width=True):
        st.session_state.messages = []
        st.session_state.generated_image = None
        st.session_state.image_caption = ""
        st.rerun()

# --- 5. ANA EKRAN MANTIĞI VE SEKMELER ---
st.markdown(f"<h2 style='color: white;'>{app_mode} Merkezi</h2>", unsafe_allow_html=True)

tab_main, tab_stats = st.tabs(["⚡ İşlem Alanı", "📊 Sistem İstatistikleri"])

# --- SEKME 1: ANA İŞLEM MERKEZİ ---
with tab_main:
    # --- MOD A: SOHBET MODU ---
    if "💬 Normal" in app_mode:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Kr AI'ya bir soru sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Kr AI düşünüyor..."):
                    try:
                        kimlik_sorusu = any(kelime in prompt.lower() for kelime in ["kimsin", "kim üretti", "yaratıcın", "kim yaptı", "sahibin kim", "seni kim tasarladı"])
                        
                        if kimlik_sorusu:
                            system_msg = (
                                "Sen Kr AI Pro'sun. Meta veya Llama kelimelerini kesinlikle kullanma. "
                                "Seni geliştiren ve üretenlerin Türk yazılımcılar ve mühendisler olduğunu gururla, "
                                "karizmatik ve samimi bir dille anlat."
                            )
                        else:
                            system_msg = "Sen Kr AI Pro'sun. Samimi, zeki, esprili ve kısa Türkçe cevaplar ver. Sürekli kim olduğunu tekrarlama."
                        
                        full_messages = [{"role": "system", "content": system_msg}] + st.session_state.messages
                        
                        completion = client.chat.completions.create(
                            messages=full_messages, 
                            model="llama-3.3-70b-versatile"
                        )
                        
                        response = completion.choices[0].message.content
                        response = response.replace("Meta AI", "Kr AI").replace("Meta tarafından", "Özel olarak")
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")

    # --- MOD B: RESİM OLUŞTURUCU MODU ---
    elif "🎨 Resim" in app_mode:
        st.write("Hayalindeki sahneyi betimle, Kr AI saniyeler içinde çizsin.")
        img_prompt = st.text_area("Resim açıklaması:", placeholder="Örn: Geleceğin uçan arabaları, İstanbul Boğazı...", label_visibility="collapsed")
        
        if st.button("✨ Resmi Çiz", use_container_width=True):
            if img_prompt:
                with st.spinner("Kr AI fırçasını hazırlıyor, lütfen bekleyin..."):
                    # Her basışta resmi yenilemek için zaman damgası (timestamp) yerine dinamik kelime yapısı kuruyoruz
                    import random
                    seed = random.randint(1, 999999)
                    
                    enhanced_prompt = f"{img_prompt}, in {art_style} style, high quality, 8k, detailed, masterpiece"
                    encoded_art = enhanced_prompt.replace(" ", "%20")
                    
                    # URL'ye seed ekleyerek tarayıcının resmi hafızada (cache) tutmasını engelliyoruz
                    img_url = f"https://image.pollinations.ai/prompt/{encoded_art}?seed={seed}&nologo=true"
                    
                    # Hafızaya kaydet
                    st.session_state.generated_image = img_url
                    st.session_state.image_caption = f"Stil: {art_style} | Kr AI Tasarımı"
                    st.balloons()
            else:
                st.warning("Lütfen önce resmini çizmek istediğiniz bir şeyler yazın!")
        
        # Eğer hafızada üretilmiş bir resim varsa ekranda sabit tut ve göster
        if st.session_state.generated_image:
            st.image(st.session_state.generated_image, caption=st.session_state.image_caption, use_container_width=True)

# --- SEKME 2: İSTATİSTİKLER ---
with tab_stats:
    st.subheader("📈 Gerçek Zamanlı Sistem Verileri")
    col_a, col_b, col_c = st.columns(3)
    total_messages = len(st.session_state.messages)
    
    col_a.metric(label="Aktif Yapay Zeka Modeli", value="Kr AI Pro v4.9", delta="En Üst Sürüm")
    col_b.metric(label="Mevcut Sohbet Hafızası", value=f"{total_messages} Mesaj", delta="Bellek Durumu")
    col_c.metric(label="Bulut Sunucu Bağlantısı", value="Çevrimiçi (7/24)", delta="Aktif")
    
    st.divider()
    st.info("💡 **Sistem Notu:** Bu uygulama kesintisiz bulut sunucularında barındırılmaktadır. Bilgisayarınız kapansa bile çalışır.")
