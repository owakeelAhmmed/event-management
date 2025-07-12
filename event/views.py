from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.db.models import Q
from datetime import date



def home(request):
    upcoming_event = Event.objects.filter(date__gt=date.today()).order_by('date').first()
    scheduled_events = Event.objects.filter(date__gte=timezone.now().date()).order_by('date', 'time')
    
    return render(request, 'home.html', {
        'upcoming_event': upcoming_event,
        'scheduled_events': scheduled_events,
    })



# Read
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

# Create
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            elif request.user.groups.filter(name='Organizer').exists():
                return redirect('organizer_dashboard')
            return redirect('event_list')
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
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            elif request.user.groups.filter(name='Organizer').exists():
                return redirect('organizer_dashboard')
            return redirect('event_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category_form.html', {'form': form})

# Delete
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.groups.filter(name='Organizer').exists():
            return redirect('organizer_dashboard')
        return redirect('event_list')
    return render(request, 'category_confirm_delete.html', {'category': category})


# ===========Event==============
def event_list(request):
    query = request.GET.get('q') 
    if query:
        events = Event.objects.filter(
            Q(name__icontains=query) | Q(location__icontains=query)
        )
    else:
        events = Event.objects.all()

    context = {
        'events': events,
    }
    return render(request, 'event_list.html', context)


#  Create Event View
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            elif request.user.groups.filter(name='Organizer').exists():
                return redirect('organizer_dashboard')
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})


#  Event Detail View
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})


#  Update Event View
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            elif request.user.groups.filter(name='Organizer').exists():
                return redirect('organizer_dashboard')
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})


#  Delete Event View
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        if request.user.is_superuser:
            return redirect('admin_dashboard')
        elif request.user.groups.filter(name='Organizer').exists():
            return redirect('organizer_dashboard')
        return redirect('event_list')
    return render(request, 'event_confirm_delete.html', {'event': event})

# ================Participant===================

def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'participant_list.html', {'participants': participants})

# Participant Create
def create_participant(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('participant_list')
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

# Participant Update
def update_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form})

# Participant Delete
def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.delete()
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    return redirect('participant_list')



def dashboard(request):
    today = date.today()
    
    all_events = Event.objects.all()
    total_events = all_events.count()
    upcoming_events = all_events.filter(date__gt=today).count()
    past_events = all_events.filter(date__lt=today).count()
    todays_events = all_events.filter(date=today)
    total_participants = Participant.objects.count()

    context = {
        "total_events": total_events,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "todays_events": todays_events,
        "total_participants": total_participants,
    }
    return render(request, "dashboard.html", context)

def event_filter_api(request, filter_type):
    today = date.today()
    
    if filter_type == "upcoming":
        events = Event.objects.filter(date__gt=today)
    elif filter_type == "past":
        events = Event.objects.filter(date__lt=today)
    else:
        events = Event.objects.all()

    event_list = list(events.values("title", "description", "date"))
    return JsonResponse(event_list, safe=False)

def is_admin_or_organizer(user):
    return user.groups.filter(name__in=['Admin', 'Organizer']).exists() or user.is_superuser

@login_required
def event_list(request):
    q = request.GET.get('q')
    events = Event.objects.all()

    if q:
        events = events.filter(name__icontains=q) | events.filter(location__icontains=q)

    context = {
        'events': events,
        'is_admin_or_organizer': is_admin_or_organizer(request.user),
    }
    return render(request, 'event_list.html', context)


@login_required
def rsvp_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user in event.rsvps.all():
        messages.info(request, "You have already RSVP'd for this event.")
    else:
        event.rsvps.add(request.user)
        messages.success(request, "You have successfully RSVP'd for the event.")

        send_mail(
            subject="RSVP Confirmation",
            message=f"Hi {request.user.username}, you have successfully RSVP’d to {event.name}.",
            from_email="noreply@event.com",
            recipient_list=[request.user.email],
            fail_silently=True,
        )
    return redirect('event_list')

@login_required
def participant_dashboard(request):
    rsvped_events = request.user.rsvp_events.all() 
    
    return render(request, 'event/participant_dashboard.html', {
        'rsvped_events': rsvped_events
    })
