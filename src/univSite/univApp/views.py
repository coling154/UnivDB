from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection

# Create your views here
def index(request):
    return render(request, 'index.html')
def admin(request):
    """
    This view is used to display admin.html landing page
    """
    return render(request, "admin.html")

def professor(request):
    """
    This view is used to display professor.html landing page
    """
    return render(request, "professor.html")

def student(request):
    """
    This view is used to display student.html landing page
    """
    return render(request, "student.html")

def F1(request):
    """
    This view is used to display F1.html template
    """
    return render(request,"queries/F1.html")
@require_http_methods(["POST"])
@csrf_exempt
def list_instructors(request):
    """
    F1 requirement
    This view is used to list all instructors in the database
    including their id, name, department, and salary
    the list can be ordered by name, department and salary in
    ascending or descending order

    :param request: Http request object
    :tye request: HttpRequest
    """
    order_by = request.POST.get('order', 'name')  # Default sort by name
    asc_desc = request.POST.get('asc_desc', 'asc')  # Default ascending
    query = f"SELECT id, name, dept_name, salary FROM instructor ORDER BY %s %s"
    cursor = connection.cursor()
    # Execute the query
    cursor.execute(query, (order_by, asc_desc,))
    rows = cursor.fetchall()

    # Convert query results to dictionary to render template
    instructors = [
        {"id": row[0], "name": row[1], "dept_name": row[2], "salary": row[3]}
        for row in rows
    ]

    return render(request, 'queries/F1Table.html', {'rows': instructors})

def F2(request):
    """
    This view is used to display F2.html template
    """
    return render(request,"queries/F2.html")


@require_http_methods(["POST"])
@csrf_exempt
def dept_stats(request):
    """
    F2 requirement
    This view is used to list the minimum,
    maximum, and average salary of a given department
    or defaults to all departments

    :param request: Http request object
    :tye request: HttpRequest
    """

    dept = request.POST.get('department')
    cursor = connection.cursor()

    # user inputs nothing
    if not dept:
        # select all departments
        query = f"SELECT dept_name, MIN(salary) AS min_salary, MAX(salary) AS max_salary, AVG(salary) AS average_salary FROM instructor GROUP BY dept_name"
        cursor.execute(query)
    else:
        # select the requested department
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
    """
    This view is used to display F3.html template
    """
    return render(request,"queries/F3.html")


@require_http_methods(["POST"])
@csrf_exempt
def prof_stats(request):
    """
    F3 requirement

    Takes input
    Professor name, year, and semester

    Reports
    how many sections professor teaches, how many students professor has,
    amount of funding secured, and the amount of papers the professor has published

    :param request: Http request object
    :tye request: HttpRequest
    """
    userIn = (request.POST.get("prof_name"), request.POST.get("year"), request.POST.get("semester"),)
    cursor = connection.cursor()
    # sections taught and how many students
    query1 = (f"SELECT COUNT(DISTINCT CONCAT(teaches.course_id, '-', teaches.sec_id)) AS Sections_taught,"
              f" COUNT(DISTINCT takes.student_id) AS Students_taught "
              f"FROM instructor i "
              f"INNER JOIN teaches ON i.id = teaches.teacher_id "
              f"INNER JOIN section ON teaches.course_id = section.course_id AND teaches.sec_id = section.sec_id AND teaches.semester = section.semester AND teaches.year = section.year "
              f"INNER JOIN takes ON section.course_id = takes.course_id AND section.semester = takes.semester AND section.year = takes.year "
              f"WHERE i.name = %s AND section.year = %s AND section.semester = %s GROUP BY i.id")
    
    query2 = (f"SELECT SUM(DISTINCT funds) AS amount_of_funding, COUNT(DISTINCT title) AS publications "
              f"FROM publication "
              f"INNER JOIN instructor on publication.instructorID = instructor.id "
              f"WHERE name = %s AND YEAR = %s AND semester = %s")
    # Execute the query1
    cursor.execute(query1, userIn)
    # save results of query1
    result1 = cursor.fetchall()
    # Execute the query2
    cursor.execute(query2, userIn)
    # save results of query2
    result2 = cursor.fetchall()
    # close cursor
    cursor.close()
    # if results are empty
    if not result1 and not result2:
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
    """
    This view is used to display F4.html template
    """
    return render(request,"queries/F4.html")

def F5(request):
    """
    This view is used to display F5.html template
    """
    return render(request,"queries/F5.html")

def F6(request):
    """
    This view is used to display F6.html template
    """
    return render(request,"queries/F6.html")
