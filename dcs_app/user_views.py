from django.shortcuts import render, redirect, get_object_or_404
from .models import User_Reg, Employee_Booking, Employee_Category, Employee_Reg, Feedback, Complaint, Feedbk
from django.contrib import messages
from .forms import BookingForm, ComplaintForm, FeedbackForm

def user_login(request):
    if request.method == 'GET':
        return render(request, 'dcs_app/user/user_login.html')
    if request.method == 'POST':
        user_phone = request.POST["user_phone"]
        user_pass = request.POST["user_password"]
        user_list = User_Reg.objects.filter(u_phone=user_phone, u_pass=user_pass)
        size = len(user_list)
        if size>0:
            request.session["session_key"] = user_phone
            redirect_url = request.session.pop('redirect_url', None)
            if redirect_url:
                return redirect(redirect_url)
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid Credentials")
        

             
def user_registration(request):
    if request.method == 'GET':
        return render(request, 'dcs_app/user/user_registration.html')
    if request.method == 'POST':
        user_name = request.POST["name"]
        user_password = request.POST["password"]
        user_email = request.POST["email"]
        user_phone = request.POST["phone"]
        user_city = request.POST["city"]
        user_pic = request.FILES.get("pic")
        user_addr = request.POST["address"]
        user_registration_obj = User_Reg(u_name=user_name, u_pass=user_password, u_pic=user_pic,u_email=user_email, u_phone=user_phone, u_city=user_city, u_addr=user_addr)
        user_registration_obj.save()
        messages.success(request, 'Registered')
        return redirect('user_login')
    


def user_edit_profile(request):
    user_details = request.session["session_key"]
    user_obj = User_Reg.objects.get(u_phone=user_details)
    context = {"user":user_obj}
    if request.method == 'GET':
        return render(request, 'dcs_app/user/user_edit_profile.html', context)
    if request.method == 'POST':
        n_name = request.POST["name"]
        n_email = request.POST["email"]
        n_phone = request.POST["phone"]
        n_city = request.POST["city"]
        n_addr = request.POST["address"]
        user_obj.u_name=n_name
        user_obj.u_email=n_email
        user_obj.u_phone=n_phone
        user_obj.u_city=n_city
        user_obj.u_addr=n_addr
        user_obj.save()
        return render(request, 'dcs_app/user/home.html', context)


def booking_req(request, employee_id):
    if request.method == 'GET':
        user_phone = request.session.get("session_key")
        if not user_phone:
            request.session['redirect_url'] = request.get_full_path()
            return redirect('user_login')
        
        user = User_Reg.objects.get(u_phone=user_phone) 
        employee = Employee_Reg.objects.get(emp_phone=employee_id)
        form = BookingForm(initial={'user': user.u_name, 'employee': employee.emp_name})
        return render(request, 'dcs_app/user/booking_req.html', {'form': form, 'employee': employee, "user":user})

    elif request.method == 'POST':
        user_phone = request.session.get("session_key")
        if user_phone:
            user = User_Reg.objects.get(u_phone=user_phone) 
            employee = Employee_Reg.objects.get(emp_phone=employee_id)
            form = BookingForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.user = user
                form.instance.employee = employee
                form.save()
                return redirect('show_bookings')
            else:
                messages.error(request, "Booking failed. Please check the form.")
                return redirect('home')
        else:
            messages.error(request, "You need to login first.")
            return redirect('user_login')


def show_bookings(request):
    user_phone = request.session.get("session_key")
    if not user_phone:
        messages.error(request, "You need to login first.")
        return redirect('user_login')

    user = User_Reg.objects.get(u_phone=user_phone)

    bookings = Employee_Booking.objects.filter(user=user)

    return render(request, 'dcs_app/user/show_bookings.html', {'bookings': bookings, "user":user})



def hide_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Employee_Booking, pk=booking_id)
        booking.visibility = False
        booking.status = 'Pending'
        booking.save()
        return redirect('show_bookings')
    return redirect('home')



def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(Employee_Booking, pk=booking_id)
        booking.delete()
        return redirect('show_bookings')
    return redirect('home')



def complaint(request, booking_id):
    booking_obj = get_object_or_404(Employee_Booking, pk=booking_id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.instance.booking = booking_obj
            form.save()
            return redirect('show_bookings')
    else:
        form = ComplaintForm()
    return render(request, 'dcs_app/user/complaint.html', {'form': form})



def feedback(request, booking_id):
    user_phone = request.session.get("session_key")
    feedback_obj = get_object_or_404(Employee_Booking, pk=booking_id)
    feedback_instance, create = Feedback.objects.get_or_create(feedback=feedback_obj)
    user = User_Reg.objects.get(u_phone=user_phone)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback_instance)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FeedbackForm(instance=feedback_instance)
    return render(request, 'dcs_app/user/feedback.html', {'form': form, 'user':user})



def delete_feedback(request, feedback_id):
    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, pk=feedback_id)
        feedback.delete()
        return redirect('home')
    return redirect('home')


def inbox(request):
    user_phone = request.session.get("session_key")
    user = User_Reg.objects.get(u_phone=user_phone)
    complaints = Complaint.objects.filter(booking__user = user)
    return render(request, 'dcs_app/user/inbox.html', {'complaints': complaints, 'user':user})



def logout(request):
    request.session.flush()
    return redirect('home')


def feedbk(request):
    if request.method == 'GET':
        return render(request, 'dcs_app/user/feedbk.html')
    if request.method == 'POST':
        remark = request.POST["remark"]
        rating = request.POST["rating"]
        feedobj = Feedbk()
        feedobj.user = User_Reg.objects.get(pk=request.session.get('session_key'))
        feedobj.rating = rating
        feedobj.remark = remark
        feedobj.save()
        messages.success(request, 'Feedback Recorded Succefully')
        return redirect('home')