from django import template
from activities.models import Topic, Message

register = template.Library()

@register.inclusion_tag('activities/topics_component.html')
def topics_list():
    topics = Topic.objects.all()
    return {'topics': topics}

@register.inclusion_tag('activities/activity_component.html')
def recent_activity():
    messages = Message.objects.all()[:5]
    return {'messages': messages}

@register.filter
def model_name(obj):
    return obj.__class__.__name__