from django import forms
from .models import Room, Topic

class RoomForm(forms.ModelForm):
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.all(), 
        required=False, label="Select Topic"
    )
    new_topic = forms.CharField(
        max_length=200, 
        required=False, 
        label="New Topic"
    )

    class Meta:
        model = Room
        fields = ['name', 'description', 'topic', 'new_topic']
        exclude = ['host', 'participants']

    def clean(self):
        cleaned_data = super().clean()
        topic = cleaned_data.get('topic')
        new_topic = cleaned_data.get('new_topic')

        if not topic and not new_topic:
            raise forms.ValidationError("Please select an existing topic or enter a new one.")
        if topic and new_topic:
            raise forms.ValidationError("Please choose either an existing topic or enter a new one, not both.")
        return cleaned_data