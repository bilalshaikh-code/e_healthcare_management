import os
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from healthcare.models import Prescription
from io import BytesIO

@login_required(login_url="login")
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

@login_required(login_url="login")
def prescription_detail(request, pk):
    prescription = None
    try:
        prescription = get_object_or_404(Prescription, id=pk, appointment__patientid=request.user)
    except:
        ...
    return render(request, 'patient/prescription_detail.html', {'prescription': prescription})

@login_required(login_url="login")
def download_prescription_pdf(request, pk):
    prescription = get_object_or_404(
        Prescription, 
        id=pk, 
        appointment__patientid=request.user
    )

    # Render HTML template to string
    html = render_to_string('patient/prescription_pdf.html', {
        'prescription': prescription,
        'patient': request.user,
    })

    # Create PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"Prescription_{prescription.id}_{prescription.date_issued.strftime('%d-%m-%Y')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        return HttpResponse("Error generating PDF", status=500)