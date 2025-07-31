import os
import django
import random
from faker import Faker
from django.utils import timezone
from django.db import IntegrityError

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connection.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from activities.models import Room, Message, RoomLike, MessageLike, Topic

fake = Faker()

# --- OPTIONAL: Uncomment these to reset all related tables before generating ---
User.objects.all().delete()
UserProfile.objects.all().delete()
Topic.objects.all().delete()
Room.objects.all().delete()
Message.objects.all().delete()
RoomLike.objects.all().delete()
MessageLike.objects.all().delete()

# --- Helper function to generate truly unique values ---
def generate_unique_value(existing_set, generator_func):
    while True:
        value = generator_func()
        if value not in existing_set:
            existing_set.add(value)
            return value

# --- Create 50 users with unique usernames and emails ---
users = []
used_usernames = set(User.objects.values_list('username', flat=True))
used_emails = set(User.objects.values_list('email', flat=True))

for _ in range(50):
    username = generate_unique_value(used_usernames, fake.user_name)
    email = generate_unique_value(used_emails, fake.email)
    user = User.objects.create_user(
        username=username,
        email=email,
        password='password123'
    )
    photo_list = [
        'profile_photos/1.jpg',
        'profile_photos/2.jpg',
        'profile_photos/3.jpg',
        'profile_photos/4.jpg',
        'profile_photos/5.jpg',
        'profile_photos/6.jpg',
        'profile_photos/7.jpg',
        'profile_photos/8.jpg',
        'profile_photos/9.jpg',
        'profile_photos/10.jpg',
        'profile_photos/11.jpg',
        'profile_photos/12.jpg',
        'profile_photos/13.jpg',
        'profile_photos/14.jpg',
        'profile_photos/15.jpg',
    ]
    UserProfile.objects.create(
        user=user,
        photo=photo_list[user.id % len(photo_list)]
    )
    users.append(user)

# --- Create 20 unique topics ---
topics = []
used_topic_names = set(Topic.objects.values_list('name', flat=True))

for _ in range(20):
    topic_name = generate_unique_value(used_topic_names, lambda: fake.word().capitalize())
    topic = Topic.objects.create(name=topic_name)
    topics.append(topic)

# --- Create 20 rooms with participants ---
rooms = []
for _ in range(20):
    room = Room.objects.create(
        name=fake.unique.word(),
        description=fake.sentence(),
        host=random.choice(users),
        topic=random.choice(topics)
    )
    participants = random.sample(users, random.randint(1, 5))
    room.participants.set(participants)
    rooms.append(room)

# --- Create 200 messages ---
for _ in range(200):
    Message.objects.create(
        user=random.choice(users),
        room=random.choice(rooms),
        body=fake.sentence(),
        created=timezone.now()
    )

# --- Create 300 unique room likes ---
room_likes_set = set(RoomLike.objects.values_list('user_id', 'room_id'))

for _ in range(300):
    user = random.choice(users)
    room = random.choice(rooms)
    key = (user.id, room.id)
    if key not in room_likes_set:
        RoomLike.objects.create(user=user, room=room, created_at=timezone.now())
        room_likes_set.add(key)

# --- Create 300 unique message likes ---
messages = list(Message.objects.all())
message_likes_set = set(MessageLike.objects.values_list('user_id', 'message_id'))

for _ in range(300):
    user = random.choice(users)
    message = random.choice(messages)
    key = (user.id, message.id)
    if key not in message_likes_set:
        MessageLike.objects.create(user=user, message=message, created_at=timezone.now())
        message_likes_set.add(key)

print("✅ Data generation complete!")
