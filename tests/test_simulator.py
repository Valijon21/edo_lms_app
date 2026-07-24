import pytest
import json
from django.urls import reverse
from django.contrib.auth import get_user_model

from simulator.models import SimulationScenario, SimulationSession, DocumentType, DifficultyLevel
from simulator.services import process_simulator_action
from gamification.models import UserGamificationProfile, GamificationActivityLog

User = get_user_model()


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", password="password123")
    UserGamificationProfile.objects.get_or_create(user=user)
    return user


@pytest.fixture
def sample_scenario(db):
    return SimulationScenario.objects.create(
        title="Test Kiruvchi Xat",
        doc_type=DocumentType.KIRUVCHI,
        difficulty=DifficultyLevel.EASY,
        description="Test ssenariy tavsifi",
        xp_reward=100,
        initial_doc_data={
            "doc_number": "111",
            "doc_date": "2026-07-22",
            "sender": "Test Vazirlik"
        },
        expected_steps=[
            {
                "action": "open_doc",
                "title": "Hujjatni ochish",
                "description": "Hujjatni bosing va oching.",
                "error_hint": "Hujjatni oching.",
                "success_message": "Ochildi!",
                "feedback": "Barakalla!",
                "required_fields": []
            },
            {
                "action": "add_resolution",
                "title": "Rezolyutsiya yozish",
                "description": "Rezolyutsiyani kiriting.",
                "error_hint": "Rezolyutsiya maydonlarini to'ldiring.",
                "success_message": "Saqlandi!",
                "feedback": "Rezolyutsiya kiritildi.",
                "required_fields": ["executor", "text"]
            }
        ]
    )


@pytest.mark.django_db
def test_scenario_and_session_creation(test_user, sample_scenario):
    assert SimulationScenario.objects.count() == 1
    session, created = SimulationSession.objects.get_or_create(
        user=test_user,
        scenario=sample_scenario
    )
    assert created is True
    assert session.current_step_index == 0
    assert session.is_completed is False


@pytest.mark.django_db
def test_process_action_validation(test_user, sample_scenario):
    # 1. Noto'g'ri harakat bajarilganda (open_doc o'rniga boshqa narsa)
    res = process_simulator_action(test_user, sample_scenario.id, "add_resolution", {})
    assert res["success"] is False
    assert "Noto'g'ri harakat!" in res["message"]
    
    # 2. To'g'ri birinchi harakat (open_doc)
    res = process_simulator_action(test_user, sample_scenario.id, "open_doc", {})
    assert res["success"] is True
    assert res["current_step"] == 1
    assert res["is_completed"] is False

    # 3. Ikkinchi harakatda majburiy maydon yetishmasa (executor, text)
    res = process_simulator_action(test_user, sample_scenario.id, "add_resolution", {"text": "Maslahat"})
    assert res["success"] is False
    assert "Majburiy maydon yetishmayapti" in res["message"]

    # 4. Ikkinchi harakatni to'liq bajarish (Ssenariy yakunlanishi va XP berilishi)
    profile = UserGamificationProfile.objects.get(user=test_user)
    assert profile.total_xp == 0

    res = process_simulator_action(test_user, sample_scenario.id, "add_resolution", {"executor": "A. Qodirov", "text": "Taklif"})
    assert res["success"] is True
    assert res["is_completed"] is True
    assert res["xp_awarded"] == 100

    profile.refresh_from_db()
    assert profile.total_xp == 100
    
    # Gamification logs mavjudligini tekshirish
    assert GamificationActivityLog.objects.filter(user=test_user, activity_type="SIMULATOR").count() == 1


@pytest.mark.django_db
def test_simulator_views_and_api(client, test_user, sample_scenario):
    client.login(username="testuser", password="password123")

    # 1. List View
    url_list = reverse("simulator:list")
    response = client.get(url_list)
    assert response.status_code == 200
    assert sample_scenario.title in response.content.decode("utf-8")

    # 2. Detail View
    url_detail = reverse("simulator:detail", kwargs={"pk": sample_scenario.id})
    response = client.get(url_detail)
    assert response.status_code == 200
    assert sample_scenario.title in response.content.decode("utf-8")

    # 3. Action API (REST POST)
    url_action = reverse("simulator:action_api", kwargs={"pk": sample_scenario.id})
    
    # open_doc API post
    data = {"action_type": "open_doc", "payload": {}}
    response = client.post(
        url_action,
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert res_json["current_step"] == 1

    # 4. Reset View
    url_reset = reverse("simulator:reset", kwargs={"pk": sample_scenario.id})
    response = client.post(url_reset)
    assert response.status_code == 302 # Redirects back to detail page
    
    # Verify session is deleted
    assert SimulationSession.objects.filter(user=test_user, scenario=sample_scenario).count() == 0
