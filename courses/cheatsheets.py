"""Cheat Sheet kontent registry — har bir modul uchun 1-sahifalik PDF kontenti."""

CHEAT_SHEETS = {
    "kiruvchi": {
        "title": "Kiruvchi Hujjatlar — Tezkor Yo'riqnoma",
        "subtitle": "Edo.ijro.uz orqali kiruvchi hujjatlarni qabul qilish bosqichlari",
        "steps": [
            {
                "number": "1",
                "title": "Tizimga kirish",
                "description": "login.ijro.uz → Foydalanuvchi nomi va parol bilan kiring.",
            },
            {
                "number": "2",
                "title": "Kiruvchi xatlar bo'limi",
                "description": "Chap menyu → 'Kiruvchi xatlar' bo'limiga o'ting.",
            },
            {
                "number": "3",
                "title": "Hujjatni ko'rish",
                "description": "Ro'yxatdan kerakli hujjatni tanlang va tafsilotlarni o'qing.",
            },
            {
                "number": "4",
                "title": "Ro'yxatdan o'tkazish",
                "description": "Hujjatni qabul qiling va tartib raqamini belgilang.",
            },
            {
                "number": "5",
                "title": "Ijrochini belgilash",
                "description": "'Yo'naltirish' tugmasi orqali mas'ul xodimni tanlang.",
            },
            {
                "number": "6",
                "title": "Javob xatini yozish",
                "description": "Kerak bo'lsa javob xatini tayyorlab, imzolang va yuboring.",
            },
        ],
        "tips": [
            "Muhim: Har bir hujjatga 3 kun ichida javob qaytaring.",
            "Shoshilinch hujjatlarga darhol e'tibor bering — qizil belgi bilan ko'rsatiladi.",
            "Hujjat tarixini kuzatish uchun 'Tarix' yorlig'idan foydalaning.",
        ],
        "legal_ref": "O'zR VQ 707-sonli qaror, 6-band",
    },
    "chiquvchi": {
        "title": "Chiquvchi Hujjatlar — Tezkor Yo'riqnoma",
        "subtitle": "Edo.ijro.uz orqali chiquvchi xat tayyorlash va yuborish bosqichlari",
        "steps": [
            {
                "number": "1",
                "title": "Yangi xat yaratish",
                "description": "'Chiquvchi xatlar' → 'Yangi xat' tugmasini bosing.",
            },
            {
                "number": "2",
                "title": "Qabul qiluvchini tanlash",
                "description": "Tashkilot yoki shaxsni qidirish orqali toping va tanlang.",
            },
            {
                "number": "3",
                "title": "Xat matnini kiritish",
                "description": "Mavzu, matn va ilova fayllarini kiriting.",
            },
            {
                "number": "4",
                "title": "Imzolash",
                "description": "Rahbar yoki mas'ul shaxs ERI (elektron raqamli imzo) bilan tasdiqlaydi.",
            },
            {
                "number": "5",
                "title": "Yuborish",
                "description": "'Yuborish' tugmasini bosing — xat qabul qiluvchiga yetkaziladi.",
            },
            {
                "number": "6",
                "title": "Holatni kuzatish",
                "description": "'Yuborilganlar' bo'limidan xat holatini tekshiring.",
            },
        ],
        "tips": [
            "Xat raqamini tizim avtomatik beradi — o'zgartirmang.",
            "Ilova fayllari hajmi 20 MB dan oshmasligi kerak.",
            "Yuborishdan oldin oldindan ko'rish (preview) qiling.",
        ],
        "legal_ref": "O'zR VQ 707-sonli qaror, 7-band",
    },
    "ichki": {
        "title": "Ichki Buyruqlar — Tezkor Yo'riqnoma",
        "subtitle": "Edo.ijro.uz orqali ichki buyruq tayyorlash va nazorat qilish",
        "steps": [
            {
                "number": "1",
                "title": "Buyruq loyihasini yaratish",
                "description": "'Ichki hujjatlar' → 'Yangi buyruq' tugmasini bosing.",
            },
            {
                "number": "2",
                "title": "Buyruq matnini kiritish",
                "description": "Buyruq mazmuni, muddati va ijrochini kiriting.",
            },
            {
                "number": "3",
                "title": "Kelishish jarayoni",
                "description": "Tegishli bo'lim boshliqlari bilan kelishib oling.",
            },
            {
                "number": "4",
                "title": "Tasdiqlash",
                "description": "Rahbar ERI bilan imzolab tasdiqlaydi.",
            },
            {
                "number": "5",
                "title": "Ijrochiga yuborish",
                "description": "Tasdiqlangan buyruq ijrochilarga avtomatik yuboriladi.",
            },
            {
                "number": "6",
                "title": "Nazorat qilish",
                "description": "'Nazorat' bo'limidan ijro holatini kuzating.",
            },
        ],
        "tips": [
            "Buyruq muddati o'tkazib yuborilsa, tizim avtomatik ogohlantiradi.",
            "Bir buyruqqa bir nechta ijrochi belgilash mumkin.",
            "Buyruq tarixini PDF formatda yuklab olish mumkin.",
        ],
        "legal_ref": "O'zR VQ 707-sonli qaror, 12-band",
    },
    "ijro": {
        "title": "Ijro Intizomi — Tezkor Yo'riqnoma",
        "subtitle": "Edo.ijro.uz orqali topshiriqlar va muddatlarni boshqarish",
        "steps": [
            {
                "number": "1",
                "title": "Topshiriqlar paneli",
                "description": "Bosh sahifadagi 'Mening topshiriqlarim' bo'limiga kiring.",
            },
            {
                "number": "2",
                "title": "Yangi topshiriqni qabul qilish",
                "description": "Kiruvchi topshiriqni ko'rib chiqing va qabul qiling.",
            },
            {
                "number": "3",
                "title": "Muddatni tekshirish",
                "description": "Har bir topshiriq muddatiga e'tibor bering (qizil = shoshilinch).",
            },
            {
                "number": "4",
                "title": "Ijroni boshlash",
                "description": "'Ijroga olish' tugmasini bosib, ishni boshlang.",
            },
            {
                "number": "5",
                "title": "Hisobotni yuborish",
                "description": "Bajarilgan ish bo'yicha hisobot va hujjatlarni ilova qiling.",
            },
            {
                "number": "6",
                "title": "Monitoring",
                "description": "'Ijro holati' bo'limidan umumiy statistikani kuzating.",
            },
        ],
        "tips": [
            "Muddat o'tgan topshiriqlar qizil rang bilan ajratiladi.",
            "Har kuni platformaga kirish odatini shakllantiring.",
            "Ogohlantirish: 3 kundan ko'p kechikish intizomiy choraga olib keladi.",
        ],
        "legal_ref": "O'zR VQ 707-sonli qaror, 15-band",
    },
}


def get_cheat_sheet_for_module(module):
    """Modul title'iga qarab cheat sheet kontentini qaytaradi.

    Matching: modul title'ida kalit so'z (kiruvchi, chiquvchi, ichki, ijro)
    mavjud bo'lsa, shunga mos kontent qaytaradi.
    """
    title_lower = module.title.lower()
    for key in CHEAT_SHEETS:
        if key in title_lower:
            return CHEAT_SHEETS[key]
    return None
