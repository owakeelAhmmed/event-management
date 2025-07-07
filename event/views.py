from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Event, Participant
from .forms import CategoryForm, EventForm, ParticipantForm
from django.http import JsonResponse
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


# ===========Event==============

def event_list(request):
    events = Event.objects.select_related('category').all()
    return render(request, 'event_list.html', {'events': events})

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_form.html', {'form': form})


def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})



def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('event_list')


def event_list(request):
    query = request.GET.get('q')  # ?q=something

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
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form})

# Participant Delete
def delete_participant(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.delete()
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


