from django.views.generic import ListView, DetailView
from .models import Contest


class ContestListView(ListView):
    model = Contest
    template_name = 'home.html'
    context_object_name = 'contests'
    ordering = ['date']


class ContestDetailView(DetailView):
    model = Contest
    template_name = 'contest_detail.html'
    context_object_name = 'object'
