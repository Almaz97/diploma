from django.db import models
# from django.contrib.auth.models import User
from user.models import User
from django.core.validators import MinValueValidator


class VacancyPosition(models.Model):
    class Meta:
        db_table = 'vacancy_position'

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Contest(models.Model):
    class Meta:
        db_table = 'contest'

    name = models.CharField(max_length=255)
    image = models.ImageField(null=True, blank=True)
    date = models.DateTimeField()
    description = models.TextField()
    vacancy_position = models.ForeignKey(VacancyPosition, on_delete=models.PROTECT)
    required_documents = models.FileField(default='contest_docs/trebuyemiye_documenti.zip')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contestant(models.Model):
    class Meta:
        db_table = 'contestant'

    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    documents = models.FileField(upload_to='contestant_docs')

    def __str__(self):
        return self.full_name


class ContestParticipant(models.Model):
    class Meta:
        db_table = 'contest_participant'

    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='contestants')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)


class ContestCommission(models.Model):
    class Meta:
        db_table = 'contest_commission'

    commission = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commissions')
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)


class ContestSummary(models.Model):
    class Meta:
        db_table = 'contest_summary'

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='summaries')
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name='summaries')
    commission = models.ForeignKey(User, on_delete=models.CASCADE, related_name='summaries')
    comment = models.TextField()
