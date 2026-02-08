from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import CustomUser, Hospital, Doctor, Nurse, Technician, Receptionist, SupportStaff, Pharmacist, Patient, Appointment, Inpatient, MedicalHistory
from django.contrib.auth import authenticate, login
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from .models import Patient
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment




import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMessage(Name, Username, Password, receiveremail):
    sender_email = "websiteyash@gmail.com"  # Your email address
    receiver_email = receiveremail  # Recipient's email address
    subject = "Welcome to Our Service"

    # HTML Email Template with dynamic username & password
    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome to Our Service</title>
        <style>
            body {{ font-family: Arial, sans-serif; background: #f4f4f4; }}
            .container {{ max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }}
            .header {{ background: #2d47d5; color: white; padding: 20px; text-align: center; font-size: 24px; border-radius: 8px 8px 0 0; }}
            .content {{ padding: 20px; text-align: center; color: #343a40; }}
            .content h2 {{ color: #2d47d5; }}
            .test-card {{ background: #2d47d5; color: white; padding: 15px; border-radius: 8px; margin-top: 20px; }}
            .footer {{ padding: 15px; background: #ddd; text-align: center; font-size: 14px; border-radius: 0 0 8px 8px; }}
            .action-button {{ background: #2d47d5; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">Welcome, {Name}!</div>
            <div class="content">
                <h2>Thank you for signing up!</h2>
                <p>Your login details:</p>
                <div class="test-card">
                    <h3>Username: {Username}</h3>
                    <h3>Password: {Password}</h3>
                </div>
                <p>Click below to log in:</p>
                <a href="http://127.0.0.1:8000/patientlogin/" class="action-button" style="color: aliceblue;">Login Now</a>
            </div>
            <div class="footer">&copy; 2025 Your Company. All rights reserved.</div>
        </div>
    </body>
    </html>
    """
      # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'html'))  # Attach HTML content

    # Gmail SMTP Server
    gmail_password = "gspl bdsf qwde ksgp"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Secure connection
            server.login(sender_email, gmail_password)  # Log in
            server.sendmail(sender_email, receiver_email, msg.as_string())  # Send email
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")






















def rolepage(request):
    return render(request, 'HealthCare/rolepage.html')

def loginuser(request):
    return render(request, 'HealthCare/login.html')

# @login_required
def hospitaldashboard(request):
        return render(request, 'HealthCare/hospitaldashboard.html')



def patientdashboard(request):
    user = request.user
    
    try:
        patient = user.patient  # Access the related Patient object
        dob = patient.dob  # Assuming the dob field exists in your Patient model

        # Calculate the age based on the date of birth and the current date
        if dob:
            current_date = datetime.now()
            age = relativedelta(current_date, dob)
            age_years = age.years  # Extract the number of years (age)
        else:
            age_years = None  # In case dob is not provided or invalid

    except Patient.DoesNotExist:
        patient = None  # Handle the case where the user doesn't have an associated Patient record
        age_years = None

    return render(request, 'HealthCare/patientdashboard.html', {'patient': patient, 'age': age_years})


def emr(request):
    return render(request, 'HealthCare/emr.html')

def adminpage(request):
    return render(request, 'HealthCare/adminpage.html')

def patientregister(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        aadhaar_number = request.POST.get('governmentId')
        first_name = request.POST.get('firstName')
        middle_name = request.POST.get('middleName', '')
        last_name = request.POST.get('lastName')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('maritalStatus')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        bloodgroup = request.POST.get('bloodgroup')
        allergies = request.POST.get('allergies')
        contact_number = request.POST.get('contactNumber')
        email = request.POST.get('email')
        permanent_address = request.POST.get('permanentAddress')
        emergency_contact_name = request.POST.get('emergencyContactName')
        emergency_contact_number = request.POST.get('emergencyContactNumber')
        password = contact_number

        # Check if Aadhaar Number is already registered
        if CustomUser.objects.filter(username=aadhaar_number).exists():
            messages.error(request, "Aadhaar Number already registered")
            return redirect('register_patient')

        # Create the CustomUser object
        user = CustomUser.objects.create_user(
            username=aadhaar_number, 
            password=password, 
            role='PATIENT'
        )

        # Create Patient Profile
        Patient.objects.create(
            user=user,
            aadhaar_number=aadhaar_number,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            dob=dob,
            gender=gender,
            marital_status=marital_status,
            weight=weight,
            height=height,
            bloodgroup=bloodgroup,
            allergies=allergies,
            contact_number=contact_number,
            email=email,
            permanent_address=permanent_address,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_number=emergency_contact_number
        )

        sendMessage(first_name, aadhaar_number, contact_number, email)

        # Log in the user
        # login(request, user)
        return redirect('hospitaldashboard')

    return render(request, "HealthCare/patientregister.html")

def hospitalregister(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        hospital_id = request.POST.get('hospital_id')  
        password = request.POST.get('password')
        name = request.POST.get('name')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        established_date = request.POST.get('established_date')
        hospital_type = request.POST.get('hospital_type')
        emergency_contact_number = request.POST.get('emergency_contact_number')

        # Log the hospital_id to ensure it's the correct value
        print(f"Trying to register hospital with hospital_id: {hospital_id}")

        # Check if a hospital with the given hospital_id already exists
        # if Hospital.objects.filter(hospital_id=hospital_id).exists():
        #     print(f"Hospital with hospital_id {hospital_id} already exists")
        #     messages.error(request, "Hospital ID already registered")
        #     return redirect('hospitalregister')
        
        # Check if a CustomUser with the same hospital_id (username) already exists
        if CustomUser.objects.filter(username=hospital_id).exists():
            print(f"CustomUser with username (hospital_id) {hospital_id} already exists")
            messages.error(request, "A hospital with this ID already exists")
            return redirect('hospitalregister')

        # Create the CustomUser object for hospital registration
        user = CustomUser.objects.create_user(
            username=hospital_id,
            password=password,
            role='HOSPITAL'
        )

        # Create Hospital Profile
        Hospital.objects.create(
            user=user,
            hospital_id=hospital_id,  
            name=name,
            address=address,
            contact_number=contact_number,
            email=email,
            established_date=established_date,
            hospital_type=hospital_type,
            emergency_contact_number=emergency_contact_number
        )

        # Log in the user (optional)
        # login(request, user)
        return redirect('hospitaldashboard')  # Redirect to the hospital's dashboard

    return render(request, "HealthCare/hospitalregister.html")
















def nurseregister(request):
    if request.method == "POST":
        # Retrieve the data from the POST request
        license_number = request.POST.get('license_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        department = request.POST.get('department')
        hospital_affiliation_id = request.POST.get('hospital_affiliation')  # Hospital's ID

        # Check if the license number is already registered
        if CustomUser.objects.filter(username=license_number).exists():
            messages.error(request, "License Number already registered")
            return redirect('register_nurse')

        # Check if the hospital exists
        try:
            hospital_affiliation = Hospital.objects.get(hospital_id=hospital_affiliation_id)
        except Hospital.DoesNotExist:
            messages.error(request, "Hospital not found")
            return redirect('register_nurse')

        # Create CustomUser for Nurse registration
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(
            username=license_number,
            password=password,
            role='NURSE'  # Role set to NURSE for the nurse registration
        )

        # Create Nurse profile
        Nurse.objects.create(
            user=user,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            email=email,
            department=department,
            hospital_affiliation=hospital_affiliation,
        )

        # Log in the user
        login(request, user)
        return redirect('nurse_dashboard')  # Redirect to the nurse's dashboard after registration

    # Pass hospitals to the template to be used in the dropdown
    hospitals = Hospital.objects.all()
    return render(request, "register_nurse.html", {'hospitals': hospitals})




def technicianregister(request):
    if request.method == "POST":
        # Retrieve the data from the POST request
        technician_id = request.POST.get('technician_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        hospital_affiliation_id = request.POST.get('hospital_affiliation')  # Hospital's ID

        # Check if the technician ID is already registered
        if CustomUser.objects.filter(username=technician_id).exists():
            messages.error(request, "Technician ID already registered")
            return redirect('register_technician')

        # Check if the hospital exists
        try:
            hospital_affiliation = Hospital.objects.get(hospital_id=hospital_affiliation_id)
        except Hospital.DoesNotExist:
            messages.error(request, "Hospital not found")
            return redirect('register_technician')

        # Create CustomUser for Technician registration
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(
            username=technician_id,
            password=password,
            role='TECHNICIAN'  # Role set to TECHNICIAN for the technician registration
        )

        # Create Technician profile
        Technician.objects.create(
            user=user,
            technician_id=technician_id,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            email=email,
            hospital_affiliation=hospital_affiliation,
        )

        # Log in the user
        login(request, user)
        return redirect('technician_dashboard')  # Redirect to the technician's dashboard after registration

    # Pass hospitals to the template to be used in the dropdown
    hospitals = Hospital.objects.all()
    return render(request, "register_technician.html", {'hospitals': hospitals})




def receptionistregister(request):
    if request.method == "POST":
        # Retrieve the data from the POST request
        receptionist_id = request.POST.get('receptionist_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        hospital_affiliation_id = request.POST.get('hospital_affiliation')  # Hospital's ID

        # Check if the receptionist ID is already registered
        if CustomUser.objects.filter(username=receptionist_id).exists():
            messages.error(request, "Receptionist ID already registered")
            return redirect('register_receptionist')

        # Check if the hospital exists
        try:
            hospital_affiliation = Hospital.objects.get(hospital_id=hospital_affiliation_id)
        except Hospital.DoesNotExist:
            messages.error(request, "Hospital not found")
            return redirect('register_receptionist')

        # Create CustomUser for Receptionist registration
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(
            username=receptionist_id,
            password=password,
            role='RECEPTIONIST'  # Role set to RECEPTIONIST for the receptionist registration
        )

        # Create Receptionist profile
        Receptionist.objects.create(
            user=user,
            receptionist_id=receptionist_id,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            email=email,
            hospital_affiliation=hospital_affiliation,
        )

        # Log in the user
        login(request, user)
        return redirect('receptionist_dashboard')  # Redirect to the receptionist's dashboard after registration

    # Pass hospitals to the template to be used in the dropdown
    hospitals = Hospital.objects.all()
    return render(request, "register_receptionist.html", {'hospitals': hospitals})



def support_staff_register(request):
    if request.method == "POST":
        # Retrieve the data from the POST request
        supportStaff_id = request.POST.get('supportStaff_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        hospital_affiliation_id = request.POST.get('hospital_affiliation')  # Hospital's ID

        # Check if the support staff ID is already registered
        if CustomUser.objects.filter(username=supportStaff_id).exists():
            messages.error(request, "Support Staff ID already registered")
            return redirect('register_support_staff')

        # Check if the hospital exists
        try:
            hospital_affiliation = Hospital.objects.get(hospital_id=hospital_affiliation_id)
        except Hospital.DoesNotExist:
            messages.error(request, "Hospital not found")
            return redirect('register_support_staff')

        # Create CustomUser for Support Staff registration
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(
            username=supportStaff_id,
            password=password,
            role='SUPPORT_STAFF'  # Role set to SUPPORT_STAFF for the Support Staff registration
        )

        # Create Support Staff profile
        SupportStaff.objects.create(
            user=user,
            supportStaff_id=supportStaff_id,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            email=email,
            hospital_affiliation=hospital_affiliation,
        )

        # Log in the user
        login(request, user)
        return redirect('support_staff_dashboard')  # Redirect to the Support Staff's dashboard after registration

    # Pass hospitals to the template to be used in the dropdown
    hospitals = Hospital.objects.all()
    return render(request, "register_support_staff.html", {'hospitals': hospitals})




def pharmacist_register(request):
    # Check if user is logged in
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not authenticated

    if request.method == "POST":
        # Retrieve the data from the POST request
        license_number = request.POST.get('license_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Get the hospital that the user is currently logged into
        hospital_affiliation = request.user.hospital_affiliation  # Assuming user has access to a hospital via a foreign key

        # Check if the pharmacist ID (license_number) is already registered
        if CustomUser.objects.filter(username=license_number).exists():
            messages.error(request, "Pharmacist license number already registered.")
            return redirect('register_pharmacist')

        # Create CustomUser for Pharmacist registration
        password = request.POST.get('password')
        user = CustomUser.objects.create_user(
            username=license_number,
            password=password,
            role='PHARMACIST'  # Role set to PHARMACIST for the pharmacist registration
        )

        # Create Pharmacist profile
        Pharmacist.objects.create(
            user=user,
            license_number=license_number,
            first_name=first_name,
            last_name=last_name,
            contact_number=contact_number,
            email=email,
            hospital_affiliation=hospital_affiliation,  # Assign hospital affiliation to the logged-in hospital
        )

        # Log in the user
        login(request, user)
        return redirect('pharmacist_dashboard')  # Redirect to the pharmacist's dashboard after registration

    # Pass the logged-in user's hospital to the template
    # hospital = request.user.hospital_affiliation  # Assuming hospital affiliation is stored in CustomUser model
    hospital = Hospital.objects.all()

    return render(request, "register_pharmacist.html", {'hospital': hospital})




def hospitallogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(user.role)
            if user.role != 'PATIENT':  # Check if the user has the 'HOSPITAL' role
                login(request, user)
                return redirect('hospitaldashboard')  # Redirect to the hospital's dashboard
            else:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('hospitallogin')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('hospitallogin')

    return render(request, 'HealthCare/hospitallogin.html')





def patientlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username , password=password)
        
        if user is not None:
            if user.role == 'PATIENT':  # Check if the user has the 'PATIENT' role
                login(request, user)
                return redirect('patientdashboard')  # Redirect to the patient's dashboard
            else:
                messages.error(request, "You are not authorized to access this page.")
                return redirect('patientlogin')
        else:
            messages.error(request, "Invalid Aadhaar number or password.")
            return redirect('patientlogin')

    return render(request, 'HealthCare/patientlogin.html')




def search_patient(request):
    aadhar_number = request.GET.get('aadhaar', None)  # Get Aadhar number from request
    if aadhar_number:
        try:
            patient = Patient.objects.get(aadhaar_number=aadhar_number)  # Fetch patient
            current_date = datetime.now()
            dob = patient.dob  # Assuming the dob field exists in your Patient model
            age = relativedelta(current_date, dob)
            
            # Convert age to a readable string format
            age_string = f"{age.years} years, {age.months} months, {age.days} days"

            data = {
                'name': patient.first_name,
                'age': age_string,  # Return age as a string
                'gender': patient.gender,
                'bloodGroup': patient.bloodgroup,
                'contact': patient.contact_number,
                'email': patient.email,
            }
            return JsonResponse({'success': True, 'data': data})
        except Patient.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Patient not found'})
    else:
        return JsonResponse({'success': False, 'message': 'Aadhaar number is required'})


# def managestaff(request):
#     return render(request , 'HealthCare/managestaff.html')











# def doctorregister(request):
#     if request.method == "POST":
#         # Retrieve the data from the POST request
#         license_number = request.POST.get('license_number')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         specialization = request.POST.get('specialization')
#         contact_number = request.POST.get('contact_number')
#         email = request.POST.get('email')
#         hospital_affiliation = request.POST.get('hospital_affiliation')  # This will store the Hospital's ID
#         password = request.POST.get('password')

#         # Check if the license number is already registered
#         if CustomUser.objects.filter(username=license_number).exists():
#             messages.error(request, "License Number already registered")
#             return redirect('doctorregister')

#         # Check if the hospital exists
#         try:
#             hospital = Hospital.objects.get(user=request.user)  # Accessing the hospital ID 
#         except Hospital.DoesNotExist:
#              return redirect('hospitallogin')

#         user = CustomUser.objects.create_user(
#             username=license_number,
#             password=password,
#             role='DOCTOR'  # Role set to DOCTOR for the doctor registration
#         )

#         # Create Doctor profile
#         Doctor.objects.create(
#             user = user,
#             license_number=license_number,
#             first_name=first_name,
#             last_name=last_name,
#             specialization=specialization,
#             contact_number=contact_number,
#             email=email,
#             hospital_affiliation=hospital_affiliation,
#         )

#         # Log in the user
#         # login(request, user)
#         return redirect('hospitaldashboard')  # Redirect to the doctor's dashboard after registration
#     context = {
#         'hospital_id': hospital.hospital_id  # Pass the hospital ID to the template for pre-selection
#     }
#     return render(request, 'HealthCare/doctorregister.html', context)



























# @login_required
def doctorregister(request):
    # Fetching the logged-in user's associated hospital
    try:
        # print(request.user.hospital_id)
        hospital = Hospital.objects.get(user=request.user)  # Accessing the hospital ID associated with the logged-in user
    except Hospital.DoesNotExist:
        return redirect('hospitallogin')

    if request.method == 'POST':
        # Extract form data
        license_number = request.POST.get('license_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        specialization = request.POST.get('specialization')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')

        # Check if the license_number (username) already exists
        if CustomUser.objects.filter(username=license_number).exists():
            messages.error(request, "Username (License Number) already exists. Please choose a different one.")
            return redirect('doctorregister')  # Redirect back to the registration page

        # Create a new user for the doctor
        user = CustomUser.objects.create_user(
            username=license_number,  # Use license number as username
            password=contact_number,  # You can set a default password or generate one
            role='DOCTOR',

        )
        
        # Create a Doctor object and associate it with the hospital
        doctor = Doctor.objects.create(
            user=user,  # Link the doctor user
            hospital_affiliation=hospital,  # Link the hospital
            first_name=first_name,
            last_name=last_name,
            license_number=license_number,
            specialization=specialization,
            contact_number=contact_number,
            email=email,  # Save the email in the doctor model as well
        )

        # Redirect to the admin page or another success page
        messages.success(request, "Doctor registered successfully!")
        return redirect('adminpage')

    # If GET request, render the registration form
    context = {
        'hospital_id': hospital.hospital_id  # Pass the hospital ID to the template for pre-selection
    }
    return render(request, 'HealthCare/doctorregister.html', context)






def create_appointment(request):
    if request.method == 'POST':
        patient = Patient.objects.get(user=request.user)  # Get logged-in patient
        hospital_id = request.POST.get('hospital_id')
        symptoms = request.POST.get('symptoms')
        
        hospital = Hospital.objects.get(hospital_id=hospital_id)  # Get selected hospital
        
        appointment = Appointment.objects.create(
            patient=patient,
            hospital=hospital,
            symptoms=symptoms,
            status='PENDING'
        )
        messages.success(request, "Appointment request sent to the hospital!")
        return redirect('patientdashboard')
    
    hospitals = Hospital.objects.all()  # Show available hospitals
    return render(request, 'HealthCare/book_appointment.html', {'hospitals': hospitals})


def approve_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    
    if request.user.customuser.role == 'HOSPITAL' and appointment.hospital.user == request.user:
        appointment.status = 'IN_QUEUE'
        appointment.save()
        messages.success(request, "Appointment added to queue.")
    
    return redirect('hospitaldashboard')



def start_treatment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    
    if request.user.customuser.role == 'DOCTOR' and appointment.hospital.user == request.user.hospital.user:
        appointment.status = 'UNDER_TREATMENT'
        appointment.doctor = request.user.doctor  # Assign doctor
        appointment.save()
        messages.success(request, "Patient is now under treatment.")
    
    return redirect('doctor_dashboard')


def add_inpatient_treatment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    
    if request.method == 'POST':
        treatment = request.POST.get('treatment')
        medications = request.POST.get('medications')

        inpatient = Inpatient.objects.create(
            appointment=appointment,
            treatment=treatment,
            medications=medications
        )
        
        messages.success(request, "Inpatient treatment recorded.")
        return redirect('doctor_dashboard')
    
    return render(request, 'HealthCare/inpatient_form.html', {'appointment': appointment})



def complete_treatment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    
    inpatient = Inpatient.objects.get(appointment=appointment)
    
    MedicalHistory.objects.create(
        patient=appointment.patient,
        hospital=appointment.hospital,
        doctor=appointment.doctor,
        diagnosis=inpatient.treatment,
        medications=inpatient.medications
    )
    
    appointment.status = 'COMPLETED'
    appointment.save()
    
    messages.success(request, "Treatment completed. Medical history updated.")
    return redirect('hospitaldashboard')


def appointment_management(request):
    hospital = request.user.hospital  # Assuming the hospital is linked to the logged-in user
    appointments = Appointment.objects.filter(hospital=hospital, status="PENDING")
    # return render(request, "'HealthCare/appointmentmanagement.html", {"appointments": appointments})
    return render(request, "HealthCare/appointmentmanagement.html", {"appointments": appointments})


def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Approved"
    appointment.save()
    return redirect("appointment_management")

def reject_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = "Rejected"
    appointment.save()
    return redirect("appointment_management")







from django.shortcuts import render, redirect, get_object_or_404
from .models import Doctor, Nurse, Technician, Receptionist, SupportStaff, Pharmacist, Hospital
from django.contrib.auth.decorators import login_required

# @login_required
def managestaff(request):
    doctors = Doctor.objects.all()
    nurses = Nurse.objects.all()
    technicians = Technician.objects.all()
    receptionists = Receptionist.objects.all()
    support_staffs = SupportStaff.objects.all()
    pharmacists = Pharmacist.objects.all()
    hospitals = Hospital.objects.all()

    return render(request, 'HealthCare/managestaff.html', {
        'doctors': doctors,
        'nurses': nurses,
        'technicians': technicians,
        'receptionists': receptionists,
        'support_staffs': support_staffs,
        'pharmacists': pharmacists,
        'hospitals': hospitals,
    })


# @login_required
def delete_staff(request, role, staff_id):
    # Mapping roles to their respective models
    model_mapping = {
        "doctor": Doctor,
        "nurse": Nurse,
        "technician": Technician,
        "receptionist": Receptionist,
        "support_staff": SupportStaff,
        "pharmacist": Pharmacist,
        "hospital": Hospital
    }

    # Get the corresponding model based on the role
    model = model_mapping.get(role.lower())

    if model:
        try:
            staff = get_object_or_404(model, pk=staff_id)
            staff.delete()
            return redirect('manage_staff')  # Redirect to manage staff page
        except Exception as e:
            print(f"Error deleting {role}: {e}")  # Debugging output

    return redirect('managestaff')



def edit_doctor(request, license_number):
    doctor = get_object_or_404(Doctor, license_number=license_number)

    if request.method == 'POST':
        doctor.first_name = request.POST.get('first_name')
        doctor.last_name = request.POST.get('last_name')
        doctor.specialization = request.POST.get('specialization')
        doctor.contact_number = request.POST.get('contact_number')
        doctor.email = request.POST.get('email')
        doctor.hospital_affiliation_id = request.POST.get('hospital_affiliation')
        
        doctor.save()
        return redirect('managestaff')  # Redirect to staff management page

    return render(request, 'HealthCare/edit_doctor.html', {'doctor': doctor})