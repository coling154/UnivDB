# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=64, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Course'

'''
class Grantaward(models.Model):
    agent = models.CharField(max_length=16)
    award_id = models.CharField(max_length=8)
    amount = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=64, blank=True, null=True)
    startyear = models.IntegerField(db_column='startYear', blank=True, null=True)  # Field name made lowercase.
    startmonth = models.IntegerField(db_column='startMonth', blank=True, null=True)  # Field name made lowercase.
    endyear = models.IntegerField(db_column='endYear', blank=True, null=True)  # Field name made lowercase.
    endmonth = models.IntegerField(db_column='endMonth', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'GrantAward'
        unique_together = (('agent', 'award_id'),)
'''

class Instructor(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    def __repr__(self):
       #return "Instructor: "+self.id+","+self.name+","+str(self.salary)
       return "Instructor: "+self.id+","+self.name+","+self.dept_name.dept_name+","+str(self.salary)

    class Meta:
        managed = False
        db_table = 'Instructor'

'''
class Investigator(models.Model):
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING)
    agent = models.ForeignKey(Grantaward, models.DO_NOTHING, db_column='agent', related_name="awards1")
    award = models.ForeignKey(Grantaward, models.DO_NOTHING, related_name="awards2")
    role = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Investigator'
        unique_together = (('teacher', 'agent', 'award'),)
'''

'''
class Prereq(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, related_name="courses")
    preq = models.ForeignKey(Course, models.DO_NOTHING, related_name="courses1")

    class Meta:
        managed = False
        db_table = 'Prereq'
        unique_together = (('course', 'preq'),)
'''

class Publication(models.Model):
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING)
    year = models.IntegerField()
    month = models.IntegerField()
    title = models.CharField(max_length=128)
    venue = models.CharField(max_length=64, blank=True, null=True)
    kind = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Publication'
        unique_together = (('teacher', 'year', 'month', 'title'),)

'''
class Section(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING)
    sec_id = models.CharField(max_length=4)
    semester = models.IntegerField()
    year = models.IntegerField()
    building = models.CharField(max_length=32, blank=True, null=True)
    room = models.CharField(max_length=8, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Section'
        unique_together = (('course', 'sec_id', 'semester', 'year'),)
'''

class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Student'

    def __repr__(self):
      return 'Student('+self.student_id+', '+self.name+', credits: '+str(self.total_credits)+')'

'''
class Takes(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, related_name="students")
    course = models.ForeignKey(Section, models.DO_NOTHING, related_name="sections")
    sec = models.ForeignKey(Section, models.DO_NOTHING, related_name="sections1")
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name="sections2")
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name="sections3")
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Takes'
        unique_together = (('student', 'course', 'sec', 'semester', 'year'),)


class Teaches(models.Model):
    course = models.ForeignKey(Section, models.DO_NOTHING, related_name="coursesTaught")
    sec = models.ForeignKey(Section, models.DO_NOTHING, related_name="sections4")
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name="semesters2")
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name="years2")
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING, related_name="teachers")

    class Meta:
        managed = False
        db_table = 'Teaches'
        unique_together = (('course', 'sec', 'semester', 'year', 'teacher'),)
'''

class Department(models.Model):
    dept_name = models.CharField(primary_key=True, max_length=32)
    building = models.CharField(max_length=32, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'
