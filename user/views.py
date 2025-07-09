from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from user.forms import SignUpForm, LoginForm
from user.decorators import admin_required, organizer_required, participant_required
from event.models import Event

# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            participant_group = Group.objects.get(name='Participant')
            participant_group.user_set.add(user)


            messages.success(request, 'Signup successful!, Please login')
            return redirect('login')
        else:
            return render(request, 'user/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form' : form})
    

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 

@admin_required
def delete_group_view(request):
    return render(request, 'admin/delete_group.html')

@organizer_required
def create_event_view(request):
    return render(request, 'event/create_event.html')

@participant_required
def view_event_list(request):
    events = Event.objects.all()
    return render(request, 'event/view_event_list.html', {'events': events})