from django.shortcuts import render
from django.http import HttpResponse

from contestant.models import Contest


def homepage(request):
    context = {
        'contests': Contest.objects.all()
    }
    return render(request, 'home.html', context)
