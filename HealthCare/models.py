from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a user with an email, username, and password.
        """
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Encrypts the password before saving
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """
        Create and return a superuser with a username, email, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')  # Assign 'ADMIN' role to superuser
        
        return self.create_user(username, password, **extra_fields)





# User Roles
USER_ROLES = [
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('HOSPITAL', 'Hospital'),
        ('PHARMACY', 'Pharmacy'),
    ]

# Custom User Model (Using Django's Default Username & Password)
class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='PATIENT')

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    aadhaar_number = models.CharField(max_length=12, unique=True, primary_key=True, db_index=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)
    weight = models.FloatField()
    height = models.FloatField()
    bloodgroup = models.CharField(max_length=5)
    allergies = models.TextField()
    contact_number = models.CharField(max_length=10)
    email = models.EmailField()
    permanent_address = models.TextField()
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Patient: {self.user.username} ({self.aadhaar_number})"

from django.db import models

class Hospital(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    hospital_id = models.CharField(max_length=50, unique=True, primary_key=True)  # Unique 
    name = models.CharField(max_length=200)  # Name of the hospital
    address = models.TextField()  # Address of the hospital
    contact_number = models.CharField(max_length=15)  # Contact number of the hospital
    email = models.EmailField()  # Email address of the hospital
    established_date = models.DateField()  # Date the hospital was established
    hospital_type = models.CharField(max_length=100)  # Type of hospital (e.g., general, 
    emergency_contact_number = models.CharField(max_length=15)  # Emergency contact number

    def __str__(self):
        return self.name


# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)
    license_number = models.CharField(max_length=50, unique=True, primary_key=True)
    first_name = models.CharField(max_length=100)  # Doctor's first name
    last_name = models.CharField(max_length=100)  # Doctor's last name
    specialization = models.CharField(max_length=100)  
    contact_number = models.CharField(max_length=15)  # Doctor's contact number
    email = models.EmailField()  # Doctor's email address
    hospital_affiliation = models.ForeignKey(Hospital, on_delete=models.CASCADE) # foreign key dalni hai

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

# Nurse Model
class Nurse(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True, primary_key=True)  # Nurse's 
    first_name = models.CharField(max_length=100)  # Nurse's first name
    last_name = models.CharField(max_length=100)  # Nurse's last name
    contact_number = models.CharField(max_length=15)  # Nurse's contact number
    email = models.EmailField()  # Nurse's email address
    department = models.CharField(max_length=100)# Nurse's area of expertise (e.g.,
    hospital_affiliation = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Foreign key 
    
    def __str__(self):
        return f"Nurse: {self.user.username} ({self.department})"

# Technician Model
class Technician(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    technician_id = models.CharField(max_length=50, unique=True, primary_key=True)  # 
    first_name = models.CharField(max_length=100)  # Technician's first name
    last_name = models.CharField(max_length=100)  # Technician's last name
    contact_number = models.CharField(max_length=15)  # Technician's contact number
    email = models.EmailField()  # Technician's email address
    hospital_affiliation = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Foreign key 

    def __str__(self):
        return f"Technician: {self.user.username} ({self.field})"

# Receptionist Model
class Receptionist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    receptionist_id = models.CharField(max_length=50, unique=True, primary_key=True)  # Nurse's 
    first_name = models.CharField(max_length=100)  # Nurse's first name
    last_name = models.CharField(max_length=100)  # Nurse's last name
    contact_number = models.CharField(max_length=15)  # Nurse's contact number
    email = models.EmailField()  # Nurse's email address
    hospital_affiliation = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Foreign key

    def __str__(self):
        return f"Receptionist: {self.user.username}"

# Support Staff Model
class SupportStaff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    supportStaff_id = models.CharField(max_length=50, unique=True, primary_key=True)  # Nurse's 
    first_name = models.CharField(max_length=100)  # Nurse's first name
    last_name = models.CharField(max_length=100)  # Nurse's last name
    contact_number = models.CharField(max_length=15)  # Nurse's contact number
    email = models.EmailField()  # Nurse's email address
    hospital_affiliation = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Foreign key


    def __str__(self):
        return f"Support Staff: {self.user.username} ({self.job_title})"

# Pharmacist Model
class Pharmacist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50, unique=True, primary_key=True)  # Nurse's 
    first_name = models.CharField(max_length=100)  # Nurse's first name
    last_name = models.CharField(max_length=100)  # Nurse's last name
    contact_number = models.CharField(max_length=15)  # Nurse's contact number
    email = models.EmailField()  # Nurse's email address
    hospital_affiliation = models.ForeignKey(Hospital, on_delete=models.CASCADE)  # Foreign key 

    def __str__(self):
        return f"Pharmacist: {self.user.username}"









class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('IN_QUEUE', 'In Queue'),
        ('UNDER_TREATMENT', 'Under Treatment'),
        ('COMPLETED', 'Completed'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    symptoms = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class Inpatient(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    treatment = models.TextField()
    medications = models.TextField()
    admitted_at = models.DateTimeField(auto_now_add=True)
    discharged_at = models.DateTimeField(null=True, blank=True)

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medications = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

