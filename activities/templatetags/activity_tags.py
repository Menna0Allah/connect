from django import template
from activities.models import Message, Topic

register = template.Library()

@register.inclusion_tag('activities/topics_component.html')
def topics_list():
    topics = Topic.objects.all()
    return {'topics': topics}

@register.inclusion_tag('activities/activity_component.html')
def recent_activity():
    messages = Message.objects.all().order_by('-created')[0:5]
    return {'messages': messages}