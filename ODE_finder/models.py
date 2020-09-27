import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Create your models here.
class Experiment(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    csv_file = models.FileField(upload_to='experiments/', max_length=100)
    upload_date = models.DateTimeField('date uploaded', auto_now=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.csv_file.delete()
        super().delete(*args, **kwargs)


class SimulationResult(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    result_file = models.FileField(upload_to='results/', max_length=100)
    simulation_date = models.DateTimeField('date simulated', auto_now=True)

    def delete(self, *args, **kwargs):
        self.result_file.delete()
        super().delete(*args, **kwargs)