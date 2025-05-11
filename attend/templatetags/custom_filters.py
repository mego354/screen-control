from datetime import timedelta
from django import template
from django.utils import timezone
import re


register = template.Library()

@register.filter
def classname(value):
    return value.__class__.__name__

@register.filter
def event_year(value):
    current_year = timezone.localtime().year

    return current_year - value.group.dofaa.year + 1
    
@register.filter
def get_url(event, url_name):
    return event.get_url(url_name)

@register.filter
def get_academic_year(value):
    return timezone.localtime().year - value + 1


@register.filter(name='in_list')
def in_list(value, list_arg):
    list_arg = [int(x) for x in list_arg.split(',')]
    return value in list_arg 

@register.filter
def relative_time(event_date):
    # Get the current time
    current_time = timezone.localtime() #- timedelta(hours=1)
    
    # Calculate the time difference
    time_diff = event_date - current_time

    # Get total seconds and minutes
    seconds = time_diff.total_seconds()
    minutes = int(seconds / 60)

    # Convert to relative time (e.g., in X minutes/hours/days)
    if minutes == 0:
        return f"Now"
    elif minutes < 60 and minutes > 0:
        return f"coming in {minutes}m"
    elif minutes < 1440 and minutes > 0:
        hours = minutes // 60
        minutes = minutes % 60
        return f"coming in {hours}h {minutes}m"
    elif minutes >= 1440 and minutes > 0:
        days = minutes // 1440
        return f"coming in {days}d"
        
    elif minutes > -60:
        return f"done for {abs(minutes)}m"
    elif minutes > -1440:
        hours = minutes // 60
        return f"done for {abs(hours)}h"
    else:
        days = minutes // 1440
        return f"done for {abs(days)}d"

@register.filter
def sanitize_id(value):
    # Replace spaces with underscores and remove invalid characters
    return re.sub(r'[^a-zA-Z0-9_]', '_', value.replace(' ', '_'))