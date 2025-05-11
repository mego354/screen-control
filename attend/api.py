from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Doctor, Department, Dofaa, Group, Class, DepCourse, Room, SpecialEvent
from .filtering import get_room_event_data
from .announcement import AnnouncementImageCreator

        

####################################     Manage Room     ##########################
def doc_img(request, doc_id):
    doctor = get_object_or_404(Doctor, pk=doc_id)
    creator = AnnouncementImageCreator()
    file_path = creator.create_doctor_announcement(doctor)
    
    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()
        return HttpResponse(image_data, content_type="image/jpeg")
    except FileNotFoundError:
        return HttpResponse("Image not found", status=404)
    except Exception as e:
        return HttpResponse("Error: " + str(e), status=500)

def get_current_event(room_code, current_date, get_event):
    room = get_object_or_404(Room, name=room_code.upper())
    data = get_room_event_data(room, current_date, get_event=get_event)
    return data

def room_pic(request, room_code):
    current_date = timezone.localtime()
    data = get_current_event(room_code, current_date, get_event=True)
    
    if data["case"] != 3:
        event = get_object_or_404(data["event_model_name"], slug=data["event_slug"])
        creator = AnnouncementImageCreator()
        file_path = creator.create_lecture_announcement(event, data)

        try:
            with open(file_path, 'rb') as f:
                image_data = f.read()
            return HttpResponse(image_data, content_type="image/jpeg")
        except FileNotFoundError:
            return HttpResponse("Image not found", status=404)
        except Exception as e:
            return HttpResponse("Error: " + str(e), status=500)
    else: #case no session
        return JsonResponse(data, safe=False)
    

####################################      forms API      ##########################
@require_POST
def load_doctors(request):
    course_id = request.POST.get('course')
    is_doctor = True if request.POST.get('doctor') == 'true' else False
    if course_id is None or is_doctor is None or not DepCourse.objects.filter(pk=course_id).exists():
        return JsonResponse({'error': 'data not provided'}, status=400)
    course = DepCourse.objects.get(pk=course_id).course
    doctors = course.doctors.filter(is_doctor=is_doctor)

    doctors_list = list(doctors.values('id', 'name'))
    return JsonResponse(doctors_list, safe=False, status=200)


@require_POST
def load_classes(request):
    group_id = request.POST.get('group')
    if group_id is None or not Group.objects.filter(pk=group_id).exists():
        return JsonResponse({'error': 'Group ID not provided'}, status=400)

    classes = Class.objects.filter(group_id=group_id).order_by('number')
    class_list = list(classes.values('id', 'number'))
    return JsonResponse(class_list, safe=False, status=200)

@require_POST 
def load_groups(request):
    year = int(request.POST.get('year'))
    department_id = request.POST.get('department_id')
    if department_id is None or not Dofaa.objects.filter(academic_year=year).exists() or not Department.objects.filter(pk=department_id).exists():
        return JsonResponse({'error': 'Can not resolve with this criteria'}, status=400)
    department = Department.objects.get(pk=department_id)
    dofaa = Dofaa.objects.get(academic_year=year)
    if Group.objects.filter(department=department, dofaa_id=dofaa.id).exists():
        groups = Group.objects.filter(department=department, dofaa_id=dofaa.id).order_by('number')
        groups_list = list(groups.values('id', 'number'))
        return JsonResponse(groups_list, safe=False, status=200)
    return JsonResponse({'error': 'Can not resolve with this criteria'}, status=400)

@require_POST
def load_departments(request):
    college_id = request.POST.get('college')
    if college_id is None:
        return JsonResponse({'error': 'college ID not provided'}, status=400)

    departments = Department.objects.filter(college_id=college_id).order_by('name')
    departments_list = list(departments.values('id', 'name'))
    return JsonResponse(departments_list, safe=False, status=200)

@require_POST
def load_depcourses(request):
    department_id = request.POST.get('department')
    year = request.POST.get('year')
    if department_id is None or year is None:
        return JsonResponse({'error': 'data not provided'}, status=400)

    depcourses = DepCourse.objects.filter(department_id=department_id, academic_year=year).order_by('course__name')
    depcourses_list = list(depcourses.values('id', 'course__name'))
    return JsonResponse(depcourses_list, safe=False, status=200)

