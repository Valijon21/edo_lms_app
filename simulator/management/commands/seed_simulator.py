from django.core.management.base import BaseCommand
from simulator.models import SimulationScenario, DocumentType, DifficultyLevel


class Command(BaseCommand):
    help = "Edo.ijro.uz virtual simulyatori uchun boshlang'ich ssenariylarni bazaga yuklaydi."

    def handle(self, *args, **kwargs):
        scenarios_data = [
            {
                "title": "Kiruvchi xat va rezolyutsiya qo'yish",
                "doc_type": DocumentType.KIRUVCHI,
                "difficulty": DifficultyLevel.EASY,
                "description": (
                    "Raqamli texnologiyalar vazirligidan kelgan xatni ko'rib chiqing va uni ijro etish "
                    "uchun mas'ul xodimga yo'naltiring, tegishli topshiriq matni hamda muddatini belgilang."
                ),
                "xp_reward": 100,
                "initial_doc_data": {
                    "doc_number": "12-45/89",
                    "doc_date": "2026-07-20",
                    "sender": "Raqamli Texnologiyalar Vazirligi",
                    "subject": "Sun'iy intellekt texnologiyalarini o'quv dasturlariga tatbiq etish to'g'risida",
                    "file_url": "/static/docs/kiruvchi_ai_tadbik.pdf",
                    "signer": "M. Karimov (Vazir o'rinbosari)"
                },
                "expected_steps": [
                    {
                        "action": "open_doc",
                        "title": "Hujjatni ochish",
                        "description": "Kelgan yangi xatni o'qib chiqish uchun uning ustiga bosing va hujjatni oching.",
                        "error_hint": "Avval kelgan hujjatni ochib, mazmuni bilan tanishib chiqing.",
                        "success_message": "Hujjat ochildi!",
                        "feedback": "Hujjat matni va fayli bilan tanishib chiqdingiz. Endi rezolyutsiya kiritishingiz kerak.",
                        "required_fields": []
                    },
                    {
                        "action": "add_resolution",
                        "title": "Rezolyutsiya yozish",
                        "description": "Hujjatga rezolyutsiya yozing: ijrochini tanlang (masalan, 'A. Qodirov'), topshiriq matnini yozing ('O'quv rejasini ko'rib chiqib taklif kiriting') va bajarish muddatini belgilang.",
                        "error_hint": "Iltimos, topshiriq berish uchun rezolyutsiya bo'limini to'ldiring.",
                        "success_message": "Rezolyutsiya loyihalandi!",
                        "feedback": "Topshiriq mazmuni, ijrochi va muddat to'g'ri kiritildi. Endi rezolyutsiyani tasdiqlang.",
                        "required_fields": ["executor", "text", "deadline"]
                    },
                    {
                        "action": "approve_resolution",
                        "title": "Rezolyutsiyani tasdiqlash",
                        "description": "Tayyorlangan rezolyutsiyani tasdiqlash (Yuborish) tugmasini bosing.",
                        "error_hint": "Rezolyutsiyani yuborish/tasdiqlash tugmasini bosing.",
                        "success_message": "Ssenariy yakunlandi!",
                        "feedback": "Ajoyib! Rezolyutsiya tizimda ro'yxatdan o'tdi va ijrochiga yuborildi. Siz 100 XP to'pladingiz!",
                        "required_fields": ["is_approved"]
                    }
                ]
            },
            {
                "title": "Chiquvchi javob xati tayyorlash",
                "doc_type": DocumentType.CHIQUVCHI,
                "difficulty": DifficultyLevel.MEDIUM,
                "description": (
                    "Avvalgi topshiriq bo'yicha vazirlikka yuboriladigan chiquvchi javob xati loyihasini "
                    "rasmiylashtiring, javob xati faylini biriktiring va rahbariyatga imzolash uchun taqdim eting."
                ),
                "xp_reward": 150,
                "initial_doc_data": {
                    "base_doc_number": "12-45/89",
                    "base_doc_title": "Sun'iy intellekt texnologiyalarini o'quv dasturlariga tatbiq etish to'g'risida",
                    "status": "Loyiha bosqichi"
                },
                "expected_steps": [
                    {
                        "action": "create_draft",
                        "title": "Loyiha yaratish",
                        "description": "Javob xati loyihasini yarating: sarlavhaga 'O'quv rejalariga SI tatbiq etish bo'yicha javob xati' va matn qismiga 'Ssenariy asosida tayyorlangan hisobot ilova qilinmoqda' deb kiritib loyiha yarating.",
                        "error_hint": "Javob xati loyihasini yaratish uchun sarlavha va asosiy matnni kiritishingiz lozim.",
                        "success_message": "Loyiha yaratildi!",
                        "feedback": "Loyiha muvaffaqiyatli yaratildi. Endi hisobot faylini (PDF formatida) biriktiring.",
                        "required_fields": ["doc_title", "doc_body"]
                    },
                    {
                        "action": "attach_file",
                        "title": "Fayl biriktirish",
                        "description": "Javob xatiga fayl biriktiring (fayl nomi: 'si_hisobot.pdf').",
                        "error_hint": "Tashkilotga yuboriladigan asosiy hisobot faylini (PDF) yuklashingiz kerak.",
                        "success_message": "Fayl muvaffaqiyatli yuklandi!",
                        "feedback": "Hisobot fayli biriktirildi. Endi ushbu loyihani imzolashi uchun tashkilot rahbariga yuboring.",
                        "required_fields": ["file_name"]
                    },
                    {
                        "action": "send_to_sign",
                        "title": "Imzolashga yuborish",
                        "description": "Imzolaydigan rahbarni tanlang (masalan, 'J. Ergashev - Direktor') va loyihani imzolashga jo'nating.",
                        "error_hint": "Loyihani imzolashi uchun rahbarni tanlang va 'Imzolashga yuborish' tugmasini bosing.",
                        "success_message": "Ssenariy yakunlandi!",
                        "feedback": "Barakalla! Javob xati loyihasi rahbarning shaxsiy kabinetiga imzolash uchun muvaffaqiyatli yuborildi. Siz 150 XP to'pladingiz!",
                        "required_fields": ["supervisor"]
                    }
                ]
            },
            {
                "title": "Tashkilot ichki buyrug'i va nazorati",
                "doc_type": DocumentType.ICHKI_BUYRUQ,
                "difficulty": DifficultyLevel.HARD,
                "description": (
                    "Tashkilot xodimlarining malaka oshirish kurslarini tashkil etish to'g'risida ichki buyruq "
                    "rasmiylashtiring. Buyruq ijrosini nazorat qiluvchi shaxsni va oxirgi muddatni belgilab, chop eting (imzolang)."
                ),
                "xp_reward": 200,
                "initial_doc_data": {
                    "doc_type_name": "Ichki buyruq",
                    "status": "Yangi loyiha"
                },
                "expected_steps": [
                    {
                        "action": "write_order",
                        "title": "Buyruq matnini kiritish",
                        "description": "Buyruq sarlavhasini 'Malaka oshirish kurslari to'g'risida' deb nomlang, buyruq matniga esa malaka oshirish tartibi va mas'ullarni kiritib loyiha yozing.",
                        "error_hint": "Buyruq loyihasini yozish uchun sarlavha va matnni kiritishingiz shart.",
                        "success_message": "Buyruq matni kiritildi!",
                        "feedback": "Buyruq matni muvaffaqiyatli yozildi. Endi buyruq ustidan nazorat muddatini hamda nazorat qiluvchi shaxsni belgilang.",
                        "required_fields": ["order_title", "order_content"]
                    },
                    {
                        "action": "set_controller",
                        "title": "Nazoratchi va muddat belgilash",
                        "description": "Buyruq ijrosi nazoratini topshirish uchun nazoratchini (masalan, 'K. Tursunov') va nazorat muddatini kiriting.",
                        "error_hint": "Nazoratchi ismi va bajarilish muddati kiritilishi shart.",
                        "success_message": "Nazorat parametrlari belgilandi!",
                        "feedback": "Nazorat parametrlari o'rnatildi. Endi buyruqni rasmiy kuchga ega bo'lishi uchun tasdiqlang va imzolang.",
                        "required_fields": ["controller_name", "deadline"]
                    },
                    {
                        "action": "publish_order",
                        "title": "Buyruqni imzolash va chop etish",
                        "description": "Tasdiqlash va imzolash tugmasini bosib buyruqni e'lon qiling.",
                        "error_hint": "Buyruqni tasdiqlang va imzolash tugmasini bosing.",
                        "success_message": "Ssenariy yakunlandi!",
                        "feedback": "Ajoyib ish! Ichki buyruq tasdiqlandi, tizimda ro'yxatga olindi va barcha xodimlarga tanishish uchun yuborildi. Siz 200 XP to'pladingiz!",
                        "required_fields": ["is_signed"]
                    }
                ]
            }
        ]

        self.stdout.write("Ssenariylarni yuklash boshlandi...")

        for s_data in scenarios_data:
            scenario, created = SimulationScenario.objects.update_or_create(
                title=s_data["title"],
                defaults={
                    "doc_type": s_data["doc_type"],
                    "difficulty": s_data["difficulty"],
                    "description": s_data["description"],
                    "xp_reward": s_data["xp_reward"],
                    "initial_doc_data": s_data["initial_doc_data"],
                    "expected_steps": s_data["expected_steps"],
                    "is_active": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Yangi ssenariy yaratildi: '{scenario.title}'"))
            else:
                self.stdout.write(self.style.WARNING(f"Ssenariy yangilandi: '{scenario.title}'"))

        self.stdout.write(self.style.SUCCESS("Barcha ssenariylar muvaffaqiyatli yuklandi!"))
