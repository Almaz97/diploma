from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Employee(models.Model):
    class Meta:
        db_table = 'employee'

    POSITION = [
        ('commission', 'Commission'),
        ('secretary', 'Secretary'),
        ('hr', 'HR')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=25, choices=POSITION)


class Contest(models.Model):
    class Meta:
        db_table = 'contest'

    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField()
    description = models.TextField()
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Contestant(models.Model):
    class Meta:
        db_table = 'contestant'

    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    photo = models.ImageField()


class ContestParticipant(models.Model):
    class Meta:
        db_table = 'contest_participant'

    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='contestants')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)


class ContestCommission(models.Model):
    class Meta:
        db_table = 'contest_commission'

    commission = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='commissions')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)


class ContestSummary(models.Model):
    class Meta:
        db_table = 'contest_summary'

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='summaries')
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='summaries')
    commission = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='summaries')
    comment = models.TextField()
