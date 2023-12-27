from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User

from app.models import Question, Answer, Profile, Tag, questionLike, answerLike, profileLike

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        users = [
            User(
                username=fake.bothify(text='????????????'),
                password=fake.password()
            ) for _ in range(ratio)
        ]
        User.objects.bulk_create(users)
        users = User.objects.all()

        profiles = [
            Profile(
                rating=fake.pyint(),
                user=users[i]
            ) for i in range(ratio)
        ]
        Profile.objects.bulk_create(profiles)
        profiles = Profile.objects.all()
        profiles_count = profiles.count()

        tags = [
            Tag(
                tag_name=fake.bothify(text='??????'),
            ) for _ in range(ratio)
        ]
        Tag.objects.bulk_create(tags)
        tags = Tag.objects.all()
        tags_count = tags.count()

        questions = [
            Question(
                title=fake.sentence(nb_words=10),
                content=fake.sentence(nb_words=30),
                author=profiles[fake.random_int(min=0, max=profiles_count - 1)],
                rating=fake.random_int(min=0, max=10000),
            ) for _ in range(ratio * 10)
        ]
        Question.objects.bulk_create(questions)
        questions = Question.objects.all()
        questions_count = questions.count()

        for i in range(ratio * 10):
            for _ in range(0, 1):
                questions[i].tags.add(tags[fake.random_int(min=0, max=tags_count - 1)])
        Question.objects.update()

        answers = [
            Answer(
                content=fake.sentence(nb_words=20),
                author=profiles[fake.random_int(min=0, max=profiles_count - 1)],
                correct=fake.pybool(),
                question=questions[fake.random_int(min=0, max=questions_count - 1)],
                rating=fake.random_int(min=0, max=10000),
            ) for _ in range(ratio * 100)
        ]
        Answer.objects.bulk_create(answers)
        answers = Answer.objects.all()
        answers_count = answers.count()

        question_likes = [
            questionLike(
                question=questions[fake.random_int(min=0, max=questions_count - 1)],
                owner=profiles[fake.random_int(min=0, max=profiles_count - 1)],
                value=fake.pybool()
            ) for _ in range(0, ratio)
        ]
        questionLike.objects.bulk_create(question_likes * 100)

        answers_likes = [
            answerLike(
                answer=answers[fake.random_int(min=0, max=answers_count - 1)],
                owner=profiles[fake.random_int(min=0, max=profiles_count - 1)],
                value=fake.pybool()
            ) for _ in range(ratio)
        ]
        answerLike.objects.bulk_create(answers_likes * 100)
