from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'autofocus': False}),
        }

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        if username == self.instance.username.lower():
            return username
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'id': 'id_old_password', 'autofocus': False, 'autocomplete': 'off'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'id': 'id_new_password1', 'autofocus': False, 'autocomplete': 'new-password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'id': 'id_new_password2', 'autofocus': False, 'autocomplete': 'new-password'})

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not old_password:
            raise forms.ValidationError(self.error_messages['password_incorrect'])
        if check_password(old_password, self.user.password):
            return old_password
        raise forms.ValidationError(self.error_messages['password_incorrect'])

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        if new_password1 and check_password(new_password1, self.user.password):
            return cleaned_data
        return super().clean()