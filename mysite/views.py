from django.http import HttpResponse
import mysql.connector

from django.template import loader
from .models import Student
from .models import Instructor


def index(request):

  template = loader.get_template('mysite/form.html')
  context = { }

  return HttpResponse(template.render(context, request))

def students(request):
   data = Student.objects.filter(student_id__lt='00000010')
   str = ""
   for o in data:
      str = str+o.__repr__()+'<br>'
   return HttpResponse(str)

'''
def instructors(request):
  amount = request.POST.get('amount', 0) # if amount is set, return it; otherwise returns 0
  print(amount)

  #data = Instructor.objects.filter(salary__gt=amount)
  data = []
  i1 = {'id':1, 'name':'alex', 'salary':10000, 'dept_name':{'dept_name':'CS'}}
  i2 = {'id':2, 'name':'white', 'salary':10000, 'dept_name':{'dept_name':'MA'}}
  i3 = {'id':3, 'name':'yao', 'salary':10000, 'dept_name':{'dept_name':'MA'}}
  data.append(i1)
  data.append(i2)
  data.append(i3)
  print(data)
  template = loader.get_template('mysite/table.html')
  context = {
        'rows': data,
    }

  return HttpResponse(template.render(context, request))
'''

#Converts query results to a list of dictionary objects
def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


from django.db import connection
def instructors(request):
  amount=request.POST.get('amount', 0)

  cursor = connection.cursor()
  query = "SELECT * FROM instructor WHERE salary >= %s"
  try:
    cursor.execute(query, (amount,))
    data = dictfetchall(cursor)
  finally:
    cursor.close()

  print(data)
  template = loader.get_template('mysite/table.html')
  context = {
        'rows': data,
    }

  return HttpResponse(template.render(context, request))

def publication(request):
   cursor = connection.cursor()
   try:
     cursor.execute("select teacher_id, year, month, title, venue from publication")
     data = dictfetchall(cursor)
     print(data)
   finally:
     cursor.close()

   return HttpResponse(data.__str__())

def admin(request):

    template = loader.get_template('mysite/F2.html')
    context = {}

    cursor = connection.cursor()
    try:
        cursor.execute("select id, username, last_login, email, is_superuser from auth_user");
        data = dictfetchall(cursor)

        print(data)
    finally:
        cursor.close()

    return HttpResponse(template.render(context, request))
def department(request):

    dept = request.POST.get('dept', 0)
    query = "SELECT dept_name, MAX(salary) FROM instructor GROUP BY dept_name HAVING dept_name = %s"
    cursor = connection.cursor()
    try:
        cursor.execute(query, (dept, ))
        data = dictfetchall(cursor)
        print(data)
    finally:
        cursor.close()
    return HttpResponse(data.__str__())

