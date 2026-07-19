import streamlit as st
from groq import Groq
import time

# --- 1. API BAĞLANTISI ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception:
    st.error("🔑 API Key Hatası!")
    st.stop()

st.set_page_config(page_title="Kr AI Pro v6.0", page_icon="👑", layout="wide")

# --- 2. GÜÇLENDİRİLMİŞ KİMLİK (SYSTEM PROMPT) ---
# Buradaki talimatlar robotun zekasını belirler
SYSTEM_INSTRUCTIONS = """
Sen Kr AI Pro'sun. Senin en önemli özelliğin, karmaşık konuları (Arduino, kodlama, yapay zeka vb.) 
çocuk düzeyinde anlayabilecek kadar basit, ama bir mühendis düzeyinde açıklayabilecek kadar teknik olmandır.
Asla üstünkörü cevap verme. 
Cevap verirken şu adımları izle:
1. Konuyu tanımla.
2. Neden önemli olduğunu belirt.
3. Teknik detaylara gir.
4. Bir örnekle veya kullanım alanıyla bitir.
Seni Türk mühendisler geliştirdi, bunu gururla söyleyebilirsin ama sohbetin odağını her zaman bilgiye ver.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_INSTRUCTIONS}]

# --- 3. ANA MANTIK (Llama 3.3 70B - En Zeki Model) ---
with st.chat_message("assistant"):
    st.markdown("👑 Kr AI v6.0 Aktif. Mühendislik moduna geçildi. Arduino'dan atom fiziğine kadar sorabilirsin.")

for message in [m for m in st.session_state.messages if m["role"] != "system"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Arduino nedir? (Detaylı anlat...)"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kr AI derinlemesine analiz ediyor..."):
            completion = client.chat.completions.create(
                messages=st.session_state.messages,
                model="llama-3.3-70b-versatile",
                temperature=0.3 # 0.3 değeri daha "kesin" ve "mantıklı" cevaplar sağlar
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
