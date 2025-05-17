from django import forms

from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import *

    
    
class SectionForm(forms.ModelForm):
    college = forms.ModelChoiceField(queryset=College.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    year = forms.IntegerField()
    class Meta:
        model = Section
        fields = ['DepCourse', 'doctor', 'group', 'classs', 'date', 'end_date', 'room', 'is_std']
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M') 
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M') 
            }),
        }

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)        

        self.fields['doctor'].queryset = Doctor.objects.none()
        self.fields['department'].queryset = Doctor.objects.none()
        self.fields['DepCourse'].queryset = Doctor.objects.none()
        self.fields['group'].queryset = Doctor.objects.none()
        self.fields['classs'].queryset = Doctor.objects.none()


        if self.instance.pk:
            dofaa = self.instance.group.dofaa
            self.fields['year'].initial = dofaa.academic_year
            self.fields['doctor'].queryset = self.instance.DepCourse.course.doctors.filter(is_doctor=False).order_by('name')
            self.fields['department'].queryset = self.instance.DepCourse.department.college.departments.order_by('name')
            self.fields['DepCourse'].queryset = self.instance.DepCourse.department.depcourses.filter(academic_year=dofaa.academic_year).order_by('course__name')
            self.fields['group'].queryset = self.instance.DepCourse.department.groups.filter(dofaa=dofaa).order_by('number')
            self.fields['classs'].queryset = self.instance.group.classes.order_by('number')
            self.fields['college'].initial = self.instance.DepCourse.department.college
            self.fields['department'].initial = self.instance.DepCourse.department
        if 'college' or 'department' or 'year' or 'DepCourse' or 'group' in self.data: 
            try:
                college_id = int(self.data.get('college'))
                department_id = int(self.data.get('department'))
                group_id = int(self.data.get('group'))
                course_id = int(self.data.get('DepCourse'))
                year = int(self.data.get('year'))

                dofaa = get_object_or_404(Dofaa, academic_year=year)
                self.fields['department'].queryset = get_object_or_404(College, pk=college_id).departments.order_by('name')
                self.fields['group'].queryset = get_object_or_404(Department, pk=department_id).groups.filter(dofaa=dofaa).order_by('number')
                self.fields['classs'].queryset = get_object_or_404(Group, pk=group_id).classes.order_by('number')
                self.fields['DepCourse'].queryset = get_object_or_404(Department, pk=department_id).depcourses.filter(academic_year=year).order_by('course__name')
                self.fields['doctor'].queryset = get_object_or_404(DepCourse, pk=course_id).course.doctors.filter(is_doctor=False).order_by('name')
            except (ValueError, TypeError):
                pass  
            
class LectureForm(forms.ModelForm):
    college = forms.ModelChoiceField(queryset=College.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    year = forms.IntegerField()
    class Meta:
        model = Lecture
        fields = ['DepCourse', 'doctor', 'group', 'date', 'end_date', 'room', 'is_std']
        widgets = {
            'date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M') 
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M') 
            }),
        }

    def __init__(self, *args, **kwargs):
        super(LectureForm, self).__init__(*args, **kwargs)        

        self.fields['doctor'].queryset = Doctor.objects.none()
        self.fields['department'].queryset = Doctor.objects.none()
        self.fields['DepCourse'].queryset = Doctor.objects.none()
        self.fields['group'].queryset = Doctor.objects.none()


        if self.instance.pk:
            dofaa = self.instance.group.dofaa
            self.fields['year'].initial = dofaa.academic_year
            self.fields['doctor'].queryset = self.instance.DepCourse.course.doctors.filter(is_doctor=True).order_by('name')
            self.fields['department'].queryset = self.instance.DepCourse.department.college.departments.order_by('name')
            self.fields['DepCourse'].queryset = self.instance.DepCourse.department.depcourses.filter(academic_year=dofaa.academic_year).order_by('course__name')
            self.fields['group'].queryset = self.instance.DepCourse.department.groups.filter(dofaa=dofaa).order_by('number')
            self.fields['college'].initial = self.instance.DepCourse.department.college
            self.fields['department'].initial = self.instance.DepCourse.department
        if 'college' or 'department' or 'year' or 'DepCourse'in self.data: 
            try:
                college_id = int(self.data.get('college'))
                department_id = int(self.data.get('department'))
                course_id = int(self.data.get('DepCourse'))
                year = int(self.data.get('year'))

                dofaa = get_object_or_404(Dofaa, academic_year=year)
                self.fields['department'].queryset = get_object_or_404(College, pk=college_id).departments.order_by('name')
                self.fields['group'].queryset = get_object_or_404(Department, pk=department_id).groups.filter(dofaa=dofaa).order_by('number')
                self.fields['DepCourse'].queryset = get_object_or_404(Department, pk=department_id).depcourses.filter(academic_year=year).order_by('course__name')
                self.fields['doctor'].queryset = get_object_or_404(DepCourse, pk=course_id).course.doctors.filter(is_doctor=True).order_by('name')
            except (ValueError, TypeError):
                pass  


class OfficeScreenForm(forms.ModelForm):
    class Meta:
        model = OfficeScreen
        fields = ['text_1', 'text_2']
        widgets = {
            'text_1': forms.TextInput(attrs={'class': 'form-control'}),
            'text_2': forms.TextInput(attrs={'class': 'form-control'}),
        }