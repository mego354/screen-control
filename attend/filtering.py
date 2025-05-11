from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from itertools import chain

from django.db.models.functions import ExtractWeekDay
from .models import Section ,Lecture

class EventFilterMixin:
    def filter_events(self, params):
        event_param = params.get("events_type", [None])[0]
        if event_param not in ['sections', 'lectures']:
            event_param = None

        available_params = ["department", "standard", "college", "year", "group", "class", "course", "doctor", "room", "day", "start_date", "end_date"]
        events = None

        if event_param:
            if event_param == "sections":
                events = Section.objects.all().order_by('group__department__college__id', 'group__dofaa__academic_year', 'group__department_id', 'group__number', 'classs__number', 'is_std', 'date')
            elif event_param == "lectures":
                events = Lecture.objects.all().order_by('group__department__college__id', 'group__dofaa__academic_year', 'group__department_id', 'group__number', 'is_std', 'date')

            for param in params:
                if events and param in available_params and param != 'event':
                    events = self.filtering(events, param, params[param][0])
            return events
        else:
            lectures = Lecture.objects.all().order_by('group__department__college__id', 'group__dofaa__academic_year', 'group__department_id', 'group__number', 'is_std', 'date')
            sections = Section.objects.all().order_by('group__department__college__id', 'group__dofaa__academic_year', 'group__department_id', 'group__number', 'classs__number', 'is_std', 'date')
            for param in params:
                if param in available_params:
                    if param != 'event' and param != 'class' and lectures:
                        lectures = self.filtering(lectures, param, params[param][0])
                    if param != 'event' and sections:
                        sections = self.filtering(sections, param, params[param][0])

            event = list(chain(lectures, sections))
            return sorted(event, key=lambda x: getattr(x, 'date'), reverse=True)
        
    def filtering(self, events, param, value):
        filter_mapping = {
            "standard": 'is_std',
            "college": 'DepCourse__department__college__name',
            "department": 'DepCourse__department__name',
            "course": 'DepCourse__course_id',
            "doctor": 'doctor_id',
            "room": 'room',
            "group": 'group__id',
            "year": 'group__dofaa__academic_year',
            "class": 'classs__id',
            "start_date": 'date__gte',
            "end_date": 'date__lte',
            "day": 'date__week_day',
        }

        field = filter_mapping.get(param)
        if field:
            try:
                if param == "day":
                    # Convert day name to day number (1 = sunday, 7 = saturday)
                    day_number = self.get_day_number(value)

                    return events.annotate(weekday=ExtractWeekDay('date')).filter(weekday=day_number) if day_number else events
                    # return events.filter(**{field: day_number}) if day_number else events

                return events.filter(**{field: value})
            except Exception as e:
                print(f"Filtering error for param {param} with value {value}: {e}")
                return events
        return events

    def get_day_number(self, day_name):
        """Convert day name to day number for Django filters."""
        days = {
            'sunday'   : 1,
            'monday'   : 2,
            'tuesday'  : 3,
            'wednesday': 4,
            'thursday' : 5,
            'friday'   : 6,
            'saturday' : 7,
        }
        return days.get(day_name.lower(), None)


def get_room_event_data(room, date, get_event=False):
    section_duration = 45
    lecture_duration = 90
    past_lecture = room.lectures.filter(date__range=(date - timedelta(minutes=lecture_duration - 1), date)).order_by('-date').first()
    past_section = room.sections.filter(date__range=(date - timedelta(minutes=section_duration - 1), date)).order_by('-date').first()
    coming_lecture = room.lectures.filter(date__range=(date , date + timedelta(hours=10))).order_by('date').first()
    coming_section = room.sections.filter(date__range=(date , date + timedelta(hours=10))).order_by('date').first()
    all_events = [event for event in [past_lecture,past_section,coming_lecture,coming_section] if event is not None ]
    if past_lecture and past_lecture.end_date < timezone.localtime(date):
        all_events = [event for event in [past_section,coming_lecture,coming_section] if event is not None ]
    if len(all_events) > 0:
        if (coming_lecture or coming_section) and not (past_lecture or past_section) :
            if coming_lecture and coming_section:
                event = coming_lecture if coming_lecture and coming_lecture.date <= coming_section.date else coming_section
            else:
                event = coming_lecture if coming_lecture else coming_section
        else:
            if past_lecture and past_section:
                event = past_lecture if past_lecture and past_lecture.date <= past_section.date else past_section
            else:
                event = past_lecture if past_lecture else past_section
################################
        if isinstance(event, Section) :
            session_type = "Sec"
            students = f"Year: {event.group.dofaa.academic_year} Group: {event.group.number} Class {event.classs.number}"
        elif isinstance(event, Lecture) :
            session_type = "Lec"
            students = f"Year: {event.group.dofaa.academic_year} Group: {event.group.number}"
################################
        current_date = timezone.localtime(date)
        event_date = timezone.localtime(event.date)
        event_end_date = timezone.localtime(event.end_date)
        if current_date <= event_date:
            difference = event_date - current_date
            total_minutes = difference.total_seconds() / 60

            # Get hours and minutes
            hours = int(total_minutes / 60)  - 1
            minutes = int(total_minutes % 60)
            time = f"Starts in {hours} H {minutes} M" if hours > 0 else f"Starts in {minutes} M"

        else:
            start_time = event_date.strftime("%I:%M %p")
            # final_date = event_date + timedelta(minutes=duration_min)
            end_time = event_end_date.strftime("%I:%M %p")
            time = f"Time: {start_time} - {end_time}"

################################

        dwin_available = event.doctor.dwin_img or None
        case_number = 1 if dwin_available else 2 #case 2 means no pic for doctor in dwin system
        dwin_img = dwin_available if dwin_available else 3
        data = {
            "case": case_number,
            "students": students,
            "session_type": session_type,
            "department_name": f"Department: {event.group.department.name}",
            "college_name": event.group.department.college.name,
            "doctor_name": str(event.doctor),
            "subject_name": f"Course: {event.DepCourse.course.name}",
            "time": time,
            "pic_id": dwin_img,
            }
        if get_event:
            data["event_slug"] = event.slug
            data["event_model_name"] = event.__class__
        return data

    else:
        return {"case": 3, "message": "This room is empty for the rest of the day"}
