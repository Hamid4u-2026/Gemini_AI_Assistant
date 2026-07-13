# =====================================
# المرحلة الأولى : استيراد المكتبات
# =====================================

import streamlit as st
from gemini_client import GeminiClient
from prompts import WELCOME_MESSAGE, ERROR_MESSAGE
from utils import save_uploaded_image, validate_image, cleanup_temp_files

# =====================================
# المرحلة الثانية : تهيئة التطبيق
# =====================================

# عنوان الصفحة
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# =====================================
# المرحلة الثالثة : تهيئة جلسة المحادثة
# =====================================

# تهيئة سجل المحادثة في الجلسة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": WELCOME_MESSAGE}
    ]

# تهيئة عميل Gemini
if "gemini_client" not in st.session_state:
    st.session_state.gemini_client = GeminiClient()

# =====================================
# المرحلة الرابعة : الشريط الجانبي
# =====================================

with st.sidebar:
    st.markdown("## 🤖 Gemini AI Assistant")
    st.markdown("---")
    
    # معلومات النموذج
    st.markdown("### Model")
    st.info("⚡ Gemini 2.5 Flash")
    
    st.markdown("---")
    
    # أزرار التحكم
    st.markdown("### Controls")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE}
        ]
        st.rerun()
    
    st.markdown("---")
    
    # معلومات إضافية
    st.markdown("### About")
    st.caption("Built with Streamlit & Google Gemini 2.5 Flash")

# =====================================
# المرحلة الخامسة : عرض المحادثة
# =====================================

st.title("🤖 Gemini AI Assistant")
st.caption("Powered by Google Gemini 2.5 Flash")

# عرض جميع رسائل المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================
# المرحلة السادسة : رفع الصور (فوق مربع الإدخال)
# =====================================

uploaded_file = st.file_uploader(
    "Upload Image (Optional)",
    type=["jpg", "jpeg", "png", "gif", "webp"],
    help="Upload an image to analyze with your question"
)

# عرض الصورة المرفوعة
if uploaded_file is not None:
    # التحقق من صحة الصورة
    if not validate_image(uploaded_file):
        st.error("Invalid image. Please upload a JPEG, PNG, GIF, or WEBP image under 5MB.")
        uploaded_file = None
    else:
        st.image(uploaded_file, caption="Uploaded Image", width=200)

# =====================================
# المرحلة السابعة : مربع إدخال المستخدم
# =====================================

# مربع الإدخال
user_input = st.chat_input("Ask me anything...")

if user_input:
    # إضافة رسالة المستخدم إلى المحادثة
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # معالجة الطلب
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = st.session_state.gemini_client
                
                # التحقق من وجود صورة
                if uploaded_file is not None:
                    # حفظ الصورة مؤقتاً
                    image_path = save_uploaded_image(uploaded_file)
                    
                    # إرسال الصورة مع السؤال
                    response = client.analyze_image(
                        image_path=image_path,
                        question=user_input
                    )
                    
                    # تنظيف الملفات المؤقتة
                    cleanup_temp_files()
                else:
                    # إرسال سؤال نصي فقط
                    response = client.ask(user_input)
                
                # عرض الرد
                st.markdown(response)
                
                # إضافة رد المساعد إلى المحادثة
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                
            except Exception as e:
                error_msg = f"{ERROR_MESSAGE}\n\nError: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
                