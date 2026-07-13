# =====================================
# المرحلة الأولى : استيراد المكتبات
# =====================================

import os
from PIL import Image
import io

# =====================================
# المرحلة الثانية : معالجة الصور
# =====================================

def save_uploaded_image(uploaded_file) -> str:
    """
    حفظ الصورة المرفوعة مؤقتاً وإرجاع مسارها
    """
    # إنشاء مجلد مؤقت إن لم يكن موجوداً
    os.makedirs("temp", exist_ok=True)
    
    # تحديد مسار الصورة
    image_path = os.path.join("temp", uploaded_file.name)
    
    # حفظ الصورة
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return image_path

def validate_image(uploaded_file) -> bool:
    """
    التحقق من صحة الصورة (النوع والحجم)
    """
    # التحقق من نوع الملف
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if uploaded_file.type not in allowed_types:
        return False
    
    # التحقق من الحجم (أقل من 5 ميجابايت)
    if uploaded_file.size > 5 * 1024 * 1024:
        return False
    
    return True

def get_image_info(image_path: str) -> dict:
    """
    استخراج معلومات الصورة (الأبعاد - النوع - الحجم)
    """
    try:
        img = Image.open(image_path)
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode
        }
    except Exception as e:
        return {"error": str(e)}

def cleanup_temp_files():
    """
    حذف الملفات المؤقتة
    """
    temp_dir = "temp"
    if os.path.exists(temp_dir):
        for file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception:
                pass

# =====================================
# المرحلة الثالثة : دوال مساعدة للنصوص
# =====================================

def clean_text(text: str) -> str:
    """
    تنظيف النصوص من المسافات الزائدة والأسطر الفارغة
    """
    # إزالة المسافات الزائدة من البداية والنهاية
    text = text.strip()
    
    # إزالة الأسطر الفارغة المتعددة
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    
    return '\n'.join(lines)

def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    اختصار النص إذا تجاوز الطول المحدد
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text