from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import ContestantForm
from .models import Contest
from application.models import Application
from django.contrib import messages


class ContestListView(ListView):
    model = Contest
    template_name = 'home.html'
    context_object_name = 'contests'
    ordering = ['date']


# class ContestDetailView(DetailView):
#     model = Contest
#     template_name = 'contest_detail.html'
#     context_object_name = 'object'


def contest_detail(request, pk):
    if request.method == 'POST':
        a_form = ContestantForm(request.POST, request.FILES)
        if a_form.is_valid():
            instance = a_form.save()
            contest = Contest.objects.get(id=pk)
            Application.objects.create(contest=contest, contestant=instance)
            messages.success(request, 'Ваша заявка усепешно принято!')
            return redirect('contestant-home')

    contest = Contest.objects.get(id=pk)
    a_form = ContestantForm()

    context = {
        'object': contest,
        'a_form': a_form
    }
    return render(request, 'contest_detail.html', context=context)


def application(request, pk):
    if request.method == 'POST':
        a_form = ContestantForm(request.POST, request.FILES)
        if a_form.is_valid():
            instance = a_form.save()
            contest = Contest.objects.get(id=pk)
            Application.objects.create(contest=contest, contestant=instance)
            messages.success(request, 'Ваша заявка усепешно принято!')
            return redirect('contestant-home')
    a_form = ContestantForm()
    context = {
        'a_form': a_form
    }
    return render(request, 'application.html', context=context)


def contest_application(request, pk):

    if request.is_ajax and request.method == "POST":

        return JsonResponse({'message': 'success'})

    contest_applications = Application.objects.filter(contest__id=pk)
    contest = contest_applications[0].contest
    context = {
        'contest': contest,
        'contest_applications': contest_applications
    }
    return render(request, 'contest_application.html', context=context)


def contest_application_update(request, pk):
    return redirect('contest-applications')
