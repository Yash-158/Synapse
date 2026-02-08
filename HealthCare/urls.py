from django.contrib import admin
from django.urls import path, include
from . import views 
urlpatterns = [
    path('', views.rolepage, name="rolepage"),
    path('hospitallogin/', views.hospitallogin, name="hospitallogin"),
    path('patientlogin/', views.patientlogin, name="patientlogin"),
    path('hospitaldashboard/', views.hospitaldashboard, name="hospitaldashboard"),
    path('patientdashboard/', views.patientdashboard, name="patientdashboard"),
    path('patientregister/', views.patientregister, name="patientregister"),
    path('hospitalregister/', views.hospitalregister, name='hospitalregister'),
    path('emr/', views.emr, name="emr"),
    path('search_patient/', views.search_patient, name='search_patient'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('doctorregister/', views.doctorregister, name='doctorregister'),
    path('managestaff/', views.managestaff, name='managestaff'),
    path('book-appointment/', views.create_appointment, name='book_appointment'),
    path("appointments/", views.appointment_management, name="appointment_management"),
    path("appointments/approve/<int:appointment_id>/", views.approve_appointment, name="approve_appointment"),
    path("appointments/reject/<int:appointment_id>/", views.reject_appointment, name="reject_appointment"),
    path('delete_staff/<str:role>/<str:staff_id>/', views.delete_staff, name='delete_staff'),
    path('edit_doctor/<str:license_number>/', views.edit_doctor, name='edit_doctor'),

]
