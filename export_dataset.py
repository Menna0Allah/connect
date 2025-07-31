import os
import django
import pandas as pd

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'connection.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from users.models import UserProfile
from activities.models import Room, Topic, Message, RoomLike, MessageLike

# Extract user data
user_data = [
    {
        'username': user.username,
        'profile_photo_url': user.profile.photo.url if hasattr(user, 'profile') and user.profile.photo else ''
    }
    for user in User.objects.all()
]

# Extract room data
room_data = [
    {
        'room_name': room.name,
        'topic_name': room.topic.name if room.topic else '',
        'description': room.description if room.description else '',
        'creator': room.host.username if room.host else '',
        'room_created': room.created,
        'room_updated': room.updated,
        'participants': ','.join([user.username for user in room.participants.all()])
    }
    for room in Room.objects.all()
]

# Extract message data
message_data = [
    {
        'message_id': message.id,
        'message_content': message.body,
        'room_name': message.room.name,
        'message_username': message.user.username,
        'message_created': message.created,
        'message_updated': message.updated
    }
    for message in Message.objects.all()
]

# Extract room likes data
room_like_data = [
    {
        'room_name': like.room.name,
        'room_like_username': like.user.username,
        'room_like_created': like.created_at
    }
    for like in RoomLike.objects.all()
]

# Extract message likes data
message_like_data = [
    {
        'message_id': like.message.id,
        'message_like_username': like.user.username,
        'message_like_created': like.created_at
    }
    for like in MessageLike.objects.all()
]

# Create DataFrames
users_df = pd.DataFrame(user_data)
rooms_df = pd.DataFrame(room_data)
messages_df = pd.DataFrame(message_data)
room_likes_df = pd.DataFrame(room_like_data)
message_likes_df = pd.DataFrame(message_like_data)

# Check if DataFrames are empty
if messages_df.empty and rooms_df.empty and room_likes_df.empty and message_likes_df.empty and users_df.empty:
    print("No data found in the database. Please populate the database and try again.")
else:
    # Start with messages to preserve message_id
    combined_df = messages_df.copy()

    # Merge with message likes on message_id (left join to keep only messages)
    if not message_likes_df.empty:
        combined_df = combined_df.merge(message_likes_df, on='message_id', how='left', suffixes=('', '_message_like'))
    else:
        # Add empty columns if no message likes
        combined_df['message_like_username'] = ''
        combined_df['message_like_created'] = ''

    # Merge with rooms on room_name (left join to keep message-related rooms)
    combined_df = combined_df.merge(rooms_df, on='room_name', how='left', suffixes=('', '_room'))

    # Merge with room likes on room_name (left join)
    combined_df = combined_df.merge(room_likes_df, on='room_name', how='left', suffixes=('', '_room_like'))

    # Merge with users for message_username
    combined_df = combined_df.merge(users_df, left_on='message_username', right_on='username', how='left', suffixes=('', '_message_user'))
    combined_df = combined_df.drop(columns=['username'], errors='ignore')
    combined_df = combined_df.rename(columns={'profile_photo_url': 'profile_photo_url_message_user'})

    # Merge with users for creator
    combined_df = combined_df.merge(users_df, left_on='creator', right_on='username', how='left', suffixes=('', '_creator'))
    combined_df = combined_df.drop(columns=['username'], errors='ignore')
    combined_df = combined_df.rename(columns={'profile_photo_url': 'profile_photo_url_creator'})

    # Merge with users for room_like_username
    combined_df = combined_df.merge(users_df, left_on='room_like_username', right_on='username', how='left', suffixes=('', '_room_like_user'))
    combined_df = combined_df.drop(columns=['username'], errors='ignore')
    combined_df = combined_df.rename(columns={'profile_photo_url': 'profile_photo_url_room_like_user'})

    # Merge with users for message_like_username
    combined_df = combined_df.merge(users_df, left_on='message_like_username', right_on='username', how='left', suffixes=('', '_message_like_user'))
    combined_df = combined_df.drop(columns=['username'], errors='ignore')
    combined_df = combined_df.rename(columns={'profile_photo_url': 'profile_photo_url_message_like_user'})

    # Fill missing values with empty strings
    combined_df = combined_df.fillna('')

    # Remove completely empty rows
    combined_df = combined_df.dropna(how='all')

    # Save to CSV
    combined_df.to_csv('connection_dataset.csv', index=False)
    print("Dataset saved as connection_dataset.csv")