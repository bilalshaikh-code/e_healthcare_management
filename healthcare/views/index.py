from django.shortcuts import render, redirect

def home(request):
    return render(request,'pages/home.html')

def about(request):
    return render(request,'pages/about.html')

def feedback(request):
    return render(request,'pages/feedback.html')

def service(request):
    return render(request,'pages/services.html')

def contact(request):
    return render(request,'pages/contact.html')