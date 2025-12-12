# forms.py
from django import forms
from .models import CustomUser, Feedback

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image', 'email', 'first_name', 'last_name', 'address','mobile_number']  # Example fields, adjust as needed

class FeedbackForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Your Full Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'you@example.com'
        })
    )
    rating = forms.ChoiceField(
        choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)],
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Share your experience...'
        }),
        min_length=10,
        max_length=1000
    )

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'rating', 'message']

    def clean_email(self):
        email = self.cleaned_data['email']
        if "spam" in email.lower() or "test" in email.lower():
            raise forms.ValidationError("Invalid email address.")
        return email