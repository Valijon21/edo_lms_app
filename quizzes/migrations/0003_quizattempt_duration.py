# Generated manually for adding duration to QuizAttempt

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quizzes", "0002_question_lesson_quizattempt_lesson"),
    ]

    operations = [
        migrations.AddField(
            model_name="quizattempt",
            name="duration",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Sarflangan vaqt (soniyalarda)"
            ),
        ),
    ]
