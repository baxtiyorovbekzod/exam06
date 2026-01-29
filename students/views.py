from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Student
from .forms import StudentForm

class StudentListView(View):
    def get(self, request):
        students = Student.objects.all()
        search = request.GET.get('search')
        if search:
            students = students.filter(
                Q(full_name__icontains=search) |
                Q(email__icontains=search)
            )

        min_age = request.GET.get('min_age')
        if min_age and min_age.isdigit():
            students = students.filter(age__gte=int(min_age))

        return render(request, 'students/student_list.html', {
            'students': students,
            'search': search,
            'min_age': min_age
        })


class StudentCreateView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'students/student_form.html', {'form': form, 'action': 'Yaratish'})

    def post(self, request):
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student muvaffaqiyatli yaratildi!')
            return redirect('student_list')
        return render(request, 'students/student_form.html', {'form': form, 'action': 'Yaratish'})


class StudentDetailView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        enrollments = student.enrollment_set.select_related('course')
        return render(request, 'students/student_detail.html', {
            'student': student,
            'enrollments': enrollments
        })


class StudentEditView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)
        return render(request, 'students/student_form.html', {'form': form, 'action': 'Tahrirlash'})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student muvaffaqiyatli yangilandi!')
            return redirect('student_detail', pk=pk)
        return render(request, 'students/student_form.html', {'form': form, 'action': 'Tahrirlash'})


class StudentDeleteView(View):
    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        messages.success(request, 'Student muvaffaqiyatli o‘chirildi!')
        return redirect('student_list')