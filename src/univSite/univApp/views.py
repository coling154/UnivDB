from django.shortcuts import render

# Create your views here
def index(request):
    return render(request, 'index.html')
def admin(request):
    print("ADMIN")
    return render(request, "admin.html")

def professor(request):
    print("professor")
    return render(request, "professor.html")

def student(request):
    return render(request, "student.html")

