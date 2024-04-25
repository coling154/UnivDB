from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db import connection
import hashlib
import re

error = 0
group = 0

# Create your views here
def index(request):
    if error:
        return render(request, 'index.html', {'error': error})
    else:
        return render(request, 'index.html')

@csrf_exempt
def admin(request):
    """
    This view is used to display admin.html landing page
    """
    return render(request, "admin.html", {"group": group})

def professor(request):
    """
    This view is used to display professor.html landing page
    """
    return render(request, "professor.html", {"group": group})

def student(request):
    """
    This view is used to display student.html landing page
    """
    return render(request, "student.html", {"group": group})

def F1(request):
    """
    This view is used to display F1.html template
    """
    return render(request,"queries/F1.html", {"group": group})
@require_http_methods(["GET", "POST"])
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
    if request.method == 'POST':
        order_by = request.POST.get('order', 'name')
        asc_desc = request.POST.get('asc_desc', 'ASC').upper()
    else:  # Default for GET requests
        order_by = request.GET.get('order', 'name')
        asc_desc = request.GET.get('asc_desc', 'ASC').upper()
    query = f"SELECT id, name, dept_name, salary FROM instructor ORDER BY {order_by} {asc_desc}"
    cursor = connection.cursor()

    # validate asc_desc
    if asc_desc not in ['ASC', 'DESC']:
        asc_desc = 'ASC'

    # validate order_by
    if order_by not in ['name', 'dept_name', 'salary']:
        order_by = 'name'

    # Execute the query
    cursor.execute(query)
    rows = cursor.fetchall()

    # Paginate the results 10 per page
    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert query results to dictionary to render template
    instructors = [
        {"id": row[0], "name": row[1], "dept_name": row[2], "salary": row[3]}
        for row in page_obj
    ]

    return render(request, 'queries/F1Table.html', {'page_obj': page_obj, 'instructors': instructors, 'group': group})

def F2(request):
    """
    This view is used to display F2.html template
    """
    return render(request,"queries/F2.html", {"group": group})


@require_http_methods(["GET", "POST"])
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
    if request.method == 'POST':
        dept = request.POST.get('department', None)
    else: # GET
        dept = request.GET.get('department', None)
    cursor = connection.cursor()

    # user inputs nothing
    if not dept:
        # select all departments
        query = f"SELECT dept_name, MIN(salary) AS min_salary, MAX(salary) AS max_salary, AVG(salary) AS average_salary FROM instructor GROUP BY dept_name"
        cursor.execute(query)
    else:
        # select the requested department
        query = (f"SELECT dept_name, MIN(salary) AS min_salary, MAX(salary) AS max_salary, AVG(salary) AS average_salary "
                 f"FROM instructor GROUP BY dept_name HAVING dept_name = %s")
        cursor.execute(query, (dept,))
    rows = cursor.fetchall()

    # Paginate the results 10 per page
    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Convert query results to dictionary for easier template rendering
    salarys = [
        {"dept_name": row[0], "min": row[1], "max": row[2], "average": row[3]}
        for row in page_obj
    ]
    return render(request, 'queries/F2Table.html', {'page_obj': page_obj, 'rows': salarys, 'group': group})


def F3(request):
    """
    This view is used to display F3.html template
    """
    return render(request,"queries/F3.html", {"group": group})


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
    dateStart, dateEnd = None, None # initializing in function scope
    # spring sem
    if int(sem) == 1:
        dateStart = f"%s-01-01" % year
        dateEnd = f"%s-05-31" % year
    # fall sem
    if int(sem) == 2:
        dateStart = f"%s-06-01" % year
        dateEnd = f"%s-12-31" % year
    cursor = connection.cursor()

    # data tuple for 3.1 and 3.2
    tuple1 = (name, year, sem,)

    # 3.1 # sections query
    query = (f"SELECT COUNT(sec_id) FROM teaches t "
              f"INNER JOIN instructor i ON t.teacher_id = i.id "
              f"WHERE i.name = %s AND t.year = %s AND t.semester = %s")
    # Execute the query
    cursor.execute(query, tuple1)
    # save results of query
    result1 = cursor.fetchall()

    # 3.2 # students taught
    query = (f"SELECT COUNT(DISTINCT takes.student_id) FROM takes "
              f"INNER JOIN teaches ON takes.course_id = teaches.course_id AND takes.sec_id = teaches.sec_id "
              f"INNER JOIN instructor ON teaches.teacher_id = instructor.id "
              f"WHERE instructor.name = %s AND takes.year = %s AND takes.semester = %s")
    # Execute the query
    cursor.execute(query, tuple1)
    # save results of query
    result2 = cursor.fetchall()

    # data tuple for 3.3, 3.4
    tuple2 = (name, dateStart, dateEnd,)

    # 3.3 funding query
    query = (f"SELECT SUM(f.funding_amount) FROM funding f "
              f"NATURAL JOIN project p "
              f"INNER JOIN instructor i ON p.PI = i.id "
              f"WHERE i.name = %s AND p.end_date BETWEEN %s AND %s")
    # Execute the query
    cursor.execute(query, tuple2)
    # save results of query
    result3 = cursor.fetchall()

    # 3.4 # publications query
    query = (f"SELECT COUNT(ip.publication_id) FROM publication p "
              f"NATURAL JOIN instructor_publishes ip "
              f"INNER JOIN instructor i ON ip.instructor_id = i.id "
              f"WHERE i.name = %s AND p.publish_date BETWEEN %s AND %s")
    # Execute the query
    cursor.execute(query, tuple2)
    # save results of query
    result4 = cursor.fetchall()

    # close cursor
    cursor.close()
    # if results are empty
    if not result1:
        result1 = {}
    if not result2:
        result2 = {}
    if not result3:
        result3 = {}
    if not result4:
        result4 = {}
    stats =[{
        "Sections_taught": result1[0][0] if result1 else 0,
        "Students_taught": result2[0][0] if result2 else 0,
        "amount_of_funding": result3[0][0] if result3 else 0,
        "publications": result4[0][0] if result4 else 0}
        for row in range(1)]
    return render(request, "queries/F3Table.html", {'rows': stats, "group": group})

