import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
try:
    user = User.objects.get(username="valijon")
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("Muvaffaqiyatli: 'valijon' foydalanuvchisi admin (superuser) qilindi!")
    print("Endi tizimdagi parolingiz bilan admin panelga kira olasiz.")
except User.DoesNotExist:
    # Agar valijon foydalanuvchisi mavjud bo'lmasa, uni yaratamiz va admin qilamiz
    user = User.objects.create_superuser("valijon", "valijon@example.com", "valijon123")
    print("Muvaffaqiyatli: 'valijon' nomli yangi superuser yaratildi. Parol: valijon123")
