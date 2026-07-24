"""Quizzes app view'lari — dars (Module) va mavzu (Lesson) darajasida."""
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from courses.models import Lesson, Module
from .models import Answer, Question, QuizAttempt


class TakeQuizView(LoginRequiredMixin, View):
    """Dars (Module) darajasidagi test topshirish sahifasi."""

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        questions_qs = module.questions.prefetch_related("answers").all()

        if not questions_qs.exists():
            return redirect("courses:course_detail", pk=module.course.id)

        # Urinishlar sonini tekshirish
        attempts_count = QuizAttempt.objects.filter(user=request.user, module=module, lesson=None).count()
        if module.max_attempts and attempts_count >= module.max_attempts:
            from django.contrib import messages
            messages.error(request, f"Siz ushbu dars testini topshirish urinishlari sonidan ({module.max_attempts} marta) oshib ketdingiz!")
            return redirect("courses:course_detail", pk=module.course.id)

        # Shuffle questions
        questions = list(questions_qs)
        random.shuffle(questions)

        # Shuffle answers for each question and prepare session data
        answers_session_data = {}
        for question in questions:
            answers = list(question.answers.all())
            random.shuffle(answers)
            question.shuffled_answers = answers
            answers_session_data[str(question.id)] = [ans.id for ans in answers]

        # Store in session
        request.session[f"quiz_questions_{module.id}"] = [q.id for q in questions]
        request.session[f"quiz_answers_{module.id}"] = answers_session_data

        context = {
            "module": module,
            "questions": questions,
            "quiz_type": "module",
        }
        return render(request, "quizzes/quiz_take.html", context)


class SubmitQuizView(LoginRequiredMixin, View):
    """Dars (Module) darajasidagi test natijalarini hisoblash va saqlash."""

    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        
        # Retrieve selected questions from session, fallback to all if not found
        question_ids = request.session.get(f"quiz_questions_{module.id}")
        if question_ids:
            questions_map = {q.id: q for q in module.questions.all()}
            questions = [questions_map[q_id] for q_id in question_ids if q_id in questions_map]
        else:
            questions = list(module.questions.all())

        total_questions = len(questions)

        if total_questions == 0:
            return redirect("courses:course_detail", pk=module.course.id)

        # Urinishlar sonini tekshirish
        attempts_count = QuizAttempt.objects.filter(user=request.user, module=module, lesson=None).count()
        if module.max_attempts and attempts_count >= module.max_attempts:
            from django.contrib import messages
            messages.error(request, "Siz ushbu dars testini topshirish urinishlari sonidan oshib ketdingiz!")
            return redirect("courses:course_detail", pk=module.course.id)

        # Retrieve shuffled answers metadata
        shuffled_answers_data = request.session.get(f"quiz_answers_{module.id}", {})

        correct_count = 0
        incorrect_details = []

        for question in questions:
            selected_answer_id = request.POST.get(f"question_{question.id}")
            
            # Reconstruct exact shuffled answer order
            shuffled_ids = shuffled_answers_data.get(str(question.id))
            if shuffled_ids:
                answers_map = {ans.id: ans for ans in question.answers.all()}
                answers = [answers_map[ans_id] for ans_id in shuffled_ids if ans_id in answers_map]
            else:
                answers = list(question.answers.all())
            
            correct_answer = None
            correct_answer_text = "Noma'lum"
            for idx, ans in enumerate(answers):
                if ans.is_correct:
                    correct_answer = ans
                    letter = chr(65 + idx)
                    correct_answer_text = f"{letter}) {ans.text}"
                    break

            selected_answer_text = "Javob berilmagan"
            is_correct = False

            if selected_answer_id:
                try:
                    selected_answer = Answer.objects.get(id=selected_answer_id, question=question)
                    selected_letter = "Noma'lum"
                    for idx, ans in enumerate(answers):
                        if ans.id == selected_answer.id:
                            selected_letter = chr(65 + idx)
                            break
                    selected_answer_text = f"{selected_letter}) {selected_answer.text}"
                    
                    if selected_answer.is_correct:
                        correct_count += 1
                        is_correct = True
                except Answer.DoesNotExist:
                    pass

            if not is_correct:
                incorrect_details.append({
                    "question_text": question.text,
                    "selected_answer": selected_answer_text,
                    "correct_answer": correct_answer_text,
                })

        score = int((correct_count / total_questions) * 100)
        passed = score >= 70

        attempt = QuizAttempt.objects.create(
            user=request.user,
            module=module,
            score=score,
            passed=passed
        )

        request.session["last_quiz_incorrect"] = incorrect_details

        # Clean session data
        request.session.pop(f"quiz_questions_{module.id}", None)
        request.session.pop(f"quiz_answers_{module.id}", None)

        return redirect("quizzes:attempt_result", attempt_id=attempt.id)


