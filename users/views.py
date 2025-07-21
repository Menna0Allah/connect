from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from activities.models import Room, Topic
from users.forms import CustomPasswordChangeForm, UserProfileForm, UsernameChangeForm
from users.models import UserProfile
from django.contrib.auth.hashers import check_password

# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username) 
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next') or 'home'  # fallback to home if no next
            return redirect(next_url)
        else:
            messages.error(request,'Username or Password does not exist')

    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occur during registration')
    return render(request, 'users/login_register.html',{'form':form})


@login_required(login_url='users:login')
def userProfile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, 'User not found')
        return redirect('home')

    # Ensure UserProfile exists
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    rooms = user.room_set.all()
    user_messages  = user.message_set.order_by('-created')
    topics = Room.objects.values('topic__name').distinct()
    first_room = user.room_set.order_by('created').first()
    first_message = user.message_set.order_by('created').first()

    profile_form = UserProfileForm(instance=user_profile)
    username_form = UsernameChangeForm(instance=user)
    password_form = CustomPasswordChangeForm(user=user)

    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Profile photo updated successfully!')
                return redirect('users:user-profile', username=user.username)
            else:
                for error in profile_form.errors.values():
                    messages.error(request, error)
        elif 'username_submit' in request.POST:
            username_form = UsernameChangeForm(request.POST, instance=user)
            if username_form.is_valid():
                new_username = username_form.cleaned_data['username'].lower()
                if new_username == user.username.lower():
                    messages.success(request, 'Username unchanged.')
                else:
                    username_form.save()
                    messages.success(request, 'Username updated successfully!')
                return redirect('users:user-profile', username=new_username)
            else:
                for error in username_form.errors.values():
                    messages.error(request, error)
        elif 'password_submit' in request.POST:
            password_form = CustomPasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                new_password = password_form.cleaned_data.get('new_password1')
                if new_password and check_password(new_password, user.password):
                    messages.success(request, 'Password unchanged.')
                else:
                    password_form.save()
                    login(request, user)
                    messages.success(request, 'Password updated successfully!')
                return redirect('users:user-profile', username=user.username)
            else:
                for error in password_form.errors.values():
                    messages.error(request, error)

    context = {
        'user': user,
        'rooms': rooms,
        'user_messages': user_messages,
        'topics': topics,
        'user_profile': user_profile,
        'profile_form': profile_form,
        'username_form': username_form,
        'password_form': password_form,
        'join_date': user.date_joined,
        'first_room': first_room,
        'first_message': first_message,
    }
    return render(request, 'users/profile.html', context)