from django.db import models

from contestant.models import Contest, Employee, Contestant


class Application(models.Model):
    class Meta:
        db_table = 'application'

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    checked_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    required_document = models.FileField()
    checked = models.BooleanField(default=False)

