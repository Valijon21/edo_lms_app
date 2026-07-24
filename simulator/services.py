from django.utils import timezone
from .models import SimulationScenario, SimulationSession


def process_simulator_action(user, scenario_id, action_type, payload=None):
    """Foydalanuvchining simulyatordagi harakatini tekshiradi va sessiyani yangilaydi.

    Args:
        user: Auth User obyekti
        scenario_id: SimulationScenario PK
        action_type: Foydalanuvchi bajargan harakat kodi (masalan: 'open_doc', 'add_resolution', 'sign_doc')
        payload: Harakat bilan birga kelgan ma'lumotlar (dict)

    Returns:
        dict: {
            'success': bool,
            'message': str,
            'current_step': int,
            'total_steps': int,
            'is_completed': bool,
            'xp_awarded': int,
            'feedback': str,
            'next_step_hint': str
        }
    """
    if payload is None:
        payload = {}

    try:
        scenario = SimulationScenario.objects.get(pk=scenario_id, is_active=True)
    except SimulationScenario.DoesNotExist:
        return {
            'success': False,
            'message': "Ssenariy topilmadi yoki faol emas.",
            'is_completed': False,
        }

    session, _ = SimulationSession.objects.get_or_create(
        user=user,
        scenario=scenario
    )

    if session.is_completed:
        return {
            'success': True,
            'message': "Ushbu ssenariy allaqachon muvaffaqiyatli yakunlangan!",
            'current_step': len(scenario.expected_steps),
            'total_steps': len(scenario.expected_steps),
            'is_completed': True,
            'xp_awarded': 0,
            'feedback': "Barcha bosqichlar bajariilgan.",
            'next_step_hint': ""
        }

    steps = scenario.expected_steps
    curr_idx = session.current_step_index

    if curr_idx >= len(steps):
        session.is_completed = True
        session.completed_at = timezone.now()
        session.save()
        return {
            'success': True,
            'message': "Ssenariy yakunlandi!",
            'is_completed': True,
            'xp_awarded': 0
        }

    expected_step = steps[curr_idx]
    expected_action = expected_step.get("action")

    # Harakat kodini solishtirish
    if action_type != expected_action:
        return {
            'success': False,
            'message': f"Noto'g'ri harakat! Kutilgan harakat: '{expected_step.get('title', expected_action)}'.",
            'current_step': curr_idx + 1,
            'total_steps': len(steps),
            'is_completed': False,
            'feedback': expected_step.get("error_hint", "Iltimos, ko'rsatmaga amal qiling."),
            'next_step_hint': expected_step.get("description", "")
        }

    # Qo'shimcha maydonlar talabini tekshirish
    required_fields = expected_step.get("required_fields", [])
    for field in required_fields:
        if not payload.get(field):
            return {
                'success': False,
                'message': f"Majburiy maydon yetishmayapti: {field}",
                'current_step': curr_idx + 1,
                'total_steps': len(steps),
                'is_completed': False,
                'feedback': f"'{field}' maydonini to'ldiring.",
                'next_step_hint': expected_step.get("description", "")
            }

    # Muvaffaqiyatli harakatni qayd etish
    action_log = {
        'step': curr_idx + 1,
        'action': action_type,
        'payload': payload,
        'timestamp': timezone.now().isoformat()
    }
    performed = list(session.performed_actions)
    performed.append(action_log)

    session.performed_actions = performed
    session.current_step_index = curr_idx + 1
    xp_awarded = 0

    is_finished = session.current_step_index >= len(steps)
    if is_finished:
        session.is_completed = True
        session.score = scenario.xp_reward
        session.completed_at = timezone.now()
        xp_awarded = scenario.xp_reward

        # Gamifikation profilliga XP ball qo'shish
        _award_gamification_xp(user, scenario.xp_reward, scenario.title)

    session.save()

    next_hint = ""
    if not is_finished:
        next_hint = steps[session.current_step_index].get("description", "")

    return {
        'success': True,
        'message': expected_step.get("success_message", "Bosqich muvaffaqiyatli bajarildi!"),
        'current_step': session.current_step_index,
        'total_steps': len(steps),
        'is_completed': is_finished,
        'xp_awarded': xp_awarded,
        'feedback': expected_step.get("feedback", "Barakalla! Keyingi qadamga o'ting."),
        'next_step_hint': next_hint
    }


def _award_gamification_xp(user, xp_amount, title):
    """Gamifikatsiya profiliga va logiga XP qo'shadi."""
    try:
        from gamification.services import reward_user_xp
        reward_user_xp(user, "SIMULATOR", xp_amount)
    except Exception:
        pass