class TakeLessonQuizView(LoginRequiredMixin, View):
    """Mavzu (Lesson) darajasidagi test topshirish sahifasi."""

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        questions_qs = lesson.questions.prefetch_related("answers").all()

        if not questions_qs.exists():
            return redirect("courses:lesson_detail", pk=lesson.id)

        # Urinishlar sonini tekshirish
        attempts_count = QuizAttempt.objects.filter(user=request.user, lesson=lesson).count()
        if lesson.max_attempts and attempts_count >= lesson.max_attempts:
            from django.contrib import messages
            messages.error(request, f"Siz ushbu mavzu testini topshirish urinishlari sonidan ({lesson.max_attempts} marta) oshib ketdingiz!")
            return redirect("courses:lesson_detail", pk=lesson.id)

        # Shuffle questions
        questions = list(questions_qs)
        random.shuffle(questions)

        # Shuffle answers and prepare session data
        answers_session_data = {}
        for question in questions:
            answers = list(question.answers.all())
            random.shuffle(answers)
            question.shuffled_answers = answers
            answers_session_data[str(question.id)] = [ans.id for ans in answers]

        # Store in session
        request.session[f"quiz_questions_lesson_{lesson.id}"] = [q.id for q in questions]
        request.session[f"quiz_answers_lesson_{lesson.id}"] = answers_session_data

        context = {
            "lesson": lesson,
            "module": lesson.module,
            "questions": questions,
            "quiz_type": "lesson",
        }
        return render(request, "quizzes/quiz_take.html", context)


class SubmitLessonQuizView(LoginRequiredMixin, View):
    """Mavzu (Lesson) darajasidagi test natijalarini hisoblash va saqlash."""

    def post(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        
        # Retrieve selected questions from session, fallback to all if not found
        question_ids = request.session.get(f"quiz_questions_lesson_{lesson.id}")
        if question_ids:
            questions_map = {q.id: q for q in lesson.questions.all()}
            questions = [questions_map[q_id] for q_id in question_ids if q_id in questions_map]
        else:
            questions = list(lesson.questions.all())

        total_questions = len(questions)

        if total_questions == 0:
            return redirect("courses:lesson_detail", pk=lesson.id)

        # Urinishlar sonini tekshirish
        attempts_count = QuizAttempt.objects.filter(user=request.user, lesson=lesson).count()
        if lesson.max_attempts and attempts_count >= lesson.max_attempts:
            from django.contrib import messages
            messages.error(request, "Siz ushbu mavzu testini topshirish urinishlari sonidan oshib ketdingiz!")
            return redirect("courses:lesson_detail", pk=lesson.id)

        # Retrieve shuffled answers metadata
        shuffled_answers_data = request.session.get(f"quiz_answers_lesson_{lesson.id}", {})

        correct_count = 0
        incorrect_details = []

        for question in questions:
            selected_answer_id = request.POST.get(f"question_{question.id}")
            
            # Reconstruct exact shuffled answer order
            shuffled_ids = shuffled_answers_data.get(str(question.id))
            if shuffled_ids:
                answers_map = {ans.id: ans for ans in question.answers.all()}
                answers = [answers_map[ans_id] for ans_id in shuffled_ids if ans_id in answers_map]
            else:
                answers = list(question.answers.all())
            
            correct_answer = None
            correct_answer_text = "Noma'lum"
            for idx, ans in enumerate(answers):
                if ans.is_correct:
                    correct_answer = ans
                    letter = chr(65 + idx)
                    correct_answer_text = f"{letter}) {ans.text}"
                    break

            selected_answer_text = "Javob berilmagan"
            is_correct = False

            if selected_answer_id:
                try:
                    selected_answer = Answer.objects.get(id=selected_answer_id, question=question)
                    selected_letter = "Noma'lum"
                    for idx, ans in enumerate(answers):
                        if ans.id == selected_answer.id:
                            selected_letter = chr(65 + idx)
                            break
                    selected_answer_text = f"{selected_letter}) {selected_answer.text}"
                    
                    if selected_answer.is_correct:
                        correct_count += 1
                        is_correct = True
                except Answer.DoesNotExist:
                    pass

            if not is_correct:
                incorrect_details.append({
                    "question_text": question.text,
                    "selected_answer": selected_answer_text,
                    "correct_answer": correct_answer_text,
                })

        score = int((correct_count / total_questions) * 100)
        passed = score >= 70

        attempt = QuizAttempt.objects.create(
            user=request.user,
            module=lesson.module,
            lesson=lesson,
            score=score,
            passed=passed
        )

        if passed:
            from django.utils import timezone
            from progress.models import Progress
            Progress.objects.update_or_create(
                user=request.user,
                lesson=lesson,
                defaults={"completed": True, "completed_at": timezone.now()}
            )

        request.session["last_quiz_incorrect"] = incorrect_details

        # Clean session data
        request.session.pop(f"quiz_questions_lesson_{lesson.id}", None)
        request.session.pop(f"quiz_answers_lesson_{lesson.id}", None)

        return redirect("quizzes:attempt_result", attempt_id=attempt.id)





class AttemptResultView(LoginRequiredMixin, View):
    """Test urinishi natijasini ko'rsatish."""

    def get(self, request, attempt_id):
        attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)
        incorrect_questions = request.session.pop("last_quiz_incorrect", [])

        context = {
            "attempt": attempt,
            "incorrect_questions": incorrect_questions,
        }
        return render(request, "quizzes/attempt_result.html", context)
