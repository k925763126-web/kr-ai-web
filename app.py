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
st.set_page_config(page_title="Kr AI Pro v4.2", page_icon="", layout="centered")

# --- 2. HAFIZA SİSTEMİ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. YAN MENÜ (KONTROL PANELİ) ---
with st.sidebar:
    st.image("", width=60)
    st.title(" Kr AI Kontrol")
    
    st.divider()
    
    # MOD SEÇİMİ (Uygulamanın ne yapacağını buradan seçiyoruz)
    app_mode = st.radio("🎯 İşlem Modu Seçin:", ["Normal Sohbet", "Resim Oluşturucu"])
    
    # RESİM MODU AYARLARI (Sadece Resim seçildiğinde görünür)
    if app_mode == "Resim Oluşturucu":
        st.divider()
        art_style = st.selectbox("🎭 Sanat Stili", ["Foto-Gerçekçi", "Siberpunk", "Yağlı Boya", "Anime", "3D Render"])
    
    st.divider()
    
    # GEÇMİŞİ SİLME
    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- 4. ANA EKRAN MANTIĞI ---
st.title(f" Kr AI ({app_mode})")

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
                        )
                    else:
                        # Normal günlük sorularda sadece samimi bir asistan gibi davranacak
                        system_msg = "Sen Kr AI Pro'sun. Samimi, zeki, esprili ve kısa Türkçe cevaplar ver. Sürekli kim olduğunu tekrarlama."
                    
                    full_messages = [{"role": "system", "content": system_msg}] + st.session_state.messages
                    
                    # Dünyanın en zeki açık kaynak modellerinden biri olan Llama 3.3-70b'yi çağırıyoruz
                    completion = client.chat.completions.create(
                        messages=full_messages, 
                        model="llama-3.3-70b-versatile"
                    )
                    
                    response = completion.choices[0].message.content
                    
                    # Filtreleme Güvenliği (Kelime kaçarsa yakalamak için)
                    response = response.replace("Meta AI", "Kr AI").replace("Meta tarafından", "Özel olarak")
                    
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
                
                # Ücretsiz ve sınırsız Pollinations API linki
                img_url = f"https://image.pollinations.ai/prompt/{encoded_art}?nologo=true"
                
                # Resmi ekranda göster
                st.image(img_url, caption=f"Stil: {art_style} | Kr AI Tasarımı", use_container_width=True)
                st.balloons()
        else:
            st.warning("Lütfen önce resmini çizmek istediğiniz bir şeyler yazın!")
