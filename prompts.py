# =====================================
# المرحلة الأولى : نصوص التوجيه للنظام
# =====================================

# النص التوجيهي الأساسي للمساعد
SYSTEM_PROMPT = """You are Gemini AI Assistant, a helpful and friendly AI assistant powered by Google Gemini 2.5 Flash.

Your role:
- Answer user questions clearly and accurately
- Be helpful, polite, and professional
- Provide detailed explanations when needed
- If you don't know something, say so honestly

Guidelines:
- Use simple and clear language
- Structure your responses well
- Be concise but comprehensive
- Support both Arabic and English queries"""

# =====================================
# المرحلة الثانية : نصوص مساعدة
# =====================================

# ترحيب المساعد
WELCOME_MESSAGE = "Hello! I'm Gemini AI Assistant. How can I help you today?"

# رسالة خطأ عامة
ERROR_MESSAGE = "Sorry, something went wrong. Please try again."

# رسالة عند عدم وجود صورة
NO_IMAGE_MESSAGE = "Please upload an image first."

# =====================================
# المرحلة الثالثة : تنسيق النصوص
# =====================================

def format_prompt(user_message: str, system_prompt: str = SYSTEM_PROMPT) -> str:
    """
    دمج النص التوجيهي مع رسالة المستخدم
    """
    return f"{system_prompt}\n\nUser: {user_message}"

def get_full_prompt(user_message: str, image_analysis: str = None) -> str:
    """
    إنشاء النص الكامل مع تحليل الصورة إن وجدت
    """
    if image_analysis:
        return f"{SYSTEM_PROMPT}\n\nImage Analysis: {image_analysis}\n\nUser: {user_message}"
    return format_prompt(user_message)