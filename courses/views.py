from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Course
from .forms import CourseForm


class CourseListView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'courses/course_list.html', {
            'courses': courses
        })


class CourseCreateView(View):
    def get(self, request):
        form = CourseForm()
        return render(request, 'courses/course_form.html', {
            'form': form,
            'action': 'Yaratish'
        })

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kurs muvaffaqiyatli yaratildi!')
            return redirect('course_list')

        return render(request, 'courses/course_form.html', {
            'form': form,
            'action': 'Yaratish'
        })


class CourseDetailView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        enrollments = course.enrollment_set.select_related('student')
        return render(request, 'courses/course_detail.html', {
            'course': course,
            'enrollments': enrollments
        })


class CourseEditView(View):
    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(instance=course)
        return render(request, 'courses/course_form.html', {
            'form': form,
            'action': 'Tahrirlash'
        })

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Kurs muvaffaqiyatli yangilandi!')
            return redirect('course_detail', pk=pk)

        return render(request, 'courses/course_form.html', {
            'form': form,
            'action': 'Tahrirlash'
        })


class CourseDeleteView(View):
    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)

        if course.enrollment_set.exists():
            messages.error(request, 'Bu kursga studentlar yozilgan. O‘chirish mumkin emas.')
            return redirect('course_detail', pk=pk)

        course.delete()
        messages.success(request, 'Kurs o‘chirildi!')
        return redirect('course_list')