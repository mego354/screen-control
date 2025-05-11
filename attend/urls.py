from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.views.generic import TemplateView

from . import views
from . import api
from .models import Section ,Lecture
from .forms import LectureForm, SectionForm

from django.contrib.auth import views as auth_views

app_name = 'attend' 
urlpatterns = [
    path('', views.TableListView.as_view(), name='TableListView'), 
    path('standard-table/create/lecture/', views.GeneralCreateView.as_view(model=Lecture, form_class=LectureForm, template_name='events/lecture_form.html'), name='lecture_create'),
    path('standard-table/create/section/', views.GeneralCreateView.as_view(model=Section, form_class=SectionForm, template_name='events/section_form.html'), name='section_create'),
    path('standard-table/lecture/<slug:slug>/', views.GeneralDetailView.as_view(model=Lecture), name='lecture_detail'),
    path('standard-table/section/<slug:slug>/', views.GeneralDetailView.as_view(model=Section), name='section_detail'), 
    path('standard-table/lecture/<slug:slug>/update/', views.GeneralUpdateView.as_view(model=Lecture, form_class=LectureForm, template_name='events/lecture_form.html'), name='lecture_update'),
    path('standard-table/section/<slug:slug>/update/', views.GeneralUpdateView.as_view(model=Section, form_class=SectionForm, template_name='events/section_form.html'), name='section_update'), 
    path('standard-table/lecture/<slug:slug>/delete/', views.GeneralDeleteView.as_view(model=Lecture), name='lecture_delete'),
    path('standard-table/section/<slug:slug>/delete/', views.GeneralDeleteView.as_view(model=Section), name='section_delete'), 
    path('standard-table/lecture/<slug:slug>/ativate/', views.AtivateEventRedirectView.as_view(model=Lecture, pattern_name='attend:lecture_detail'), name='lecture_ativate'),
    path('standard-table/section/<slug:slug>/ativate/', views.AtivateEventRedirectView.as_view(model=Section, pattern_name='attend:section_detail'), name='section_ativate'),


    # dwin APIs
    path('room/<str:room_code>/', views.RoomDataView.as_view(), name='room'),
    path('room/<str:room_code>/list/', views.RoomPicturesListView.as_view(), name='room_pictures'),
    path('doc_img/<int:doc_id>/', api.doc_img, name='doc_img'),

    # API
    path('ajax/load-departments/', api.load_departments, name='ajax_load_departments'),
    path('ajax/load-courses/', api.load_depcourses, name='ajax_load_courses'), 
    path('ajax/load-doctors/', api.load_doctors, name='ajax_load_doctors'),
    path('ajax/load-groups/', api.load_groups, name='ajax_load_groups'), 
    path('ajax/load-classes/', api.load_classes, name='ajax_load_classes'),

]
 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

