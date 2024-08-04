from django.shortcuts import render, redirect, get_object_or_404
from .models import Feedback, Contact,Comp_Reg, Employee_Category, Hiring, User_Reg, Feedbk
from django.contrib import messages
from .forms import JobForm



def home(request):
    categories = Employee_Category.objects.all()
    company_list = Comp_Reg.objects.order_by('-date')
    all_feedback = Feedback.objects.all()
    feedbk = Feedbk.objects.all()
    user_details = request.session.get("session_key")
    user_obj = None
    if user_details:
        try:
            user_obj = User_Reg.objects.get(u_phone=user_details)
        except:
            try:
                user_obj = Comp_Reg.objects.get(pk=user_details)
            except:
                return render(request, 'dcs_app/html/index.html', {"categories":categories, "companies":company_list, "feedbacks":all_feedback, "user":user_obj})
    context = {"categories":categories, "companies":company_list, "feedbacks":all_feedback, "user":user_obj, 'feedbk':feedbk}
    return render(request, 'dcs_app/html/index.html', context)



def contact(request):
    if request.method == 'GET':
        return render(request, 'dcs_app/html/index.html')
    if request.method == 'POST':
        user_name = request.POST["name"]
        user_phone = request.POST["phone"]
        user_email = request.POST["email"] 
        user_question = request.POST["question"]
        contact_obj = Contact(name=user_name, phone=user_phone, email=user_email, question=user_question)
        contact_obj.save()
        messages.success(request, 'Contact Info Sent Succefully')
        return render(request, 'dcs_app/html/index.html')



def careers(request):
    if request.method == 'GET':
        career_obj = Hiring.objects.all().order_by('-job_lastdate_toapply')
        context = {"careers":career_obj}
        return render(request, 'dcs_app/html/careers.html', context)



def jobs(request, c_id):
    if request.method == 'POST':
        job_obj = get_object_or_404(Comp_Reg, c_id=c_id)
        hiring_obj = job_obj.hiring_set.first()
        form = JobForm(request.POST,  request.FILES)
        if form.is_valid():
            if job_obj:
                job_application = form.save(commit=False)
                job_application.hiring = hiring_obj
                job_application.save()
                messages.success(request, "Form Submitted")
                return redirect('jobs', c_id=c_id)
            else:
                return redirect('jobs')
    else:
        form = JobForm()
    return render(request, 'dcs_app/html/jobs.html', {'form': form})
   


def worker(request):
    categories = Employee_Category.objects.all()
    user_details = request.session.get("session_key")
    user_obj = None
    if user_details:
        user_obj = User_Reg.objects.get(u_phone=user_details)
    context = {"categories":categories,  "user":user_obj}
    return render(request, 'dcs_app/html/workers.html', context)