def F4(request):
    """
    This view is used to display F4.html template
    """
    return render(request,"queries/F4.html", {"group": group})


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
    sem = request.POST.get("semester")
    year = request.POST.get("year")
    id = request.POST.get("id")
    cursor = connection.cursor()
    query = (f"SELECT DISTINCT s.course_id, ts.sec_id,(SELECT COUNT(DISTINCT t.student_id) "
             f"FROM takes t "
             f"WHERE t.course_id = s.course_id AND t.sec_id = s.sec_id AND t.semester = s.semester AND t.year = s.year) "
             f"AS student_count FROM section s "
             f"NATURAL JOIN teaches ts "
             f"WHERE s.semester = {sem} AND s.year = {year} AND ts.teacher_id = {id}")
    # Execute the query
    cursor.execute(query)
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
    return render(request, "queries/F4Table.html", {'rows': stats, 'group': group})

def F5(request):
    """
    This view is used to display F5.html template
    """
    return render(request,"queries/F5.html", {"group": group})


@require_http_methods(["POST"])
@csrf_exempt
def list_students(request):
    """
    FR5 Requirement

    Takes instructor id, course, section, year, and semester
    Returns id, name, and grade of every student that took that
    course and section with that instructor that semester and year
    """
    id = request.POST.get("id")
    course = request.POST.get("course")
    section = request.POST.get("section")
    year = request.POST.get("year")
    sem = request.POST.get("semester")
    tuple1 = (id, course, section, year, sem)
    cursor = connection.cursor()
    query = (f"SELECT DISTINCT s.name, s.student_id, ta.grade "
             f"FROM student s "
             f"NATURAL JOIN takes ta "
             f"NATURAL JOIN section sec "
             f"NATURAL JOIN teaches t"
             f" WHERE t.teacher_id = %s AND t.course_id = %s AND t.sec_id = %s AND t.year = %s AND t.semester = %s")
    # execute the query
    cursor.execute(query, tuple1)
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
    return render(request, "queries/F5Table.html", {'rows': stats, 'group': group})

def F6(request):
    """
    This view is used to display F6.html template
    """
    return render(request,"queries/F6.html", {'group': group})


@require_http_methods(["POST"])
@csrf_exempt
def dep_courses(request):
    """
    F6 Requirement
    Takes Department name, year, and semester
    and returns a list of all courses and sections that semester
    """
    dept_name = request.POST.get("dept_name")
    year = request.POST.get("year")
    sem = request.POST.get("semester")
    tuple1 = (dept_name, year, sem,)
    cursor = connection.cursor()

    query = (f"SELECT c.course_id, c.title, s.sec_id "
             f"FROM section s "
             f"NATURAL JOIN course c "
             f"NATURAL JOIN department d "
             f"WHERE d.dept_name = %s AND s.year = %s AND s.semester = %s")
    # execute the query
    cursor.execute(query, tuple1)
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
    return render(request, "queries/F6Table.html", {'rows': stats, 'group': group})

@require_http_methods(["POST"])
@csrf_exempt
def login(request):
    global error
    global group

    user, pwd = request.POST.get("user"), request.POST.get("pass")

    pwd = hashlib.sha256(pwd.encode("utf-8")).hexdigest()

    cursor = connection.cursor()

    query = (f'SELECT perm_group FROM user '
             f'WHERE username="{user}" AND pass="{pwd}" LIMIT 1')

    cursor.execute(query)

    row = cursor.fetchone()

    if row:
        pGroup = row[0]
        error = 0
        if pGroup == 1:
            group = 1 
            return redirect('admin')

        elif pGroup == 2:
            group = 2
            return redirect('professor')

        elif pGroup == 3:
            group = 3
            return redirect('student')
    else: 
        error = 1
        return redirect('index')