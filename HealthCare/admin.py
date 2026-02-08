from django.contrib import admin
from .models import CustomUser, Patient, Hospital, Doctor, Nurse, Technician, Receptionist, SupportStaff, Pharmacist

# Custom User Admin
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

# Patient Admin
class PatientAdmin(admin.ModelAdmin):
    list_display = ('aadhaar_number', 'first_name', 'last_name', 'dob', 'gender', 'email', 'contact_number')
    search_fields = ('aadhaar_number', 'first_name', 'last_name', 'email')
    list_filter = ('gender',)
    ordering = ('aadhaar_number',)

admin.site.register(Patient, PatientAdmin)

# Hospital Admin
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('hospital_id', 'name', 'contact_number', 'established_date', 'hospital_type')
    search_fields = ('hospital_id', 'name', 'contact_number')
    list_filter = ('hospital_type',)
    ordering = ('hospital_id',)

admin.site.register(Hospital, HospitalAdmin)

# Doctor Admin
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'first_name', 'last_name', 'specialization', 'hospital_affiliation', 'contact_number', 'email')
    search_fields = ('license_number', 'first_name', 'last_name', 'specialization', 'hospital_affiliation__name')
    list_filter = ('specialization', 'hospital_affiliation')
    ordering = ('license_number',)

admin.site.register(Doctor, DoctorAdmin)

# Nurse Admin
class NurseAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'first_name', 'last_name', 'department', 'hospital_affiliation', 'contact_number', 'email')
    search_fields = ('license_number', 'first_name', 'last_name', 'department', 'hospital_affiliation__name')
    list_filter = ('department', 'hospital_affiliation')
    ordering = ('license_number',)

admin.site.register(Nurse, NurseAdmin)

# Technician Admin
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ('technician_id', 'first_name', 'last_name', 'hospital_affiliation', 'contact_number', 'email')
    search_fields = ('technician_id', 'first_name', 'last_name', 'hospital_affiliation__name')
    list_filter = ('hospital_affiliation',)
    ordering = ('technician_id',)

admin.site.register(Technician, TechnicianAdmin)

# Receptionist Admin
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ('receptionist_id', 'first_name', 'last_name', 'hospital_affiliation', 'contact_number', 'email')
    search_fields = ('receptionist_id', 'first_name', 'last_name', 'hospital_affiliation__name')
    list_filter = ('hospital_affiliation',)
    ordering = ('receptionist_id',)

admin.site.register(Receptionist, ReceptionistAdmin)

# Support Staff Admin
class SupportStaffAdmin(admin.ModelAdmin):
    list_display = ('supportStaff_id', 'first_name', 'last_name', 'hospital_affiliation', 'contact_number', 'email')
    search_fields = ('supportStaff_id', 'first_name', 'last_name', 'hospital_affiliation__name')
    list_filter = ('hospital_affiliation',)
    ordering = ('supportStaff_id',)

admin.site.register(SupportStaff, SupportStaffAdmin)

# Pharmacist Admin
class PharmacistAdmin(admin.ModelAdmin):
    list_display = ('license_number', 'first_name', 'last_name', 'hospital_affiliation', 'contact_number', 'email')
    search_fields = ('license_number', 'first_name', 'last_name', 'hospital_affiliation__name')
    list_filter = ('hospital_affiliation',)
    ordering = ('license_number',)

admin.site.register(Pharmacist, PharmacistAdmin)

