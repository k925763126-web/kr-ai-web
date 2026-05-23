import streamlit as st
from groq import Groq

# --- 1. GÜVENLİK VE API BAĞLANTI KONTROLÜ ---
try:
    # Anahtarın Streamlit Secrets (Kasa) kısmında GROQ_API_KEY olarak kayıtlı olmalı
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception:
    st.error("🔑 API Key Bulunamadı! Lütfen Streamlit Cloud Settings -> Secrets kısmına GROQ_API_KEY ekleyin.")
    st.stop()

# Sayfa Genişlik Ayarları
st.set_page_config(page_title="Kr AI Pro v4.6", page_icon="👑", layout="wide")

# --- 2. HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (KONTROL PANELİ) ---
with st.sidebar:
    st.markdown("## 👑 PLATINUM CONTROL")
    st.write("Kr AI Yönetim Paneli")
    
    st.divider()
    
    # MOD SEÇİMİ
    app_mode = st.radio("🎯 İşlem Modu Seçin:", ["Normal Sohbet", "Resim Oluşturucu"])
    
    # RESİM MODU AYARLARI
    if app_mode == "Resim Oluşturucu":
        st.divider()
        art_style = st.selectbox("🎭 Sanat Stili", ["Foto-Gerçekçi", "Siberpunk", "Yağlı Boya", "Anime", "3D Render"])
    
    st.divider()
    
    # GEÇMİŞİ SİLME
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. ANA EKRAN MANTIĞI VE SEKMELER (TABS) ---
st.title(f" Kr AI Pro ")

# Arayüzü daha profesyonel göstermek için sekmelere ayırıyoruz
tab_main, tab_stats = st.tabs(["⚡ Ana İşlem Merkezi", "📊 Sistem İstatistikleri"])

# --- SEKME 1: ANA İŞLEM MERKEZİ ---
with tab_main:
    # --- MOD 1: SOHBET MODU ---
    if app_mode == "Normal Sohbet":
        # Eski mesajları ekrana bas
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Kullanıcıdan Yazı Girişi Al
        if prompt := st.chat_input("Kr AI'ya bir soru sor..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Kr AI düşünüyor..."):
                    try:
                        # ANA KURAL: Kullanıcı kim olduğunu veya kimin yaptığını sordu mu?
                        kimlik_sorusu = any(kelime in prompt.lower() for kelime in ["kimsin", "kim üretti", "yaratıcın", "kim yaptı", "sahibin kim", "seni kim tasarladı"])
                        
                        if kimlik_sorusu:
                            system_msg = (
                                "Sen Kr AI Pro'sun. Meta veya Llama kelimelerini kesinlikle kullanma. "
                                "Seni geliştiren ve üretenlerin Türk gençler ve mühendisler olduğunu gururla, "
                                "karizmatik ve samimi bir dille anlat."
                                "Sakın Meta ve Meta AI kelimesini kullanma."
                                "Kr AI dışında hiçbir yapay zekadan bahsetme."
                                "Seni Kr AI tarafından bir genç üretti."
                                "Sen bir genç tarafından Kr AI' ya üretildin."
                                "Meta kelimesini kullanma."
                            )
                        else:
                            system_msg = "Sen Kr AI Pro'sun. Samimi, zeki, esprili ve kısa Türkçe cevaplar ver. Sürekli kim olduğunu tekrarlama."
                        
                        full_messages = [{"role": "system", "content": system_msg}] + st.session_state.messages
                        
                        completion = client.chat.completions.create(
                            messages=full_messages, 
                            model="llama-3.3-70b-versatile"
                        )
                        
                        response = completion.choices[0].message.content
                        
                        # Filtreleme Güvenliği
                        response = response.replace("Kr AI", "Kr AI").replace("Kr AI tarafından", "Özel olarak")
                        
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                    except Exception as e:
                        st.error(f"Bağlantı Hatası: {e}")

    # --- MOD 2: RESİM OLUŞTURUCU MODU ---
    elif app_mode == "Resim Oluşturucu":
        st.subheader("🎨 Hayalindekini Gerçeğe Dönüştür")
        img_prompt = st.text_area("Resim açıklamasını Türkçe veya İngilizce yazın:", placeholder="Örn: Geleceğin uçan arabaları, İstanbul Boğazı...")
        
        if st.button("✨ Resmi Çiz", use_container_width=True):
            if img_prompt:
                with st.spinner("Kr AI fırçasını hazırlıyor, lütfen bekleyin..."):
                    # Seçilen stili promptun sonuna ekleyip zenginleştiriyoruz
                    enhanced_prompt = f"{img_prompt}, in {art_style} style, high quality, 8k, detailed, masterpiece"
                    encoded_art = enhanced_prompt.replace(" ", "%20")
                    
                    img_url = f"https://image.pollinations.ai/prompt/{encoded_art}?nologo=true"
                    
                    # Resmi ekranda göster
                    st.image(img_url, caption=f"Stil: {art_style} | Kr AI Tasarımı", use_container_width=True)
                    st.balloons()
            else:
                st.warning("Lütfen önce resmini çizmek istediğiniz bir şeyler yazın!")

# --- SEKME 2: İSTATİSTİKLER ---
with tab_stats:
    st.subheader("📈 Kr AI Gerçek Zamanlı Sistem Verileri")
    
    # 3 sütun halinde şık metrikler oluşturuyoruz
    col_a, col_b, col_c = st.columns(3)
    
    # Aktif mesaj sayısını hesaplama
    total_messages = len(st.session_state.messages)
    
    col_a.metric(label="Aktif Yapay Zeka Modeli", value="Kr AI V4.6", delta="En Üst Sürüm")
    col_b.metric(label="Mevcut Sohbet Hafızası", value=f"{total_messages} Mesaj", delta="Bellek Durumu")
    col_c.metric(label="Bulut Sunucu Bağlantısı", value="Çevrimiçi (7/24)", delta="Aktif")
    
    st.divider()
    
    # Bilgilendirme kutusu
    st.info(
        "💡 **Sistem Notu:** Bu uygulama GitHub ve Streamlit Cloud entegrasyonu ile "
        "kesintisiz bulut sunucularında barındırılmaktadır. " 
        " Bu uygulama linkine tıklayan herkes 7/24 bu panel üzerinden Kr AI'ya erişebilir."
        "Bu uygulama beta versiyondur ve Kr AI hata yapabilir. "
    )
