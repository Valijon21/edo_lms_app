"""
Demo keys ma'lumotlarini yaratish uchun management command
"""
from django.core.management.base import BaseCommand
from case_studies.models import CaseStudy, ScenarioNode, ScenarioEdge


class Command(BaseCommand):
    help = "Demo keys ma'lumotlarini yaratadi"

    def handle(self, *args, **options):
        self.stdout.write('Demo keys yaratilmoqda...')

        # Eski demo keyslarni o'chirish
        CaseStudy.objects.filter(
            title__contains='Demo'
        ).delete()

        # 1-Keys: Shoshilinch hujjat keldi
        case1 = CaseStudy.objects.create(
            title="Shoshilinch hujjat yo'naltirish",
            description=(
                "Tashqi idoradan juda muhim va shoshilinch xat keldi. "
                "Mas'ul rahbar xizmat safarida. Qanday yo'naltirish kerak?"
            ),
            xp_reward=100,
            is_active=True
        )

        # Start node
        start = ScenarioNode.objects.create(
            case_study=case1,
            title="Vaziyat tavsifi",
            content=(
                "Siz ish boshqarish bo'limi xodimisiz. "
                "Bugun ertalab tashqi idoradan \"JUDA SHOSHILINCH\" "
                "belgisi bilan xat keldi. Xat sizning bo'lim "
                "rahbaringizga qaratilgan, lekin u 3 kun davomida "
                "xizmat safarida. Xat ertaga soat 12:00 gacha "
                "javob berilishini talab qilmoqda."
            ),
            is_start_node=True,
        )

        # Option 1: O'zim qaror qilaman
        node1 = ScenarioNode.objects.create(
            case_study=case1,
            title="Noto'g'ri qaror - O'zim hal qildim",
            content=(
                "Siz rahbar yo'qligida o'zingiz xatga javob "
                "yozdingiz va imzoladingiz. Bu jiddiy xatolik! "
                "Sizda bunday vakolat yo'q."
            ),
            is_end_node=True,
            is_fail_node=True,
        )

        ScenarioEdge.objects.create(
            from_node=start,
            to_node=node1,
            option_text="O'zim javob yozib imzolaymanù xat shoshilinch",
            feedback_text=(
                "NOTO'G'RI! Sizda rahbar nomidan hujjat "
                "imzolash vakolati yo'q. Bu huquqbuzarlikdir "
                "va intizomiy javobgarlikka olib keladi."
            ),
            xp_delta=-50,
        )

        # Option 2: O'rinbosar bilan maslahatlashaman
        node2 = ScenarioNode.objects.create(
            case_study=case1,
            title="To'g'ri qaror - O'rinbosar topish",
            content=(
                "Siz kadrlar bo'limiga murojaat qildingiz va "
                "rahbaringizning o'rinbosari kim ekanligini "
                "aniqladingiz. O'rinbosar xat bilan tanishdi va "
                "tegishli qaror qabul qildi."
            ),
            is_end_node=True,
            is_fail_node=False,
        )

        ScenarioEdge.objects.create(
            from_node=start,
            to_node=node2,
            option_text=(
                "Rahbarning o'rinbosari bilan maslahatlashaman"
            ),
            feedback_text=(
                "TO'G'RI! Rahbar yo'qligida uning "
                "o'rinbosari vakolat bilan ish yuritadi. "
                "Sizning harakatingiz qonun va qoidalarga to'liq "
                "mos keladi."
            ),
            xp_delta=50,
        )

        # Option 3: Kutib turaman
        node3 = ScenarioNode.objects.create(
            case_study=case1,
            title="Noto'g'ri qaror - Passiv munosabat",
            content=(
                "Siz rahbar qaytib kelguncha kutdingiz. "
                "Natijada xatga javob muddati o'tib ketdi "
                "va tashkilotga zarar yetdi."
            ),
            is_end_node=True,
            is_fail_node=True,
        )

        ScenarioEdge.objects.create(
            from_node=start,
            to_node=node3,
            option_text="Rahbar qaytguncha kutib turaman",
            feedback_text=(
                "NOTO'G'RI! Shoshilinch xatlarga o'z vaqtida "
                "javob berish majburiyati bor. Passiv munosabat "
                "ish intizomini buzishdir."
            ),
            xp_delta=-30,
        )

        # 2-Keys: Maxfiy hujjat bilan ishlash
        case2 = CaseStudy.objects.create(
            title="Maxfiy hujjat himoyasi",
            description=(
                "Sizga maxfiy hujjat topshirildi. "
                "Tushlik vaqti bo'ldi. Qanday harakat qilasiz?"
            ),
            xp_reward=80,
            is_active=True
        )

        # Start node
        start2 = ScenarioNode.objects.create(
            case_study=case2,
            title="Maxfiy hujjat bilan ishlash",
            content=(
                "Siz maxfiy belgisi bilan belgilangan hujjat "
                "ustida ishlayapsiz. Tushlik vaqti keldi va siz "
                "oshxonaga borishingiz kerak. Ish stolingizda "
                "maxfiy hujjat yotibdi."
            ),
            is_start_node=True,
        )

        # Option 1: Seyfga qo'yaman
        node2_1 = ScenarioNode.objects.create(
            case_study=case2,
            title="To'g'ri qaror - Seyfda saqlash",
            content=(
                "Siz hujjatni seyfga joylashtirib, uni "
                "qulflab chiqdingiz. Bu to'g'ri yechim! "
                "Maxfiy hujjatlar doimo maxsus joyda "
                "saqlanishi kerak."
            ),
            is_end_node=True,
            is_fail_node=False,
        )

        ScenarioEdge.objects.create(
            from_node=start2,
            to_node=node2_1,
            option_text="Hujjatni seyfga qo'yib, qulflab chiqaman",
            feedback_text=(
                "TO'G'RI! Maxfiy hujjatlar doimo maxsus "
                "saqlash joyida (seyf, maxfiy shkaf) bo'lishi "
                "kerak. Sizning xavfsizlik qoidalariga rioya "
                "qilganingiz mukammal!"
            ),
            xp_delta=40,
        )

        # Option 2: Stolda qoldiraman
        node2_2 = ScenarioNode.objects.create(
            case_study=case2,
            title="Noto'g'ri qaror - Ochiq qoldirish",
            content=(
                "Siz hujjatni stolda qoldirib chiqdingiz. "
                "Bu maxfiylik rejimini buzish! Jiddiy "
                "oqibatlarga olib kelishi mumkin."
            ),
            is_end_node=True,
            is_fail_node=True,
        )

        ScenarioEdge.objects.create(
            from_node=start2,
            to_node=node2_2,
            option_text="Stol yopiq, xona qulflangan - stolda qoldiraman",
            feedback_text=(
                "NOTO'G'RI! Maxfiy hujjatlarni hatto qulflangan "
                "xonada ham ochiq qoldirish mumkin emas. "
                "Bu maxfiylik qoidalarini qo'pol buzishdir."
            ),
            xp_delta=-40,
        )

        # Option 3: Hamkasbga topshiraman
        node2_3 = ScenarioNode.objects.create(
            case_study=case2,
            title="Noto'g'ri qaror - Boshqaga topshirish",
            content=(
                "Siz hujjatni hamkasbingizga \"kuzatib tur\" "
                "deb topshirdingiz. Bu noto'g'ri! Maxfiy hujjat "
                "faqat mas'ul shaxslar qo'lida bo'lishi mumkin."
            ),
            is_end_node=True,
            is_fail_node=True,
        )

        ScenarioEdge.objects.create(
            from_node=start2,
            to_node=node2_3,
            option_text="Ishonchli hamkasbga \"kuzatib tur\" deb topshiraman",
            feedback_text=(
                "NOTO'G'RI! Maxfiy hujjatni vakolatsiz shaxsga "
                "topshirish qat'iyan man etilgan. Faqat maxsus "
                "ruxsatnomasi bor shaxslargina maxfiy hujjat "
                "bilan ishlashi mumkin."
            ),
            xp_delta=-35,
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ {CaseStudy.objects.count()} ta demo keys yaratildi!'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'📊 Jami {ScenarioNode.objects.count()} ta node'
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f'🔗 Jami {ScenarioEdge.objects.count()} ta edge'
            )
        )
