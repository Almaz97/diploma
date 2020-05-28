from django.conf import settings
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from .forms import ContestantForm
from .models import Contest, ContestCommission
from application.models import Application
from django.contrib import messages
from django.core.mail import send_mail
import datetime


# class ContestListView(ListView):
#     model = Contest
#     template_name = 'home.html'
#     context_object_name = 'contests'
#     ordering = ['date']


def contest(request):

    contests = Contest.objects.all()
    context = {
        'contests': contests
    }

    if request.is_ajax and request.GET.get('date'):
        print('working')
        date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d')
        # data = json.loads(request.body)
        # date = data['date']
        # print(date)
        contests = Contest.objects.filter(created_at__lte=date)
        print(contests)
        context = {
            'contests': contests
        }

        return render(request, 'home.html', context=context)

    return render(request, 'home.html', context)

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

    created_date = contest.created_at.date()
    print(created_date)
    current_date = datetime.date.today()
    print(current_date)
    date_difference = current_date - created_date
    application_deadline = created_date + datetime.timedelta(days=31)
    is_actual = True
    if date_difference.days > 32:
        is_actual = True

    context = {
        'object': contest,
        'a_form': a_form,
        'is_actual': is_actual,
        'application_deadline': application_deadline,
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
        data = json.loads(request.body)
        application_id = data['application']
        contest_id = data['contest']
        confirmed = data['confirmed']
        applic = Application.objects.get(id=int(application_id))
        applic.checked = True
        applic.checked_by = request.user
        if confirmed:
            applic.confirmed = True
            message = 'Ваша заявка было рассмотрено. Мы рады сообщить Вам, что Вы допущены на отбор.'
        else:
            applic.confirmed = False
            message = 'Ваша заявка было рассмотрено. Вы не добущены на отбор. '
            reject_reason = data.get('message', None)
            if reject_reason:
                message += str(reject_reason)
        print('message')
        applic.save()
        subject = 'КГТУ им. Раззакова. Заявка на конкурс'
        from_email = settings.EMAIL_HOST_USER
        to_list = [applic.contestant.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return JsonResponse({'message': 'success'})

    contest_applications = Application.objects.filter(contest__id=pk)
    if request.user.is_commission:
        contest_applications = contest_applications.filter(checked=True)

    contest = contest_applications[0].contest
    context = {
        'contest': contest,
        'contest_applications': contest_applications
    }
    return render(request, 'contest_application.html', context=context)


def contest_application_update(request, pk):
    return redirect('contest-applications')


def commission_contests(request, pk):
    c_contests = ContestCommission.objects.filter(commission_id=pk).select_related('contest')
    contests = [c_contest.contest for c_contest in c_contests]
    context = {
        'contests': contests
    }
    return render(request, 'home.html', context=context)


def contest_review(request, pk_1, pk_2):
    application = Application.objects.filter(pk=pk_2).first()
    contestant = application.contestant
    context = {
        'application': application
    }
    return render(request, 'contest_review.html', context=context)


def contest_result(request, pk):
    contest_applications = Application.objects.filter(contest__id=pk)

    contest = contest_applications[0].contest
    context = {
        'contest': contest,
        'contest_applications': contest_applications
    }
    return render(request, 'contest_result.html', context=context)