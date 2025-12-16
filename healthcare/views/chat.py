# healthcare/views/patient/chat.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from healthcare.models import ChatRoom, Appointment

@login_required(login_url="login")
def patient_chat_list(request):
    if request.user.role != 'patient':
        return redirect('home')

    # Get all chat rooms where user is patient
    chat_rooms = ChatRoom.objects.filter(
        patient=request.user,
        is_active=True
    ).select_related('doctor__user', 'appointment')

    return render(request, 'patient/chat_list.html', {
        'chat_rooms': chat_rooms
    })