from django import forms
from django import forms
from django.contrib.auth.forms import UserCreationForm
from healthcare.models import CustomUser, Doctor

class DoctorRegisterForm(UserCreationForm):
    """
    Form captures user fields + doctor-only fields.
    """

    # Extra doctor fields
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    degree = forms.CharField(max_length=50)
    speciality = forms.ModelChoiceField(queryset=None)
    fees = forms.IntegerField()
    image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "address",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load specialities dynamically
        from healthcare.models import Speciality
        self.fields["speciality"].queryset = Speciality.objects.all()

        # Add CSS classes
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


# class DoctorLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)

# from django import forms

# class UserLoginForm(forms.Form):
#     username = forms.CharField()
#     password = forms.CharField(widget=forms.PasswordInput)
