from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection

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
@require_http_methods(["POST"])
@csrf_exempt
def list_instructors(request):
    order_by = request.POST.get('order', 'name')  # Default sort by name
    asc_desc = 'ASC' if request.POST.get('asc_desc', 'asc') == 'asc' else 'DESC'

    query = f"SELECT id, name, dept_name, salary FROM instructor ORDER BY {order_by} {asc_desc}"
    cursor = connection.cursor()
    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Convert query results to dictionary for easier template rendering
    instructors = [
        {"id": row[0], "name": row[1], "dept_name": row[2], "salary": row[3]}
        for row in rows
    ]

    return render(request, 'mysite/F1Table.html', {'rows': instructors})

def F2(request):
    return render(request,"mysite/F2.html")


@require_http_methods(["POST"])
@csrf_exempt
def dept_stats(request):
    dept = request.POST.get('department')
    cursor = connection.cursor()

    if(dept.lower() == 'all'):
        query = f"SELECT dept_name, MIN(salary) AS min_salary, MAX(salary) AS max_salary, AVG(salary) AS average_salary FROM instructor GROUP BY dept_name"
        cursor.execute(query)
    else:
        query = f"SELECT dept_name, MIN(salary) AS min_salary, MAX(salary) AS max_salary, AVG(salary) AS average_salary FROM instructor GROUP BY dept_name HAVING dept_name = %s"
        cursor.execute(query, (dept,))
    rows = cursor.fetchall()

    # Convert query results to dictionary for easier template rendering
    salarys = [
        {"dept_name": row[0], "min": row[1], "max": row[2], "average": row[3]}
        for row in rows
    ]
    return render(request, 'mysite/F2Table.html', {'rows': salarys})
def F3(request):
    return render(request,"mysite/F3.html")
