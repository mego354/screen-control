from django.contrib import admin
from .models import *

admin.site.site_header = "BATU Attendance"
admin.site.site_title = "BATU Attendance Admin Portal"
admin.site.index_title = "Welcome to BATU Attendance"

class AdminUser(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name")
    search_fields = ('first_name',)

class AdminLecture(admin.ModelAdmin):
    list_display = ("id" ,"DepCourse" ,"doctor", "group", "room", "date")
    search_fields = ('id',)
    list_filter = ('DepCourse','doctor','group','room','date','is_std',)
class AdminSection(admin.ModelAdmin):
    list_display = ("id" ,"DepCourse" ,"doctor", "group", "classs", "room", "date")
    search_fields = ('id',)
    list_filter = ('DepCourse','doctor','group','classs','room','date','is_std',)

class AdminDofaa(admin.ModelAdmin):
    list_display = ("id", "year", "academic_year", "is_done")
class AdminDoctor(admin.ModelAdmin):
    list_display = ("id", "name", "is_doctor")
class AdminCourse(admin.ModelAdmin):
    list_display = ("id", "name")
class AdminDepCourse(admin.ModelAdmin):
    list_display = ("id", "course", "department", "academic_year")
class AdminCollege(admin.ModelAdmin):
    list_display = ("id", "name")
class AdminDepartment(admin.ModelAdmin):
    list_display = ("id" ,"name", "college")
class AdminGroup(admin.ModelAdmin):
    list_display = ("dofaa" ,"department", "number")

class AdminClass(admin.ModelAdmin):
    list_display = ("get_group_dof" ,"get_group_dep", "get_group_num", "number")

    def get_group_dof(self, obj):
        return obj.group.dofaa
    def get_group_dep(self, obj):
        return obj.group.department
    def get_group_num(self, obj):
        return obj.group.number

    get_group_dof.short_description = "dofaa"
    get_group_dep.short_description = "department"    
    get_group_num.short_description = "group"    

    # Enable sorting
    get_group_dof.admin_order_field = "group__dofaa"
    get_group_dep.admin_order_field = "group__department"
    get_group_num.admin_order_field = "group__number"

class AdminRoom(admin.ModelAdmin):
    list_display = ("id" ,"name", "ip")
class AdminSpecialEvent(admin.ModelAdmin):
    list_display = ("case" ,"doctor" ,"time", "pic_id", "room", "date")


admin.site.register(Dofaa, AdminDofaa)
admin.site.register(User, AdminUser)
admin.site.register(Doctor, AdminDoctor)
admin.site.register(Course, AdminCourse)
admin.site.register(DepCourse, AdminDepCourse) 
admin.site.register(College, AdminCollege)
admin.site.register(Department, AdminDepartment)
admin.site.register(Group, AdminGroup)
admin.site.register(Class, AdminClass)
admin.site.register(Room, AdminRoom)
admin.site.register(SpecialEvent, AdminSpecialEvent)
admin.site.register(Lecture, AdminLecture)
admin.site.register(Section, AdminSection)



@admin.register(OfficeScreen)
class OfficeScreenAdmin(admin.ModelAdmin):
    list_display = ('doctor_name', 'text_1', 'text_2')
    search_fields = ('doctor__name', 'text_1', 'text_2')

    def doctor_name(self, obj):
        return obj.doctor.name
    doctor_name.short_description = 'Doctor'
