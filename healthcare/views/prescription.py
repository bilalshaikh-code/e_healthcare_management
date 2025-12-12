import os
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
# from weasyprint import HTML
from django.conf import settings
from django.contrib.auth.decorators import login_required
from healthcare.models import Prescription

@login_required
def my_prescriptions(request):
    if request.user.role != 'patient':
        return redirect('home')

    prescriptions = Prescription.objects.filter(
        appointment__patientid=request.user
    ).select_related(
        'appointment__doctorid__user', 'appointment__slotid'
    ).order_by('-date_issued')

    return render(request, 'patient/my_prescriptions.html', {
        'prescriptions': prescriptions
    })

@login_required
def prescription_detail(request, pk):
    prescription = None
    try:
        prescription = get_object_or_404(Prescription, id=pk, appointment__patientid=request.user)
    except:
        ...
    return render(request, 'patient/prescription_detail.html', {'prescription': prescription})

@login_required
def download_prescription_pdf(request, pk):
    # if os.name == 'nt':  # Windows fix
    #     os.add_dll_directory(r'C:\Program Files\GTK3-Runtime Win64\bin')

    # prescription = get_object_or_404(Prescription, id=pk, appointment__patientid=request.user)
    # html_string = render_to_string('patient/prescription_pdf.html', {'prescription': prescription, 'user': request.user})
    # html = HTML(string=html_string, base_url=request.build_absolute_uri())
    # pdf = html.write_pdf()

    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="prescription_{prescription.id}.pdf"'
    # return response
    ...