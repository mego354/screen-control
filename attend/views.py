from django.utils import timezone
from dateutil import parser

import os
from django.conf import settings

from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView, RedirectView

from django.http import FileResponse, Http404, JsonResponse
from django.urls import reverse_lazy

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q, Max, Min

from .models import *
from .forms import  *
from .filtering import EventFilterMixin
from .helpers import get_user_device, generate_exc, close_event
from .api import get_current_event
from .announcement import AnnouncementImageCreator


from threading import Thread

CLOSE_TIMER = 30
'''
XTOKEN
'''

class tryy(TemplateView):
    template_name = 'attend/try.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device = get_user_device(self.request)
        context['browser'] = device['browser_family']

        return context



####################################   General  Events   ##########################

class TableListView(ListView, EventFilterMixin):
    template_name = 'events/table.html'
    context_object_name = 'events'
    paginate_by = 50
    required_role = [1, 2, 3]
    redirect_url = 'attend:login'

    def get_queryset(self):
        # Extract GET parameters for filtering
        params = dict(self.request.GET)
        self.events = self.filter_events(params)
        return self.events

    def get_filter_options(self, queryset, field, sort_field=None):
        """Extract unique values from the queryset based on the given field and sort them if needed."""
        items = {getattr(event, field, None) for event in queryset if getattr(event, field, None)}

        if sort_field:
            return sorted(items, key=lambda x: getattr(x, sort_field), reverse=True)
        return items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch filtered events
        events = self.events

        # Add colleges and academic years to the context
        context.update({
            "colleges": College.objects.all().order_by('name'),
            "departments": Department.objects.all().order_by('name'),
            "years": Dofaa.objects.filter(is_done=False).order_by('academic_year').values_list('academic_year', flat=True),
        })

        # Add filter options (groups, classes, courses, doctors, rooms) to the context
        context.update({
            "groups": self.get_filter_options(events, 'group'),
            "classes": self.get_filter_options(events, 'classs'),
            "courses": self.get_filter_options(self.get_filter_options(events, 'DepCourse'), 'course'),
            "doctors": self.get_filter_options(events, 'doctor'),
            "rooms": Room.objects.filter(Q(lectures__isnull=False) | Q(sections__isnull=False)).distinct(),
        })

        # Aggregate date ranges from both Lecture and Section models
        context.update(self.get_date_ranges())

        # Handle query parameters for pagination
        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()

        return context

    def get_date_ranges(self):
        """Return the earliest and most recent dates across Lecture and Section models."""
        lecture_dates = Lecture.objects.aggregate(
            most_recent=Max('date'),
            earliest=Min('date')
        )
        section_dates = Section.objects.aggregate(
            most_recent=Max('date'),
            earliest=Min('date')
        )

        try:
            # Ensure dates exist, fall back to None if dates are missing
            start_date = min(filter(None, [lecture_dates['earliest'], section_dates['earliest']]))
            end_date = max(filter(None, [lecture_dates['most_recent'], section_dates['most_recent']]))

            # Parse the date strings into datetime objects using dateutil to handle multiple formats
            start_date = parser.parse(str(start_date))
            end_date = parser.parse(str(end_date))

            # Format the dates as mm/dd/yyyy
            formatted_start_date = start_date.strftime("%Y-%m-%d")
            formatted_end_date = end_date.strftime("%Y-%m-%d")

            return {
                "start_date": formatted_start_date,
                "end_date": formatted_end_date,
            }
        except:
            return {
                "start_date": None,
                "end_date": None,
            }


class GeneralCreateView(CreateView):

    def get_model(self):
        return self.model
    def get_form_class(self):
        return self.form_class
    def get_template_names(self):
        return self.template_name
    def get_success_url(self):
        messages.success(self.request,"Items has been Created successfully")
        return self.object.get_url('detail')

class GeneralDetailView(DetailView):
    template_name = 'events/general_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_model(self):
        return self.model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.get_model().__name__
        return context

class GeneralUpdateView(UpdateView):
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_model(self):
        return self.model

    def get_form_class(self):
        return self.form_class

    def get_template_names(self):
        return self.template_name

    def get_success_url(self):
        messages.success(self.request, "Changes have been saved successfully")
        return self.object.get_url('detail')

