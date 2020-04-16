from django.db import models

from contestant.models import Contest, Contestant
from user.models import User


class Application(models.Model):
    class Meta:
        db_table = 'application'

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return f'Заявка на конкурс: {self.contest.name}'
