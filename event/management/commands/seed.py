

from django.core.management.base import BaseCommand
from faker import Faker
from event.models import Category, Event, Participant
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Seed the database with 20 fake entries for Category, Event, Participant'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding database with fake data...")

        # Create 5 categories
        categories = []
        for _ in range(5):
            cat = Category.objects.create(
                name=fake.word().capitalize(),
                description=fake.sentence()
            )
            categories.append(cat)

        # Create 10 events
        events = []
        for _ in range(10):
            evt = Event.objects.create(
                name=fake.catch_phrase(),
                description=fake.paragraph(nb_sentences=2),
                date=fake.date_this_year(),
                time=fake.time(),
                location=fake.city(),
                category=random.choice(categories)
            )
            events.append(evt)

        # Create 5 participants and assign random events
        for _ in range(5):
            participant = Participant.objects.create(
                name=fake.name(),
                email=fake.email()
            )
            participant.event.set(random.sample(events, k=random.randint(1, 3)))

        self.stdout.write(self.style.SUCCESS("✅ Done! 20 fake data entries added successfully."))
