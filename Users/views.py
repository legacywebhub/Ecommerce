from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}, your account was successfully created. You can sign in now')
            return redirect('Users:login')
    else:
        form = UserForm()
        context = {
        'form': form,
    }
    return render(request, 'register.html', context)

# @login_required
# def profile(request, user):
#     return render(request, 'profile.html')