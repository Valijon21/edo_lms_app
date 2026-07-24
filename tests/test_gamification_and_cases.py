import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from progress.models import Progress
from quizzes.models import QuizAttempt
from gamification.models import UserGamificationProfile, GamificationActivityLog
from case_studies.models import CaseStudy, ScenarioNode, ScenarioEdge, UserCaseProgress
from case_studies.services import start_case_study, submit_case_decision

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="gamer1", password="password123")

@pytest.fixture
def test_setup(db):
    from courses.models import Course, Module, Lesson
    course = Course.objects.create(title="Edo basics", description="LMS basics")
    module = Module.objects.create(course=course, title="Module 1")
    lesson = Lesson.objects.create(module=module, title="Lesson 1", content="Content")
    return course, module, lesson

@pytest.mark.django_db
def test_lesson_completion_awards_xp(test_user, test_setup):
    course, module, lesson = test_setup
    Progress.objects.create(
        user=test_user,
        lesson=lesson,
        completed=True,
        completed_at=timezone.now()
    )
    profile = UserGamificationProfile.objects.get(user=test_user)
    assert profile.total_xp == 10
    assert GamificationActivityLog.objects.filter(user=test_user, activity_type=f"lesson_complete_{lesson.id}").exists()

@pytest.mark.django_db
def test_quiz_completion_awards_xp(test_user, test_setup):
    course, module, lesson = test_setup
    QuizAttempt.objects.create(
        user=test_user,
        module=module,
        lesson=lesson,
        score=80,
        passed=True
    )
    profile = UserGamificationProfile.objects.get(user=test_user)
    assert profile.total_xp == 20

    # No duplicate award
    QuizAttempt.objects.create(
        user=test_user,
        module=module,
        lesson=lesson,
        score=90,
        passed=True
    )
    profile.refresh_from_db()
    assert profile.total_xp == 20

@pytest.mark.django_db
def test_case_study_graph_traversal(test_user):
    case = CaseStudy.objects.create(title="Test Case", description="Testing graphs", xp_reward=50)
    node_start = ScenarioNode.objects.create(case_study=case, title="Start", content="Start here", is_start_node=True)
    node_middle = ScenarioNode.objects.create(case_study=case, title="Middle", content="Middle path")
    node_end = ScenarioNode.objects.create(case_study=case, title="End", content="The End", is_end_node=True)
    edge1 = ScenarioEdge.objects.create(from_node=node_start, to_node=node_middle, option_text="Go mid", xp_delta=10)
    edge2 = ScenarioEdge.objects.create(from_node=node_middle, to_node=node_end, option_text="Go end", xp_delta=15)

    progress = start_case_study(test_user, case)
    assert progress.current_node == node_start
    assert progress.score == 0

    progress, feedback, xp_earned = submit_case_decision(test_user, case.id, edge1.id)
    assert progress.current_node == node_middle
    assert progress.score == 10
    assert xp_earned == 10

    progress, feedback, xp_earned = submit_case_decision(test_user, case.id, edge2.id)
    assert progress.current_node == node_end
    assert progress.score == 25
    assert progress.is_completed

    profile = UserGamificationProfile.objects.get(user=test_user)
    assert profile.total_xp == 10 + 15 + 50
