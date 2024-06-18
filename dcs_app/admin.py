from django.contrib import admin
from .models import Feedback, Contact,Comp_Reg, User_Reg, Employee_Reg, Employee_Category, Hiring, JobApplication, Employee_Booking, Complaint

admin.site.register(Feedback)
admin.site.register(Contact)
admin.site.register(Comp_Reg)
admin.site.register(User_Reg)
admin.site.register(Employee_Reg)
admin.site.register(Employee_Category)
admin.site.register(Employee_Booking)
admin.site.register(Hiring)
admin.site.register(JobApplication)
admin.site.register(Complaint)
