from django.shortcuts import render, redirect, get_object_or_404
from .models import Comp_Reg, Employee_Category, Employee_Reg, JobApplication, Employee_Booking, Complaint, Hiring
from django.contrib import messages
from .forms import HiringForm
from django.http import JsonResponse


def company_login(request):
    key = request.session.get('session_key')
    if key:
        try:
            user = Comp_Reg.objects.filter(pk=key)
            if user:
                return redirect('company_home')
        except:
            return render(request, 'dcs_app/companies/company_login.html')

    if request.method == 'POST':
        comp_id = request.POST["compid"]
        comp_pass = request.POST["comp_password"]
        company_list = Comp_Reg.objects.filter(c_id=comp_id, c_pass=comp_pass, status=True)
        size = len(company_list)
        if size>0:
            request.session["session_key"] = comp_id
            comp_obj = Comp_Reg.objects.get(c_id=comp_id)
            context = {"comp":comp_obj}
            return redirect('company_home')
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'dcs_app/companies/company_login.html')
    
    if request.method == 'GET':
        return render(request, 'dcs_app/companies/company_login.html')
    

def company_registration(request):
    if request.method == 'GET':
        return render(request, 'dcs_app/companies/company_registration.html')
    if request.method == 'POST':
        comp_id = request.POST["cid"]
        comp_pass = request.POST["cpass"]
        comp_img = request.FILES.get("cpic")
        comp_name = request.POST["cname"]
        comp_ceo_name = request.POST["cceo"]
        comp_phone = request.POST["cphone"]
        comp_email = request.POST["cemail"]
        comp_city = request.POST["ccity"]
        comp_regno = request.POST["cregno"]
        comp_addr = request.POST["caddr"]
        comp_about = request.POST["cabout"]
        registration_obj = Comp_Reg(c_id=comp_id,c_pic=comp_img, c_pass=comp_pass, c_name=comp_name, c_ceo=comp_ceo_name, c_phone=comp_phone, c_email=comp_email, c_city=comp_city, c_regno=comp_regno, c_addr=comp_addr, c_about=comp_about)
        registration_obj.save()
        messages.success(request, 'Registered')
        return redirect('company_login')


def company_home(request):
    if "session_key" not in request.session.keys():
        return redirect("company_login")
    comp_details = request.session["session_key"]
    comp_obj = Comp_Reg.objects.get(c_id=comp_details)
    context = {"comp":comp_obj, 'user':comp_obj}
    return render(request, 'dcs_app/companies/company_home.html', context)


def company_edit_profile(request):
    if "session_key" not in request.session.keys():
        return redirect("company_login")
    comp_details = request.session["session_key"]
    comp_obj = Comp_Reg.objects.get(c_id=comp_details)
    context = {"comp":comp_obj, 'user':comp_obj}
    if request.method == 'GET':
        return render(request, 'dcs_app/companies/company_edit_profile.html', context)
    if request.method == 'POST':
        c_name = request.POST["name"]
        c_img = request.FILES.get("cpic")
        if c_img == None:
            c_img = comp_obj.c_pic.name

        c_email = request.POST["email"]
        c_phone = request.POST["phone"]
        c_city = request.POST["city"]
        c_addr = request.POST["address"]
        comp_obj.c_pic = c_img
        comp_obj.c_name = c_name
        comp_obj.c_email = c_email
        comp_obj.c_phone = c_phone
        comp_obj.c_city = c_city
        comp_obj.c_addr = c_addr
        comp_obj.save()
        return redirect('company_home')



def add_category(request):
    if "session_key" not in request.session.keys():
        return redirect("company_login")
    comp_details = request.session["session_key"]
    comp_obj = Comp_Reg.objects.get(c_id=comp_details)
    
    if request.method == 'GET':
        return render(request, 'dcs_app/companies/add_category.html',{'user':comp_obj})
    if request.method == 'POST':
        emp_categ = request.POST["emp_cat"]
        emp_desc = request.POST["emp_des"]
        emp_pic = request.FILES["epic"]
        add_obj = Employee_Category(comp_reg = comp_obj,emp_category_pic = emp_pic,  emp_category= emp_categ, emp_description = emp_desc)
        add_obj.save()
        messages.success(request, "Category Added Succefully")
        return redirect('add_category')


def add_workers(request):
    if "session_key" not in request.session.keys():
        return redirect("company_login")
    comp_details = request.session["session_key"]
    comp_obj = Comp_Reg.objects.get(c_id=comp_details)
    if request.method == 'GET':
        add_obj = Employee_Category.objects.filter(comp_reg = comp_details)
        context = {"categories":add_obj, 'user':comp_obj}
        return render(request, 'dcs_app/companies/add_workers.html', context)
    if request.method == 'POST':
        empcateg = request.POST["empcat"]
        emp_obj = Employee_Category.objects.get(emp_category=empcateg)
        empid = request.POST["empid"]
        empname = request.POST["empname"]
        empphone = request.POST["emppho"]
        empcity = request.POST["empcit"]
        empaddr = request.POST["empadd"]
        empstatus = request.POST["empsta"]
        emppic = request.FILES["emppic"]
        add_obj = Employee_Reg(emp_reg = emp_obj,emp_status=empstatus, emp_id=empid, emp_pic=emppic, emp_name=empname, emp_phone=empphone, emp_city=empcity, emp_addr=empaddr)
        add_obj.save()
        messages.success(request, 'Worker Added')
        return redirect('add_workers')


