# healthcare/views/doctor/chat.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from healthcare.models import Appointment, ChatRoom, ChatMessage, Doctor

@login_required
def doctor_chat_list(request):
    if request.user.role != 'doctor':
        return redirect('home')
    doctor = request.user.doctor_profile

    # Get all active chat rooms
    chat_rooms = ChatRoom.objects.filter(doctor=doctor, is_active=True).select_related('patient', 'appointment')

    return render(request, 'doctor/chat_list.html', {
        'chat_rooms': chat_rooms
    })

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)

    if request.user == room.patient or (request.user.role == 'doctor' and Doctor.objects.get(user=request.user.id) == room.doctor):
        messages = room.messages.all()
        return render(request, 'chat/room.html', {
            'room': room,
            'messages': messages,
            'other_person': room.doctor.user if request.user == room.patient else room.patient
        })
    return redirect('home')

@login_required
def send_message(request):
    if request.method == 'POST':
        room_id = request.POST['room_id']
        message = request.POST['message'].strip()
        if message:
            room = get_object_or_404(ChatRoom, id=room_id)
            ChatMessage.objects.create(
                chat_room=room,
                sender=request.user,
                message=message
            )
    return JsonResponse({'status': 'sent'})