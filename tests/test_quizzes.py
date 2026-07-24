import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from courses.models import Course, Module, Lesson
from quizzes.models import Question, Answer, QuizAttempt

User = get_user_model()

@pytest.fixture
def test_user(db):
    return User.objects.create_user(username="testuser", password="password123")

@pytest.fixture
def sample_quiz_data(db):
    course = Course.objects.create(title="Test Course")
    module = Module.objects.create(course=course, title="Test Module", max_attempts=5)
    lesson = Lesson.objects.create(module=module, title="Test Lesson", max_attempts=5)
    
    # Create 3 questions for the lesson/module
    q1 = Question.objects.create(module=module, lesson=lesson, text="Question 1")
    Answer.objects.create(question=q1, text="Ans 1.1", is_correct=True)
    Answer.objects.create(question=q1, text="Ans 1.2", is_correct=False)
    Answer.objects.create(question=q1, text="Ans 1.3", is_correct=False)
    Answer.objects.create(question=q1, text="Ans 1.4", is_correct=False)
    
    q2 = Question.objects.create(module=module, lesson=lesson, text="Question 2")
    Answer.objects.create(question=q2, text="Ans 2.1", is_correct=False)
    Answer.objects.create(question=q2, text="Ans 2.2", is_correct=True)
    Answer.objects.create(question=q2, text="Ans 2.3", is_correct=False)
    Answer.objects.create(question=q2, text="Ans 2.4", is_correct=False)
    
    q3 = Question.objects.create(module=module, lesson=lesson, text="Question 3")
    Answer.objects.create(question=q3, text="Ans 3.1", is_correct=False)
    Answer.objects.create(question=q3, text="Ans 3.2", is_correct=False)
    Answer.objects.create(question=q3, text="Ans 3.3", is_correct=True)
    Answer.objects.create(question=q3, text="Ans 3.4", is_correct=False)

    return course, module, lesson

@pytest.mark.django_db
def test_lesson_quiz_shuffling(client, test_user, sample_quiz_data):
    client.login(username="testuser", password="password123")
    course, module, lesson = sample_quiz_data
    
    url = reverse("quizzes:lesson_quiz_take", kwargs={"lesson_id": lesson.id})
    response = client.get(url)
    assert response.status_code == 200
    
    # Check that questions and answers are stored in session
    session = client.session
    q_ids_key = f"quiz_questions_lesson_{lesson.id}"
    a_map_key = f"quiz_answers_lesson_{lesson.id}"
    
    assert q_ids_key in session
    assert a_map_key in session
    
    # Check that all questions are present
    assert len(session[q_ids_key]) == 3
    assert set(session[q_ids_key]) == {q.id for q in lesson.questions.all()}

@pytest.mark.django_db
def test_lesson_quiz_submission(client, test_user, sample_quiz_data):
    client.login(username="testuser", password="password123")
    course, module, lesson = sample_quiz_data
    
    # Fetch to populate session
    url_take = reverse("quizzes:lesson_quiz_take", kwargs={"lesson_id": lesson.id})
    client.get(url_take)
    
    session = client.session
    q_ids_key = f"quiz_questions_lesson_{lesson.id}"
    a_map_key = f"quiz_answers_lesson_{lesson.id}"
    
    shuffled_questions = session[q_ids_key]
    shuffled_answers = session[a_map_key]
    
    # Submit one correct and two incorrect answers
    # Find correct answer id for the first question in shuffled order
    q1_id = shuffled_questions[0]
    q1 = Question.objects.get(id=q1_id)
    correct_ans_1 = q1.answers.get(is_correct=True)
    
    # Submit incorrect for the second question
    q2_id = shuffled_questions[1]
    q2 = Question.objects.get(id=q2_id)
    incorrect_ans_2 = q2.answers.filter(is_correct=False).first()
    
    # No answer for the third question
    
    post_data = {
        f"question_{q1_id}": correct_ans_1.id,
        f"question_{q2_id}": incorrect_ans_2.id,
    }
    
    url_submit = reverse("quizzes:lesson_quiz_submit", kwargs={"lesson_id": lesson.id})
    response = client.post(url_submit, data=post_data)
    
    assert response.status_code == 302  # redirects to result
    
    # Check attempt is created
    attempt = QuizAttempt.objects.latest("id")
    assert attempt.user == test_user
    assert attempt.lesson == lesson
    # 1 correct out of 3 total = 33%
    assert attempt.score == 33
    assert attempt.passed is False
    
    # Verify incorrect details log has 2 items (questions 2 and 3)
    last_quiz_incorrect = client.session.get("last_quiz_incorrect")
    assert len(last_quiz_incorrect) == 2
    
    # Check that session clean up works
    assert q_ids_key not in client.session
    assert a_map_key not in client.session