def show_category(request, c_id):
    if request.method == 'GET':
        add_obj = Employee_Category.objects.filter(comp_reg = c_id)
        context = {"add":add_obj}
        return render(request, 'dcs_app/companies/show_category.html', context)


def workers(request, id):
    if request.method == 'GET':
        emp_obj = Employee_Reg.objects.filter(emp_reg_id = id)
        context = {"emp":emp_obj}
        return render(request, 'dcs_app/companies/workers.html', context)


def hiring(request):
    if "session_key" not in request.session.keys():
        return redirect("company_login")
    comp_details = request.session["session_key"]
    comp_obj = Comp_Reg.objects.get(c_id=comp_details)
    if request.method == 'POST':
        form = HiringForm(request.session.get("session_key"),request.POST)
        if form.is_valid():
            comp_id = request.session.get("session_key")
            if comp_id:
                form.instance.company_id = comp_id
                form.instance.job_post_link = comp_id
                form.save()
                return redirect('careers')
            else:
                return redirect('company_login')
    else:
        form = HiringForm(request.session.get("session_key"))
    return render(request, 'dcs_app/companies/hiring.html', {'form': form, 'user':comp_obj})


def applicants(request):
    company_id = request.session.get("session_key")
    company = None
    if company_id:
        try:
            company = Comp_Reg.objects.get(c_id=company_id)
        except Comp_Reg.DoesNotExist:
            return redirect('company_login')
    else:
        return redirect('company_login')

    job_applications = JobApplication.objects.filter(hiring__company=company)
    return render(request, 'dcs_app/companies/applicants.html', {'job_applications': job_applications, 'user':company})


def bookings(request):
    company_id = request.session.get("session_key")
    if company_id:
        try:
            company = Comp_Reg.objects.get(c_id=company_id)
            bookings = Employee_Booking.objects.filter(employee__emp_reg__comp_reg=company)
            context = {'bookings': bookings, 'user':company}
            if request.method == 'POST':
                booking_id = request.POST.get('booking_id')
                booking_obj = Employee_Booking.objects.get(id=booking_id)
                status = request.POST['status']
                response = request.POST['response']
                if status == 'Cancel':
                    booking_obj.delete()
                    return render(request, 'dcs_app/companies/bookings.html', context)
                booking_obj.status = status
                booking_obj.response = response
                booking_obj.save()
            else:
                return render(request, 'dcs_app/companies/bookings.html', context)
            return render(request, 'dcs_app/companies/bookings.html', context)
        except Comp_Reg.DoesNotExist:
            return redirect('company_login')
    else:
        return redirect('company_login')


def show_complaints(request):
    company_id = request.session.get("session_key")
    company = None
    if company_id:
        try:
            company = Comp_Reg.objects.get(c_id=company_id)
        except Comp_Reg.DoesNotExist:
            return redirect('company_login')
    else:
        return redirect('company_login')
    complaints = Complaint.objects.filter(booking__employee__emp_reg__comp_reg=company)
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        complaint_obj = Complaint.objects.get(booking=complaint_id)
        resolve = request.POST['resolve']
        complaint_obj.resolve = resolve
        complaint_obj.save()
    return render(request, 'dcs_app/companies/show_complaints.html', {'complaints': complaints, 'user':company})


def check_existing_data(request):
    exists = False 
    if request.method == 'GET' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data_type = request.GET.get('data_type')
        data_value = request.GET.get('data_value')
        
        if data_type == 'cid':
            exists = Comp_Reg.objects.filter(c_id=data_value).exists()
        elif data_type == 'cemail':
            exists = Comp_Reg.objects.filter(c_email=data_value).exists()
        elif data_type == 'cphone':
            exists = Comp_Reg.objects.filter(c_phone=data_value).exists()
        
        return JsonResponse({'exists': exists})
    else:
        return JsonResponse({'error': 'Invalid request'})


def reject_applicant(request, pk):
    obj = JobApplication.objects.get(pk=pk)
    obj.delete()
    messages.success(request, 'Application Rejected')
    return redirect('applicants')


def accept_applicant(request, pk):
    app_obj = JobApplication.objects.get(pk=pk)
    wobj = Employee_Reg()
    wobj.emp_pic = app_obj.js_pic
    wobj.emp_name = app_obj.js_name
    wobj.emp_phone = app_obj.js_phone
    wobj.emp_reg = app_obj.hiring.job_category
    wobj.emp_status = 'Available'
    wobj.emp_city = app_obj.js_city
    wobj.emp_addr = app_obj.js_address
    wobj.emp_id = app_obj.pk
    wobj.save()
    messages.success(request, 'Employee Added to the Database')
    cobj = Hiring.objects.get(pk=app_obj.hiring.pk)
    cobj.job_seats = int(cobj.job_seats) - 1
    cobj.save()
    app_obj.visibility = False
    app_obj.save()
    if cobj.job_seats < 1:
        cobj.delete()
    return redirect('show_workers')


def show_workers(request):
    key = request.session.get('session_key')
    comp = None
    if key:
        try:
            comp = Comp_Reg.objects.get(pk=key)
        except:
            return redirect('company_login')
        obj = Employee_Reg.objects.filter(emp_reg__comp_reg=comp).order_by('emp_name')
        return render(request, 'dcs_app/companies/show_workers.html', {'user':comp, 'emp':obj})
    else:
        return redirect('company_login')


def company_logout(request):
    request.session.flush()
    return redirect("company_login")



