from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector
from django.db import connection

from django.template import loader
# Create your views here.

def index(request):
  return render(request, "index.html")


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def admin(request):
    print("ADMIN")
    return render(request, "admin.html")

def professor(request):
    print("professor")
    return render(request, "professor.html")

def student(request):
    return render(request, "student.html")

def F2(request):
    dept = request.POST.get('dept', 0)
    query = "SELECT dept_name,MIN(salary), MAX(salary), AVG(salary) FROM instructor GROUP BY dept_name HAVING dept_name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (dept,))
        data = dictfetchall(cursor)
        print(data)
    finally:
        cursor.close()
    return HttpResponse(data.__str__())


