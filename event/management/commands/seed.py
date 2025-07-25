from django.core.management.base import BaseCommand
from event.models import Category, Event, Participant
import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


fake = Faker()

class Command(BaseCommand):
    help = "Seed database with current/future Categories, Events, Participants"

    def handle(self, *args, **kwargs):
        # Optional: Clear old data
        Category.objects.all().delete()
        Event.objects.all().delete()
        Participant.objects.all().delete()

        # Create Categories
        categories = []
        for _ in range(5):
            cat = Category.objects.create(
                name=fake.unique.word().capitalize(),
                description=fake.sentence()
            )
            categories.append(cat)

        # Create Events (Today to 20 days ahead)
        events = []
        for _ in range(20):
            future_date = datetime.now().date() + timedelta(days=random.randint(0, 20))
            future_time = (datetime.now() + timedelta(minutes=random.randint(30, 300))).time()

            event = Event.objects.create(
                name=fake.catch_phrase(),
                description=fake.text(),
                date=future_date,
                time=future_time,
                location=fake.address(),
                category=random.choice(categories)
            )
            events.append(event)

        # Create Participants and randomly assign events
        for _ in range(10):
            participant = Participant.objects.create(
                name=fake.name(),
                email=fake.unique.email()
            )
            joined_events = random.sample(events, random.randint(1, 4))
            for ev in joined_events:
                participant.events.add(ev)

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded 5 Categories, 20 Events (future), 10 Participants"))