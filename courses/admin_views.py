from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import uuid


@staff_member_required
@csrf_protect
def upload_image(request):
    """
    TinyMCE rich text editor'i uchun rasm yuklash API.
    Faqatgina admin xodimlari (staff) foydalana oladi va CSRF token talab qilinadi.
    """
    if request.method == "POST" and request.FILES.get("file"):
        image_file = request.FILES["file"]
        
        # Fayl kengaytmasini tekshirish
        ext = os.path.splitext(image_file.name)[1].lower()
        if ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
            return JsonResponse(
                {"error": "Faqat rasm fayllari yuklashga ruxsat etilgan (.jpg, .jpeg, .png, .gif, .webp)"},
                status=400
            )
            
        # UUID yordamida takrorlanmas nom yaratish (fayllar bir-birini o'chirib yubormasligi uchun)
        filename = f"{uuid.uuid4()}{ext}"
        path = default_storage.save(f"uploads/{filename}", ContentFile(image_file.read()))
        
        # Faylga tegishli to'liq URL manzilini olish
        url = default_storage.url(path)
        return JsonResponse({"location": url})
        
    return JsonResponse({"error": "Noto'g'ri so'rov usuli yoki fayl yetishmayapti."}, status=400)
