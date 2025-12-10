from django.shortcuts import render, redirect
from ..models import CustomUser
from django.contrib.auth.decorators import login_required
from ..forms import UserProfileForm

@login_required
def view(request):
    if request.user.is_authenticated:
        puser= CustomUser.objects.get(id=request.user.id)
        return render(request,"pages/profile/view.html",{'puser':puser})
    
@login_required
def update(request):
    # current_user=CustomUser.objects.get(id=request.id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')    
    else:
        form = UserProfileForm(instance=request.user)
    return render(request,'pages/profile/update.html',{'form':form})