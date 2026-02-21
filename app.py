import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_mic_recorder import mic_recorder
import time

# --- إعداد الهوية والذكاء الاصطناعي ---
# ⚠️ حط الـ API Key بتاعك هنا بين العلامتين
MY_API_KEY = "AIzaSyCOdFVcx0W2pdlfh5uDTq-v5DN2zD2ZfWU" 

genai.configure(api_key=MY_API_KEY)

# حل مشكلة الـ 404 بتحديد المسار الكامل للموديل
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

# --- إعدادات الواجهة الشيك ---
st.set_page_config(page_title="X ASSISTANT v2", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 50px;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
        text-align: center;
    }
    .stChatMessage { border-radius: 15px; border: 1px solid #1e272e; }
    </style>
    """, unsafe_allow_html=True)

# --- الأنيميشن بتاع الدخول ---
if 'entry' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown('<div style="text-align:center; padding:100px;"><h1 class="main-title">X ASSISTANT v2</h1><p style="color:#4facfe;">System Loading...</p></div>', unsafe_allow_html=True)
        time.sleep(2)
    st.session_state.entry = True
    placeholder.empty()

# --- نظام الذاكرة ---
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])
if "user_name" not in st.session_state:
    st.session_state.user_name = "Harreef"

# --- القائمة الجانبية (صور وصوت) ---
with st.sidebar:
    st.markdown(f"### أهلاً يا **{st.session_state.user_name}** 😎")
    st.divider()
    
    st.write("📸 **ارفع صورة للتحليل:**")
    up_img = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    st.divider()
    st.write("🎤 **سجل رسالة صوتية:**")
    # إضافة زر الصوت بجانب خانة الشات (هنا في الجنب لضمان الاستقرار)
    audio_record = mic_recorder(start_prompt="إبدأ الكلام 🎤", stop_prompt="إرسال 📤", key='mic')
    
    if st.button("🗑️ مسح الذاكرة"):
        st.session_state.chat = model.start_chat(history=[])
        st.rerun()

# --- عرض المحادثة ---
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# --- معالجة المدخلات ---
prompt = st.chat_input("تؤمرني بإيه يا Harreef؟")

# دمج الرسالة الصوتية لو وجدت
if audio_record and not prompt:
    prompt = "لقد أرسلت لك تسجيلاً صوتياً، كيف يمكنني مساعدتك بخصوصه؟"

if prompt:
    # حفظ اسم المستخدم لو قاله
    if "اسمي" in prompt:
        st.session_state.user_name = prompt.split("اسمي")[-1].strip()

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("جاري الاتصال بالعقل المفكر..."):
            try:
                if up_img:
                    img = Image.open(up_img)
                    # إرسال النص مع الصورة
                    response = st.session_state.chat.send_message([prompt, img])
                else:
                    response = st.session_state.chat.send_message(prompt)
                
                st.markdown(response.text)
            except Exception as e:
                # حل ذكي لو حصل خطأ في الموديل تاني
                st.error(f"عذراً يا حريف، حصل خطأ في الاتصال: {e}")
  
