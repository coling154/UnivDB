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

def F1(request):
    return render(request,"mysite/F1.html")
def F2(request):
    return render(request,"mysite/F2.html")
def F3(request):
    return render(request,"mysite/F3.html")
