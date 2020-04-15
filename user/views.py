from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm
from django.contrib import messages


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }
    return render(request, 'profile.html', context=context)