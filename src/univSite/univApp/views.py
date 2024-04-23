from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import connection
import hashlib
import re

# Create your views here
def index(request):
    return render(request, 'index.html')

@csrf_exempt
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
    :type request: HttpRequest
    """
    year = request.POST.get("year")
    sem = request.POST.get("semester")
    name = request.POST.get("prof_name")
    userIn = (name, year, sem, )
    dateStart, dateEnd = None, None
    # spring sem
    if int(sem) == 1:
        dateStart = year + '-01-01'
        dateEnd = year + '-05-31'
    # fall sem
    if int(sem) == 2:
        dateStart = year + '-06-01'
        dateEnd = year + '-12-31'
    cursor = connection.cursor()
    query1 = f"SELECT COUNT(sec_id) FROM teaches t INNER JOIN instructor i ON t.teacher_id = i.id WHERE i.name = %s AND t.year = %s AND t.semester = %s"
    query2 = f"SELECT COUNT(DISTINCT takes.student_id) FROM takes INNER JOIN teaches ON takes.course_id = teaches.course_id AND takes.sec_id = teaches.sec_id INNER JOIN instructor ON teaches.teacher_id = instructor.id WHERE instructor.name = %s AND takes.year = %s AND takes.semester = %s"

    in2 = (name, dateStart, dateEnd, )
    query3 = f"SELECT SUM(f.funding_amount) from funding f NATURAL JOIN research r INNER JOIN instructor i ON r.PI = i.id WHERE i.name = %s AND r.end_date BETWEEN %s AND %s"
    query4 = f"SELECT COUNT(ip.publication_id) FROM publication p NATURAL JOIN instructor_publishes ip INNER JOIN instructor i ON ip.instructor_id = i.id WHERE i.name = %s AND p.publish_date BETWEEN %s AND %s"
    # Execute the query1
    cursor.execute(query1, userIn)
    # save results of query1
    result1 = cursor.fetchall()
    # Execute the query2
    cursor.execute(query2, userIn)
    # save results of query2
    result2 = cursor.fetchall()
    # Execute the query3
    cursor.execute(query3, in2)
    # save results of query3
    result3 = cursor.fetchall()
    # Execute the query4
    cursor.execute(query4, in2)
    # save results of query4
    result4 = cursor.fetchall()
    # close cursor
    cursor.close()
    # if results are empty
    if not result1 and not result2:
        stats = {}  # Handle the case where no data is returned
    else:
        stats =[{
            "Sections_taught": result1[0][0] if result1 else 0,
            "Students_taught": result2[0][0] if result2 else 0,
            "amount_of_funding": result3[0][0] if result3 else 0,
            "publications": result4[0][0] if result4 else 0}
            for row in range(1)]
    return render(request, "queries/F3Table.html", {'rows': stats})

def F4(request):
    """
    This view is used to display F4.html template
    """
    return render(request,"queries/F4.html")


@require_http_methods(["POST"])
@csrf_exempt
def sections(request):
    """
    FR4 Requirement

    Given a professors name, semester, and year
    return list of course sections with number of students in each

    :param request: Http request object
    :type request: HttpRequest
    """
    # get data
    userIn = (request.POST.get("semester"), request.POST.get("year"), request.POST.get("id"),)

    cursor = connection.cursor()
    query = (f"SELECT DISTINCT s.course_id, ts.sec_id,(SELECT COUNT(DISTINCT t.student_id) "
             f"FROM takes t "
             f"WHERE t.course_id = s.course_id AND t.sec_id = s.sec_id AND t.semester = s.semester AND t.year = s.year) "
             f"AS student_count FROM section s "
             f"NATURAL JOIN teaches ts "
             f"WHERE s.semester = %s AND s.year = %s AND ts.teacher_id = %s")
    # Execute the query
    cursor.execute(query, userIn)
    # get results
    results = cursor.fetchall()
    cursor.close()
    if not results:
        stats = {}  # Handle the case where no data is returned
    else:
        stats =[{
            "course_id": row[0],
            "sec_id": row[1],
            "student_count": row[2]}
            for row in results]
    return render(request, "queries/F4Table.html", {'rows': stats})

def F5(request):
    """
    This view is used to display F5.html template
    """
    return render(request,"queries/F5.html")


@require_http_methods(["POST"])
@csrf_exempt
def list_students(request):
    """
    FR5 Requirement

    Takes instructor id, course, section, year, and semester
    Returns id, name, and grade of every student that took that
    course and section with that instructor that semester and year
    """
    userIn = (request.POST.get("id"), request.POST.get("course"),
              request.POST.get("section"), request.POST.get("year"), request.POST.get("semester"), )

    cursor = connection.cursor()
    query = (f"SELECT DISTINCT s.name, s.student_id, ta.grade "
             f"FROM student s "
             f"NATURAL JOIN takes ta "
             f"NATURAL JOIN section sec "
             f"NATURAL JOIN teaches t"
             f" WHERE t.teacher_id = %s AND t.course_id = %s AND t.sec_id = %s AND t.year = %s AND t.semester = %s")
    # execute the query
    cursor.execute(query, userIn)
    # get results
    results = cursor.fetchall()
    cursor.close()
    if not results:
        stats = {}  # Handle the case where no data is returned
    else:
        stats =[{
            "name": row[0],
            "student_id": row[1],
            "grade": row[2]}
            for row in results]
    return render(request, "queries/F5Table.html", {'rows': stats})

def F6(request):
    """
    This view is used to display F6.html template
    """
    return render(request,"queries/F6.html")


@require_http_methods(["POST"])
@csrf_exempt
def dep_courses(request):
    """
    F6 Requirement
    Takes Department name, year, and semester
    and returns a list of all courses and sections that semester
    """
    userIn = ( request.POST.get("dept_name"),request.POST.get("year"), request.POST.get("semester"),)

    cursor = connection.cursor()

    query = (f"SELECT c.course_id, c.title, s.sec_id "
             f"FROM section s "
             f"NATURAL JOIN course c "
             f"NATURAL JOIN department d "
             f"WHERE d.dept_name = %s AND s.year = %s AND s.semester = %s")
    # execute the query
    cursor.execute(query, userIn)
    # save results
    results = cursor.fetchall()
    cursor.close()
    if not results:
        stats = {}  # Handle the case where no data is returned
    else:
        stats = [{
            "course_id": row[0],
            "title": row[1],
            "sec_id": row[2]}
            for row in results]
    return render(request, "queries/F6Table.html", {'rows': stats})

@require_http_methods(["POST"])
@csrf_exempt
def login(request):
    user, pwd = request.POST.get("user"), request.POST.get("pass")

    pwd = hashlib.sha256(pwd.encode("utf-8")).hexdigest()

    cursor = connection.cursor()

    query = f'SELECT perm_group FROM user WHERE username="{user}" AND pass="{pwd}" LIMIT 1'

    cursor.execute(query)

    row = cursor.fetchone()

    if row:
        group = row[0]
        if group == 1:
            return redirect('admin')

        elif group == 2:
            return redirect('professor')
        elif group == 3:
            return redirect('student')
    else: 
        return redirect('index')