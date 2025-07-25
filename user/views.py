from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from user.forms import SignUpForm, LoginForm
from event.forms import CategoryForm
from user.decorators import admin_required, organizer_required, participant_required
from django.contrib.auth.decorators import login_required
from event.models import Event, Category
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from .forms import ProfileUpdateForm, CustomUserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()





def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])

            user.is_active = False  
            user.save()

            participant_group, created = Group.objects.get_or_create(name='Participant')
            participant_group.user_set.add(user)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = request.build_absolute_uri(
                reverse('activate_account', kwargs={'uidb64': uid, 'token': token})
            )

            subject = 'Activate Your Account'
            message = render_to_string('user/activation_email.html', {
                'user': user,
                'activation_link': activation_link,
            })

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            messages.success(request, 'Signup successful! Please check your email to activate your account.')
            return redirect('login')
        else:
            return render(request, 'user/signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'user/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        messages.success(request, 'Your account has been activated. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('signup')


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
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Login successful!')

                    if user.is_superuser:
                        return redirect('admin_dashboard')
                    elif user.groups.filter(name = 'Organizer').exists():
                        return redirect('organizer_dashboard')
                    elif user.groups.filter(name = 'Participant').exists():
                        return redirect('participant_dashboard')
                    else:
                        return redirect('home')
                else:
                    messages.error(request, 'Account not activated. Please check your email.')
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

# def admin_dashboard(request):
#     events = Event.objects.all()
#     categories = Category.objects.all()
#     participants = User.objects.filter(groups__name='Participant')

#     return render(request, 'dashboard/admin_dashboard.html', {
#         'events': events,
#         'categories': categories,
#         'participants': participants,
#     })

# def admin_dashboard(request):
#     if not request.user.is_authenticated or not request.user.is_superuser:
#         return redirect('login')
    
#     events = Event.objects.all()
#     categories = Category.objects.all()
#     participants = User.objects.filter(groups__name='Participant')

#     total_events = events.count()
#     total_participants = participants.count()
#     upcoming_events = events.filter(date__gte=now().date()).count()
#     past_events = events.filter(date__lt=now().date()).count()
#     todays_events = events.filter(date=now().date())

#     context = {
#         'events': events,
#         'categories': categories,
#         'participants': participants,
#         'total_events': total_events,
#         'total_participants': total_participants,
#         'upcoming_events': upcoming_events,
#         'past_events': past_events,
#         'todays_events': todays_events,
#     }
#     return render(request, 'dashboard/admin_dashboard.html', context)


class AdminDashbordView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/admin_dashboard.html'

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect('login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        events = Event.objects.all()
        categories = Category.objects.all()
        participants = User.objects.filter(groups__name = 'Participant')


        context['events'] = events
        context['categories'] = categories
        context['participants'] = participants
        context['total_events'] = events.count()
        context['total_participants'] = participants.count()
        context['upcoming_events'] = events.filter(date__gte = now().date()).count()
        context['past_events'] = events.filter(date__lt=now().date()).count()
        context['todays_events'] = events.filter(date=now().date())

        return context






def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Create
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'category_form.html', {'form': form})

# Update
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

# Delete
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})

@organizer_required
def organizer_dashboard(request):
    events = Event.objects.all()
    categories = Category.objects.all()

    total_events = events.count()
    upcoming_events = events.filter(date__gte=now().date()).count()
    past_events = events.filter(date__lt=now().date()).count()
    todays_events = events.filter(date=now().date())

    return render(request, 'dashboard/organizer_dashboard.html', {
        'events': events,
        'categories': categories,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    })

@login_required
def participant_dashboard(request):
    rsvped_events = Event.objects.filter(rsvps=request.user)
    

    return render(request, 'dashboard/participant_dashboard.html', {
        'rsvped_events': rsvped_events,
    })

# Profile View
@login_required
def profile_view(request):
    return render(request, 'user/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/change_password.html', {'form': form})