from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Enrollment
from .forms import EnrollmentForm

class EnrollmentListView(View):
    def get(self, request):
        enrollments = Enrollment.objects.select_related('student', 'course')
        return render(request, 'enrollments/enrollment_list.html', {
            'enrollments': enrollments
        })


class EnrollmentCreateView(View):
    def get(self, request):
        form = EnrollmentForm()
        return render(request, 'enrollments/enrollment_form.html', {'form': form})

    def post(self, request):
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Student kursga muvaffaqiyatli yozildi!')
                return redirect('enrollment_list')
            except IntegrityError:
                messages.error(request, 'Bu student allaqachon ushbu kursga yozilgan!')
        return render(request, 'enrollments/enrollment_form.html', {'form': form})


class EnrollmentDeleteView(View):
    def post(self, request, pk):
        enrollment = get_object_or_404(Enrollment, pk=pk)
        enrollment.delete()
        messages.success(request, 'Ro‘yxatdan o‘chirish muvaffaqiyatli amalga oshirildi!')
        return redirect('enrollment_list')