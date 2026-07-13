# =====================================
# المرحلة الأولى : استيراد المكتبات
# =====================================

import os
from google import genai
from dotenv import load_dotenv

# =====================================
# المرحلة الثانية : تهيئة العميل
# =====================================

class GeminiClient:
    """
    Handles communication with Google Gemini API.
    """

    def __init__(self):
        # تحميل المتغيرات من ملف .env
        load_dotenv()
        
        # استرجاع مفتاح API
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        # التحقق من وجود المفتاح
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is missing. Please add it to .env file.")
        
        # إنشاء عميل Gemini
        self.client = genai.Client(api_key=self.api_key)
        
        # تحديد النموذج
        self.model = "gemini-2.5-flash"
        # =====================================
# المرحلة الثالثة : إرسال الأسئلة النصية
# =====================================

    def ask(self, question: str) -> str:
        """
        Send a text question to Gemini and return the response.
        """
        try:
            # إرسال السؤال إلى النموذج
            response = self.client.models.generate_content(
                model=self.model,
                contents=question
            )
            
            # استرجاع النص من الرد
            return response.text
        
        except Exception as e:
            # إرجاع رسالة الخطأ
            return f"Error: {str(e)}"
        # =====================================
# المرحلة الرابعة : تحليل الصور
# =====================================

    def analyze_image(self, image_path: str, question: str = "What do you see in this image?") -> str:
        """
        Send an image to Gemini for analysis with an optional question.
        """
        try:
            # قراءة ملف الصورة
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            # إرسال الصورة والسؤال إلى النموذج
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    {
                        "parts": [
                            {"text": question},
                            {"inline_data": {"mime_type": "image/jpeg", "data": image_data}}
                        ]
                    }
                ]
            )
            
            # استرجاع النص من الرد
            return response.text
        
        except Exception as e:
            # إرجاع رسالة الخطأ
            return f"Error: {str(e)}"
        