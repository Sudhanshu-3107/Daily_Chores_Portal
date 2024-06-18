from django.db import models
from django.utils import timezone


# Create your models here.

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=13)
    question = models.TextField()
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default = timezone.now)



class Comp_Reg(models.Model):
    usertype = models.CharField(max_length=20, default='company')
    c_id = models.CharField(max_length=100, primary_key=True, default=1)
    c_pic = models.FileField(max_length=100, upload_to='Dailychores_Security/Companies/', default="")
    c_pass = models.CharField(max_length=32)
    c_name = models.CharField(max_length=50)
    c_ceo = models.CharField(max_length=50)
    c_phone = models.CharField(max_length=13)
    c_email = models.EmailField(max_length=30)
    c_city = models.CharField(max_length=20)
    c_regno = models.CharField(max_length=30)
    status = models.BooleanField(default=False)
    c_addr = models.TextField()
    c_about = models.TextField()
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.c_id



class User_Reg(models.Model):
    usertype = models.CharField(max_length=20, default='user')
    u_name = models.CharField(max_length=50)
    u_pic = models.FileField(max_length=100, upload_to='Dailychores_Security/Users/', default="")
    u_email = models.EmailField(max_length=50)
    u_phone = models.CharField(max_length=13, primary_key=True)
    u_pass = models.CharField(max_length=32)
    u_city = models.CharField(max_length=50)
    u_addr = models.TextField()
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)



class Employee_Category(models.Model):
    comp_reg = models.ForeignKey(Comp_Reg, on_delete=models.DO_NOTHING)
    emp_category = models.CharField(max_length=50)
    emp_category_pic = models.FileField(max_length=100, upload_to='Dailychores_Security/Employee_categories/', default="")
    category_charge = models.IntegerField(default=50000)
    emp_description = models.CharField(max_length=100)
    def __str__(self):
        return self.emp_category



class Employee_Reg(models.Model):
    emp_reg = models.ForeignKey(Employee_Category, on_delete=models.DO_NOTHING)
    emp_id = models.CharField(max_length=50)
    emp_pic = models.FileField(max_length=100, upload_to='Dailychores_Security/Employees/', default="")
    emp_name = models.CharField(max_length=50)
    emp_phone = models.CharField(max_length=13,primary_key=True)
    emp_status = models.CharField(max_length=13, default="Available")
    emp_city = models.CharField(max_length=50)
    emp_addr = models.TextField()
    time = models.TimeField(default=timezone.now)
    date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.emp_phone



class Hiring(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    job_category = models.ForeignKey(Employee_Category, on_delete=models.DO_NOTHING)
    job_description = models.TextField()
    job_requirement = models.CharField(max_length=50)
    job_location = models.CharField(max_length=50)
    job_salary = models.CharField(max_length=50)
    job_age_limit = models.CharField(max_length=5)
    job_mail = models.CharField(max_length=50)
    job_lastdate_toapply = models.DateField(default=timezone.now)
    job_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    job_seats = models.CharField(max_length=5)
    job_post_link = models.CharField(max_length=50)
    company = models.ForeignKey(Comp_Reg, on_delete=models.DO_NOTHING)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']



class JobApplication(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    hiring = models.ForeignKey(Hiring, on_delete=models.DO_NOTHING)
    js_pic = models.FileField(max_length=100, upload_to='Dailychores_Security/Job_seekers/', default="")
    js_name = models.CharField(max_length=50)
    js_age = models.CharField(max_length=10)
    js_city = models.CharField(max_length=30, default='Lucknow')
    js_gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    js_address = models.TextField()
    js_phone = models.CharField(max_length=15)
    js_details = models.CharField(max_length=50)
    visibility = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']



class Employee_Booking(models.Model):
    STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
    )
    user = models.ForeignKey(User_Reg, on_delete=models.DO_NOTHING)
    employee = models.ForeignKey(Employee_Reg, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")
    duration = models.CharField(max_length=10)
    payment = models.FileField(max_length=100, upload_to='Dailychores_Security/Payment_Screenshots/')
    visibility = models.BooleanField(default=True)
    response = models.TextField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def save(self, *args, **kwargs):
        if self.status == 'Confirmed':
            self.employee.emp_status = 'Not Available'
            self.employee.save()
        elif self.status == 'Pending':
            self.employee.emp_status = 'Available'
            self.employee.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.employee.emp_status = 'Available'
        self.employee.save()
        super().delete(*args, **kwargs)



class Complaint(models.Model):
    booking = models.ForeignKey(Employee_Booking, on_delete=models.DO_NOTHING)
    complaint = models.TextField()
    resolve = models.TextField(null=True)
    complaint_date = models.DateTimeField(default=timezone.now)
    resolve_date = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']



class Feedback(models.Model):
    feedback = models.ForeignKey(Employee_Booking, on_delete=models.DO_NOTHING)
    remark = models.TextField()
    rating = models.CharField(max_length=10, default="★★★★★")
    created = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']