from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Student
from django.contrib.auth.decorators import login_required


# Asosiy sahifa
def home(request):
    return render(request, 'home.html')

# Sign up (ro‘yxatdan o‘tish)
def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('sign_up')

        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, "Account created successfully! Please sign in.")
        return redirect('sign_in')

    return render(request, 'sign_up.html')


# Sign in (tizimga kirish)
def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('student_list')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('sign_in')

    return render(request, 'sign_in.html')


# Logout (tizimdan chiqish)
def logout_view(request):
    logout(request)
    return redirect('sign_in')



@login_required(login_url='sign_in')
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(group__icontains=query) | Student.objects.filter(jdu_id__icontains=query)
    else:
        students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


@login_required(login_url='sign_in')

# def student_add(request):
#     if request.method == 'POST':
#         full_name = request.POST['full_name']
#         jdu_id = request.POST['jdu_id']
#         group = request.POST['group']
#         age = request.POST['age']
#         Student.objects.create(full_name=full_name, jdu_id=jdu_id, group=group, age=age)
#         messages.success(request, "Student added successfully!")
#         return redirect('student_list')
#     return render(request, 'student_add.html')


@login_required(login_url='sign_in')
def student_edit(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        student.full_name = request.POST['full_name']
        student.jdu_id = request.POST['jdu_id']
        student.group = request.POST['group']
        student.age = request.POST['age']
        student.save()
        messages.success(request, "Student updated successfully!")
        return redirect('student_list')
    return render(request, 'student_edit.html', {'student': student})


@login_required(login_url='sign_in')
def student_delete(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect('student_list')




def student_add(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        jdu_id = request.POST['jdu_id']
        group = request.POST['group']
        age = request.POST['age']

        # 🔍 Avval jdu_id mavjudligini tekshiramiz
        if Student.objects.filter(jdu_id=jdu_id).exists():
            messages.error(request, f"Bu JDU ID ({jdu_id}) allaqachon mavjud!")
            return redirect('student_add')

        # ✅ Aks holda yangi student yaratamiz
        Student.objects.create(
            full_name=full_name,
            jdu_id=jdu_id,
            group=group,
            age=age
        )
        messages.success(request, "Student added successfully!")
        return redirect('student_list')

    return render(request, 'student_add.html')