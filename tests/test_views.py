"""Ko'rinishlar uchun testlar."""
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

from courses.models import Course, Module, Lesson
from quizzes.models import Question, Answer, QuizAttempt
from accounts.models import Profile

User = get_user_model()


@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username="testuser", password="password123")
    # Profile signal or default check
    Profile.objects.get_or_create(user=user, defaults={"role": Profile.Role.IJROCHI})
    return user


@pytest.fixture
def rahbar_user(db):
    user = User.objects.create_user(username="rahbar", password="password123")
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.role = Profile.Role.RAHBAR
    profile.save()
    return user


@pytest.fixture
def sample_course(db):
    course = Course.objects.create(title="Sample Course", description="Description")
    module = Module.objects.create(course=course, title="Module 1")
    lesson = Lesson.objects.create(module=module, title="Lesson 1", content="Content")
    return course, module, lesson


@pytest.mark.django_db
def test_course_list_redirect_anonymous(client):
    url = reverse("courses:course_list")
    response = client.get(url)
    assert response.status_code == 302  # login-ga yo'naltiriladi


@pytest.mark.django_db
def test_course_list_authenticated(client, test_user, sample_course):
    client.login(username="testuser", password="password123")
    url = reverse("courses:course_list")
    response = client.get(url)
    assert response.status_code == 200
    assert "Sample Course" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_lesson_detail(client, test_user, sample_course):
    client.login(username="testuser", password="password123")
    course, module, lesson = sample_course
    url = reverse("courses:lesson_detail", kwargs={"pk": lesson.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "Lesson 1" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_manager_dashboard_permissions(client, test_user, rahbar_user):
    # Oddiy foydalanuvchiga ruxsat berilmasligi kerak (yoki 403 yoki redirect)
    client.login(username="testuser", password="password123")
    url = reverse("progress:manager_dashboard")
    response = client.get(url)
    assert response.status_code in [302, 403]

    # Rahbarga ruxsat berilishi kerak
    client.login(username="rahbar", password="password123")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_form_instantiation():
    from accounts.forms import RegisterForm
    form = RegisterForm()
    assert "username" in form.fields
    assert "email" in form.fields
    assert "password1" in form.fields
    assert "password2" in form.fields


@pytest.mark.django_db
def test_certificate_auto_generation(sample_course, test_user):
    from progress.models import Progress, Certificate
    from django.utils import timezone
    course, module, lesson = sample_course
    
    # Initially, no certificates
    assert Certificate.objects.filter(user=test_user, course=course).count() == 0
    
    # Complete the lesson
    Progress.objects.create(
        user=test_user,
        lesson=lesson,
        completed=True,
        completed_at=timezone.now()
    )
    
    # All lessons completed, verify Certificate generated
    assert Certificate.objects.filter(user=test_user, course=course).count() == 1


