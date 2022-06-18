import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), True)
 
 
class QuestionIndexViewTests(TestCase):
    
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_questions'], [])
    
    def test_past_question(self):
        question = create_question(question="Balls?", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions'], [question])
    
    def test_future_question(self):
        question = create_question(question="Balls?", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_questions'], [])
    
    def test_future_and_past_question(self):
        future = create_question(question="Balls?", days=30)
        past = create_question(question="Balls?", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions'], [past])
    
    def test_past_two_questions(self):
        past1 = create_question(question="Balls?", days=-20)
        past2 = create_question(question="Balls?", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_questions'], [past1, past2])

class QuestionDetailViewTests(TestCase):
    
    def test_past_question(self):
        past = create_question(question="Balls?", days=-30)
        response = self.client.get(reverse('polls:detail', args=(past.id,)))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, past.question_text)
    
    def test_future_question(self):
        future = create_question(question="Balls?", days=30)
        response = self.client.get(reverse('polls:detail', args=(future.id,)))
        self.assertEquals(response.status_code, 404)


def create_question(question, days):
    """
    Create a question with the given `question` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question, pub_date=time)