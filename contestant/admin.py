from django.contrib import admin
from .models import ContestCommission, Contest, Contestant, ContestParticipant, ContestSummary

admin.site.register(ContestCommission)
admin.site.register(Contest)
admin.site.register(Contestant)
admin.site.register(ContestParticipant)
admin.site.register(ContestSummary)
