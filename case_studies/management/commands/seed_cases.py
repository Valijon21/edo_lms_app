from django.core.management.base import BaseCommand
from django.db import transaction
from case_studies.models import CaseStudy, ScenarioNode, ScenarioEdge
from gamification.models import Badge

class Command(BaseCommand):
    help = "Seeds interactive case studies and mock gamification data into the database"

    def handle(self, *args, **options):
        self.stdout.write("Seeding data started...")
        
        with transaction.atomic():
            # 1. Clean existing records (optional, but good for idempotency)
            CaseStudy.objects.all().delete()
            Badge.objects.filter(badge_type__in=['fast_learner', 'seven_day_streak', 'streak_3', 'streak_7']).delete()
            
            # 2. Seed Badges
            Badge.objects.create(
                name="Tezkor O'rganuvchi",
                description="100 XP to'plagan foydalanuvchilar uchun",
                badge_type="fast_learner",
                xp_required=100
            )
            Badge.objects.create(
                name="3 Kunlik Streak",
                description="Ketma-ket 3 kun faol bo'ling",
                badge_type="streak_3",
                xp_required=30
            )
            Badge.objects.create(
                name="7 Kunlik Streak",
                description="Ketma-ket 7 kun faol bo'ling",
                badge_type="streak_7",
                xp_required=70
            )
            
            # 3. Create Case Study
            case = CaseStudy.objects.create(
                title="Kiruvchi Hujjatlar Bilan Ishlash (Shoshilinch Vaziyat)",
                description="Tashqi idoradan shoshilinch ijro etilishi lozim bo'lgan xat keldi, biroq mas'ul rahbar safarda. Vaziyatni to'g'ri hal eting.",
                xp_reward=50
            )
            
            # 4. Create Nodes
            n_start = ScenarioNode.objects.create(
                case_study=case,
                title="Ssenariy Boshi",
                content="Tashqi idoradan shoshilinch ijro etilishi lozim bo'lgan xat keldi, biroq mas'ul rahbar xizmat safarida. Hujjatni qanday yo'naltirasiz?",
                is_start_node=True
            )
            
            n_register = ScenarioNode.objects.create(
                case_study=case,
                title="Hujjat Ro'yxatdan O'tdi",
                content="Siz hujjatni qabul qilib, ro'yxatdan o'tkazdingiz. Endi mas'ul rezolyutsiya yozuvchini belgilashingiz kerak. Kimni tanlaysiz?",
            )
            
            n_delegate = ScenarioNode.objects.create(
                case_study=case,
                title="Muvaqqat Raxbar Rezolyutsiyasi",
                content="Muvaqqat vazifasini bajaruvchi rahbarga rezolyutsiya yuborildi. U topshiriq loyihasini tayyorlashni buyurdi.",
            )
            
            n_wait = ScenarioNode.objects.create(
                case_study=case,
                title="Rahbar Qaytishini Kutish",
                content="Siz rahbar safardan qaytishini kutishga qaror qildingiz. Biroq hujjat ijro muddati 2 kun bo'lganligi sababli, ijro intizomi tizimida QIZIL ogohlantirish paydo bo'ldi va muddat buzildi.",
            )
            
            n_success = ScenarioNode.objects.create(
                case_study=case,
                title="Muvaffaqiyatli Yakun",
                content="Topshiriq loyihasi tasdiqlandi va ijrochiga muddatida yuborildi. Ish muvaffaqiyatli yakunlandi! Siz o'z vazifangizni a'lo darajada bajardingiz.",
                is_end_node=True
            )
            
            n_fail = ScenarioNode.objects.create(
                case_study=case,
                title="Muvaffaqiyatsiz Yakun",
                content="Ijro muddati buzildi yoki noto'g'ri rezolyutsiya sababli loyiha bekor qilindi. Siz tizimda intizomiy ogohlantirish oldingiz.",
                is_fail_node=True
            )
            
            # 5. Create Edges (Branches)
            # From Start Node
            ScenarioEdge.objects.create(
                from_node=n_start,
                to_node=n_register,
                option_text="Hujjatni qabul qilish va ro'yxatdan o'tkazish",
                feedback_text="To'g'ri qaror! Tizimga kelgan har qanday rasmiy hujjat dastlab ro'yxatdan o'tishi shart.",
                xp_delta=10
            )
            ScenarioEdge.objects.create(
                from_node=n_start,
                to_node=n_wait,
                option_text="Rahbar xizmat safaridan qaytishini kutish",
                feedback_text="Noto'g'ri. Shoshilinch xatlarni ro'yxatga olmasdan kutib turish ijro intizomining buzilishiga sabab bo'ladi.",
                xp_delta=-5
            )
            
            # From Register Node
            ScenarioEdge.objects.create(
                from_node=n_register,
                to_node=n_delegate,
                option_text="Muvaqqat vazifasini bajaruvchi rahbarga rezolyutsiya yozish uchun yuborish",
                feedback_text="To'g'ri! Asosiy rahbar bo'lmaganda, uning vakolatlarini rasman bajaruvchi shaxs rezolyutsiya (topshiriq) berishga haqli.",
                xp_delta=15
            )
            ScenarioEdge.objects.create(
                from_node=n_register,
                to_node=n_wait,
                option_text="Rezolyutsiyani safardagi rahbarning o'ziga yuborish va kutish",
                feedback_text="Noto'g'ri. Rahbar xizmat safarida bo'lganida internet va tizimga kirish imkoni cheklangan bo'lishi mumkin. Vaqt yo'qotiladi.",
                xp_delta=-5
            )
            
            # From Wait Node
            ScenarioEdge.objects.create(
                from_node=n_wait,
                to_node=n_fail,
                option_text="Jarayonni yakunlash (Xatolikni tan olish)",
                feedback_text="Siz ijro muddatini o'tkazib yubordingiz. Bu tashkilot reytingiga salbiy ta'sir ko'rsatadi.",
                xp_delta=0
            )
            
            # From Delegate Node
            ScenarioEdge.objects.create(
                from_node=n_delegate,
                to_node=n_success,
                option_text="Topshiriq loyihasini kiritish va ijrochilarga yuborish",
                feedback_text="Ajoyib! Topshiriq o'z vaqtida shakllantirilib ijrochiga yetkazildi.",
                xp_delta=25
            )
            ScenarioEdge.objects.create(
                from_node=n_delegate,
                to_node=n_fail,
                option_text="Topshiriqni rad etish va loyihani bekor qilish",
                feedback_text="Noto'g'ri qaror. Muvaqqat rahbar buyrug'ini asossiz bekor qilish ish faoliyatini to'xtatib qo'yadi.",
                xp_delta=-10
            )

        self.stdout.write(self.style.SUCCESS("Data successfully seeded!"))
