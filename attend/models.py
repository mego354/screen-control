from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

from django.urls import reverse
from django.utils import timezone

import random
import string

def generate_unique_code(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class User(AbstractUser):
    ROLE_CHOICES = (
          (1, 'Admin'),
          (2, 'Subadmin'),
          (3, 'Student'),
          (4, 'Doctor'),
    )
    SEX_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default='Male')
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=3)
    national_id = models.PositiveIntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"#{self.id}"

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
    
class Doctor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    name = models.CharField(max_length=64, unique=True)
    image = models.ImageField(upload_to='doc_pics/', blank=True, null=True)
    is_doctor = models.BooleanField(default=True)
    dwin_img = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        # name = f'{self.user.first_name} {self.user.last_name}'
        if self.is_doctor:
            return f"Prof. {self.name}"
        else:
            return f"Eng. {self.name}"
    
class College(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=64)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="departments")

    def __str__(self):
        return self.name

class Dofaa(models.Model):
    year = models.PositiveSmallIntegerField()
    academic_year = models.SmallIntegerField(default=1)
    is_done = models.BooleanField(default=False)
    def __str__(self):
        return str(self.year) 


class Group(models.Model):
    number = models.PositiveSmallIntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="groups")
    dofaa = models.ForeignKey(Dofaa, on_delete=models.CASCADE, related_name="groups")

    def __str__(self):
        return f"P{self.dofaa} - {self.department} - G{self.number} "

class Class(models.Model):
    number = models.PositiveSmallIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="classes")

    def __str__(self):
        return f"P{self.group.dofaa} - D{self.group.department} - G{self.group.number} - C{self.number}"

class Course(models.Model):
    name = models.CharField(max_length=64, unique=True)
    doctors = models.ManyToManyField(Doctor,blank=True)
    duration = models.DurationField(default=timedelta(minutes=90))

    def __str__(self):
        return f"{self.id} {self.name}"

class DepCourse(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="depcourses")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="depcourses")
    academic_year = models.SmallIntegerField(null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'department', 'academic_year'], name='unique_dep_course_year')
        ]
    
    def __str__(self):
        return self.course.name    

class Room(models.Model):
    name = models.CharField(max_length=64, unique=True)
    ip = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return self.name

class Section(models.Model): 
    slug = models.SlugField(unique=True, blank=True)
    DepCourse = models.ForeignKey(DepCourse, on_delete=models.CASCADE, related_name="sections")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="sections", limit_choices_to={'is_doctor': False})
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="sections")
    classs = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="sections")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="sections")

    date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_std = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_code = generate_unique_code()
            while Section.objects.filter(slug=unique_code).exists():
                unique_code = generate_unique_code()
            self.slug = unique_code

        duration = self.DepCourse.course.duration
        self.end_date = self.date + duration
            
        super().save(*args, **kwargs)

    def get_url(self, url):
        urls = {
            'detail': reverse('attend:section_detail', kwargs={'slug': self.slug}),
            'ativate': reverse('attend:section_ativate', kwargs={'slug': self.slug}),
            'update': reverse('attend:section_update', kwargs={'slug': self.slug}),
            'delete': reverse('attend:section_delete', kwargs={'slug': self.slug}),
            }
        return urls.get(url)
        
    def excel_filename(self):
        return f"SEC {self.DepCourse.course.name} G{self.group.number} c{self.classs.number} date {self.date.day}-{self.date.month}.xlsx"

    def __str__(self):
        return f"#{self.id} {self.DepCourse.course.name}, Audiance: {self.classs}"
    
class Lecture(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    DepCourse = models.ForeignKey(DepCourse, on_delete=models.CASCADE, related_name="lectures")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="lectures", limit_choices_to={'is_doctor': True})
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="lectures")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="lectures")

    date = models.DateTimeField()
    end_date = models.DateTimeField(blank=True, null=True)
    is_std = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_code = generate_unique_code(length=7)
            while Lecture.objects.filter(slug=unique_code).exists():
                unique_code = generate_unique_code(length=7)
            self.slug = unique_code

        duration = self.DepCourse.course.duration
        self.end_date = self.date + duration

        super().save(*args, **kwargs)

    def get_url(self, url):
        urls = {
            'detail': reverse('attend:lecture_detail', kwargs={'slug': self.slug}),
            'ativate': reverse('attend:lecture_ativate', kwargs={'slug': self.slug}),
            'update': reverse('attend:lecture_update', kwargs={'slug': self.slug}),
            'delete': reverse('attend:lecture_delete', kwargs={'slug': self.slug}),
            }
        return urls.get(url)

    def excel_filename(self):
        return f"SEC {self.DepCourse.course.name} G{self.group.number} date {self.date.day}-{self.date.month}.xlsx"

    def __str__(self):
        return f"#{self.id} {self.DepCourse.course.name}, Audiance: {self.group}"


class SpecialEvent(models.Model):
    slug = models.SlugField(unique=True, blank=True)
    case = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    students = models.CharField(max_length=150, blank=True, null=True)
    session_type_CHOICES = (
        ('Lec', 'Lec'),
        ('Sec', 'Sec'),
    )
    session_type = models.CharField(max_length=3, choices=session_type_CHOICES, default='Lec')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="specialevents", blank=True, null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="specialevents")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="specialevents")
    doctor_name = models.CharField(max_length=150, blank=True)
    subject_name = models.CharField(max_length=150, blank=True, null=True)
    time = models.CharField(max_length=150, blank=True, null=True)
    pic_id = models.PositiveSmallIntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="specialevents")
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_code = generate_unique_code(length=6)
            while SpecialEvent.objects.filter(slug=unique_code).exists():
                unique_code = generate_unique_code(length=6)
            self.slug = unique_code
        
        self.doctor_name = str(self.doctor) if not self.doctor_name else self.doctor_name
        dwin_available = self.doctor.dwin_img or None
        self.pic_id = dwin_available if dwin_available else 3

        current_date = timezone.localtime()
        event_date = timezone.localtime(self.date)
        if current_date < event_date:
            difference = event_date - current_date
            total_minutes = difference.total_seconds() / 60

            # Get hours and minutes
            hours = int(total_minutes / 60) - 1 
            minutes = int(total_minutes % 60)              
            self.time = f"Starts in {hours} H {minutes} M" if hours > 0 else f"Starts in {minutes} M"

        else:
            if self.duration:
                start_time = event_date.strftime("%I:%M %p")
                final_date = event_date + timedelta(minutes=self.duration)
                end_time = final_date.strftime("%I:%M %p")
                self.time = f"Time: {start_time} - {end_time}"
            else:
                self.time = f"Time: {start_time}"
                
        if not self.subject_name:
            self.subject_name = 'General'
        super().save(*args, **kwargs)

    def get_data(self): 
        data = {
            "event_model_name": SpecialEvent,
            "event_slug": self.slug,
            "id": self.id,
            "case": self.case,
            "students": self.students,
            "session_type": self.session_type,
            "department_name": 'Department: ' + self.department.name,
            "college_name": self.college.name,
            "doctor_name": self.doctor_name,
            "subject_name": self.subject_name,
            "time": self.time,
            "pic_id": self.pic_id,
            }

        return data
        
    def __str__(self):
        return f"#{self.id} {self.time}, duration: {self.duration}, room {self.room}"

class OfficeScreen(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="screen")
    text_1 = models.CharField(max_length=255, blank=True, null=True)
    text_2 = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return str(self.doctor.name)
