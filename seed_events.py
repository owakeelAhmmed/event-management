import os
import django
import random
from datetime import datetime, timedelta, time

# Django environment setup
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "event_management.settings")
django.setup()

from event.models import Category, Event, Participant

# ✅ 1. Create Categories
category_names = [
    "Technology", "Design", "Business", "Marketing", "Leadership"
]
categories = []

for name in category_names:
    category = Category(name=name, description=f"{name} related sessions")
    categories.append(category)

Category.objects.bulk_create(categories)
print("✅ Created 5 Categories")

# ✅ 2. Create Events
created_categories = list(Category.objects.all())
events = []

for i in range(20):
    date = datetime.today().date() + timedelta(days=i)
    event_time = time(hour=random.randint(9, 17), minute=random.choice([0, 30]))
    event = Event(
        name=f"Event {i+1}: {random.choice(['Tech Trends', 'UX Basics', 'Startup Hacks'])}",
        description="This is a sample event.",
        date=date,
        time=event_time,
        location=random.choice(["Room 101", "Main Hall", "Auditorium", "Stage A"]),
        category=random.choice(created_categories)
    )
    events.append(event)

Event.objects.bulk_create(events)
print("✅ Created 20 Events")

# ✅ 3. Create Participants and assign random events
created_events = list(Event.objects.all())
participants = []

for i in range(30):
    name = f"Participant {i+1}"
    email = f"user{i+1}@example.com"
    participant = Participant.objects.create(name=name, email=email)
    
    # Randomly assign 1 to 3 events
    assigned_events = random.sample(created_events, k=random.randint(1, 3))
    participant.events.add(*assigned_events)

print("✅ Created 30 Participants and assigned them to events")
