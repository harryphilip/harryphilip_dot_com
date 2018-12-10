from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

# Create your models here.


class Plan(models.Model):
    DAYS_TO_COMPLETE = 1001

    # Class to store 101 in 1,001 list
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def end_date(self):
        """Tests that end date is properly calculated."""
        return self.start_date + timedelta(days=self.DAYS_TO_COMPLETE)

    def days_left(self, current_date=None):
        if not(current_date):
            current_date = datetime.now()
        dif = self.end_date()-current_date
        return dif.days

    def pct_done(self, current_date=None):
        if not(current_date):
            current_date = datetime.now()
        completed_tasks = self.activity_set.filter(completion_date__lte=current_date).count()
        total_tasks = self.activity_set.all().count()
        return completed_tasks / total_tasks

class Activity(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(Plan, models.PROTECT)
    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    definition_of_done = models.TextField()
    completion_date = models.DateField(null=True)
    notes = models.TextField()


