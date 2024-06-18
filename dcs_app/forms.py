from django import forms
from .models import Hiring, JobApplication, Employee_Category, Employee_Booking, Complaint, Feedback


class HiringForm(forms.ModelForm):
    class Meta:
        model = Hiring
        fields = '__all__'
        exclude = ['company', 'job_post_link']
        widgets = {
            'job_lastdate_toapply': forms.DateInput(attrs={'type': 'date'}),
            'job_category': forms.Select(attrs={'class': 'form-select'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control'}),
            'job_requirement': forms.TextInput(attrs={'class': 'form-control'}),
            'job_location': forms.TextInput(attrs={'class': 'form-control'}),
            'job_salary': forms.TextInput(attrs={'class': 'form-control'}),
            'job_age_limit': forms.TextInput(attrs={'class': 'form-control'}),
            'job_mail': forms.EmailInput(attrs={'class': 'form-control'}),
            'job_lastdate_toapply': forms.DateInput(attrs={'type': 'date','class': 'form-control'}),
            'job_gender': forms.Select(attrs={'class': 'form-select'}),
            'job_seats': forms.TextInput(attrs={'class': 'form-control'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, company_id, *args, **kwargs):
        super(HiringForm, self).__init__(*args, **kwargs)
        self.fields['job_category'].queryset = Employee_Category.objects.filter(comp_reg__c_id=company_id)



class JobForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = '__all__'
        exclude = ['hiring', 'visibility']
        widgets = {
            'js_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'js_name': forms.TextInput(attrs={'class': 'form-control'}),
            'js_age': forms.TextInput(attrs={'class': 'form-control'}),
            'js_city': forms.TextInput(attrs={'class': 'form-control'}),
            'js_gender': forms.Select(attrs={'class': 'form-select'}),
            'js_address': forms.Textarea(attrs={'class': 'form-control'}),
            'js_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'js_details': forms.TextInput(attrs={'class': 'form-control'}),
        }


class BookingForm(forms.ModelForm):
    user = forms.CharField(max_length=50, required=False)
    employee = forms.CharField(max_length=50, required=False)
    class Meta:
        model = Employee_Booking
        fields = ['payment','duration']
        widgets ={
            'payment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = [ 'complaint']
        widgets = {
         'complaint': forms.Textarea(attrs={'class': 'form-control'}),
        }


class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = [ 'remark', 'rating']
        widgets = {
         'remark': forms.Textarea(attrs={'class': 'form-control'}),
        }