class GeneralDeleteView(DeleteView):
    template_name = 'events/general_delete.html'

    def get_model(self):
        return self.model

    def get_success_url(self):
        messages.success(self.request,"Items has been deleted successfully")
        return reverse_lazy('attend:TableListView')


####################################    Attend Method    ##########################
class AtivateEventRedirectView(RedirectView):
    model = None

    def get_redirect_url(self, *args, **kwargs):
        model = self.model
        event = get_object_or_404(model, slug=kwargs['slug'])
        if event.is_done:
            messages.error(self.request,f"This {model.__name__} is done previously we can't active it again")
        elif event.is_active:
            messages.success(self.request,f"This {model.__name__} is done already active")
        else:
            event.is_active = True; event.save()
            Thread(target=close_event, args=(event, CLOSE_TIMER), daemon=True).start()
            messages.success(self.request,f"{model.__name__}'s been activated successfully")
        return super().get_redirect_url(*args, **kwargs)


class GeneralViewAttendView(DetailView):
    template_name = 'events/view_attend.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_model(self):
        return self.model

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_class = self.get_model()
        context['model_name'] = model_class.__name__
        return context

class DownloadExcelSheet(View):
    def get(self, request, model_name, slug):
        if model_name.title() == 'Lecture':
            model = Lecture
        elif model_name.title() == 'Section':
            model = Section
        else: raise Http404("File not foundable")
        event = get_object_or_404(model, slug=slug)

        file_path = generate_exc(event)
        if os.path.exists(file_path):
            filename = os.path.basename(file_path)
            response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            return response
        else:
            raise Http404("File not found")


####################################  Room views  ##########################
class RoomDataView(View):
    def get(self, request, room_code):
        current_date = timezone.localtime()
        data = get_current_event(room_code, current_date, get_event=False)
        try:
            if data["event_model_name"] == SpecialEvent:
                data["event_model_name"] = 'SpecialEvent'
        except:
            pass
        return JsonResponse(data, safe=False)

class RoomPicturesListView(TemplateView):
    template_name = 'events/room_list.html'
    destination_path = os.path.join(settings.STATIC_ROOT, "room")
    announcement_creator = AnnouncementImageCreator()

    def get_context_data(self, **kwargs):
        """
        Generates the context for the room list view, including room events
        and their associated images.
        """
        context = super().get_context_data(**kwargs)
        room_code = self.kwargs.get('room_code')
        context['room'] = room_code
        context['events'] = self.get_room_events(room_code)
        return context

    def get_room_events(self, room_code):
        """
        Retrieves a list of events for the specified room within the current day,
        generating images for each unique event.
        """
        current_date = timezone.localtime()
        end_date = current_date.replace(hour=20, minute=0, second=0, microsecond=0)
        events = []
        last_event_data = None

        # Ensure destination directory exists
        if not os.path.exists(self.destination_path):
            os.makedirs(self.destination_path)

        # Loop through 30-minute increments until end_date
        while current_date < end_date:
            event_data = get_current_event(room_code, current_date, get_event=True)

            # Avoid processing duplicate or unavailable events
            if event_data == last_event_data or event_data["case"] == 3:
                current_date += timedelta(minutes=30)
                continue

            # Process and add event details to events list
            event_instance = get_object_or_404(event_data["event_model_name"], slug=event_data["event_slug"])
            file_name = f"{len(events)}_img.jpg"
            image_path = self.generate_event_image(event_instance, event_data, file_name)
            events.append(self.format_event_data(event_instance, file_name))

            # Update the last event and increment time
            last_event_data = event_data

            current_date += timedelta(minutes=30)

        return events

    def generate_event_image(self, event, event_data, file_name):
        """
        Creates an image announcement for the event and saves it to a unique path.
        """
        file_path = os.path.join(self.destination_path, file_name)
        return self.announcement_creator.create_lecture_announcement(event, event_data, file_path)

    def format_event_data(self, event_instance, file_name):
        """
        Formats event data for inclusion in the template context.
        """
        event_url = event_instance.get_url('detail') if event_instance.__class__.__name__ != "SpecialEvent" else None
        event_date = event_instance.date
        event_end_date = event_instance.end_date if event_instance.__class__.__name__ != "SpecialEvent" else event_date + timedelta(minutes=event_instance.duration)

        return {
            'image': f"room/{file_name}",
            'url': event_url,
            'date': event_date,
            'end_date': event_end_date,
        }
####################################  END Room views  ##########################
