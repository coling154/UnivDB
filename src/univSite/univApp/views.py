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
    return render(request,"queries/F1.html")
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

    return render(request, 'queries/F1Table.html', {'rows': instructors})

def F2(request):
    return render(request,"queries/F2.html")


@require_http_methods(["POST"])
@csrf_exempt
def dept_stats(request):
    dept = request.POST.get('department')
    cursor = connection.cursor()

    if not dept:
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
    return render(request, 'queries/F2Table.html', {'rows': salarys})
def F3(request):
    return render(request,"queries/F3.html")
@require_http_methods(["POST"])
@csrf_exempt
def prof_stats(request):
    userIn = (request.POST.get("prof_name"), request.POST.get("year"), request.POST.get("semester"),)
    cursor = connection.cursor()
    query1 = f"SELECT COUNT(DISTINCT CONCAT(teaches.course_id, '-', teaches.sec_id)) AS Sections_taught, COUNT(DISTINCT takes.student_id) AS Students_taught FROM instructor i INNER JOIN teaches ON i.id = teaches.teacher_id INNER JOIN section ON teaches.course_id = section.course_id AND teaches.sec_id = section.sec_id AND teaches.semester = section.semester AND teaches.year = section.year INNER JOIN takes ON section.course_id = takes.course_id AND section.semester = takes.semester AND section.year = takes.year WHERE i.name = %s AND section.year = %s AND section.semester = %s GROUP BY i.id"
    query2 = f"SELECT SUM(DISTINCT funds) AS amount_of_funding, count(DISTINCT title) as publications from publication INNER JOIN instructor on publication.instructorID = instructor.id WHERE name = %s AND YEAR = %s AND semester = %s"
    cursor.execute(query1, userIn)
    result1 = cursor.fetchall()
    cursor.execute(query2, userIn)
    result2 = cursor.fetchall()
    if not result1 or not result2:
        stats = {}  # Handle the case where no data is returned
    else:
        stats =[{
            "Sections_taught": result1[0][0] if result1 else 0,
            "Students_taught": result1[0][1] if result1 else 0,
            "amount_of_funding": result2[0][0] if result2 else 0,
            "publications": result2[0][1] if result2 else 0}
            for row in range(1)]
    return render(request, "queries/F3Table.html", {'rows': stats})

def F4(request):
    return render(request,"queries/F4.html")

def F5(request):
    return render(request,"queries/F5.html")

def F6(request):
    return render(request,"queries/F6.html")
