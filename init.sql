DROP DATABASE
    university;

create database university;

use university;

create table
    department(
        dept_name varchar(32),
        building varchar(32),
        budget int,
        primary key (dept_name)
    );

INSERT INTO
    department
VALUES
    ('ECE', 'CAMP', 65000),
    ('CHE', 'CAMP', 40000),
    ('MA', 'SCIENCE CENTER', 55000),
    ('EC', 'SNELL', 45000),
    ('CEE', 'CAMP', 47500),
    ('CS', 'SCIENCE CENTER', 560000),
    ('COMM', 'SNELL', 20000),
    ('PY', 'SCIENCE CENTER', 12500),
    ('BY', 'SCIENCE CENTER', 13500),
    ('PH', 'SCIENCE CENTER', 70000),
    ('CSE', 'SNELL', 17000),
    ('AE', 'CAMP', 72000),
    ('DA', 'SNELL', 50500),
    ('AC', 'SNELL', 33000),
    ('HIST', 'SNELL', 12700),
    ('LAW', 'SNELL', 45000),
    ('ME', 'CAMP', 50000),
    ('MK', 'SNELL', 25000),
    ('SE', 'CAMP', 67000),
    ('OIS', 'SNELL', 37500),
    ('HSS', 'SNELL', 34500),
    ('IA', null, 20000),
    ('EM', null, 40000),
    ('ES', null, 30000);

create table
    instructor(
        id varchar(5),
        name varchar(32),
        dept_name varchar(32),
        salary int,
        primary key (id),
        foreign key (dept_name) references department(dept_name) on update cascade
    );

INSERT INTO
    instructor
VALUES
    ('12345', 'Hou', 'ECE', 100000),
    ('23456', 'Martin', 'MA', 100000),
    ('34567', 'Maciel', 'CS', 800000),
    ('13579', 'Ramsdell', 'PH', 105000),
    ('54545', 'Liu', 'ECE', 135000),
    ('45678', 'Liu', 'CS', 110000),
    ('21433', 'Thorpe', 'CS', 140000),
    ('28345', 'York', 'COMM', 125000),
    ('14534', 'White', 'MA', 150000),
    ('28346', 'Zhang', 'PY', 115000),
    ('89067', 'Tamon', 'CS', 120000),
    ('65623', 'Lee', 'ECE', 115000),
    ('12370', 'Skufca', 'MA', 132000),
    ('12371', 'Mondal', 'MA', 123000),
    ('10102', 'Hussain', 'ECE', 90000),
    ('22904', 'Khondker', 'ECE', 125000),
    ('20560', 'Conlon', 'OIS', 115000),
    ('35420', 'King', 'CHE', 200000),
    ('02441', 'Banerjee', 'CS', 100000),
    ('05133', 'Stein', 'HIST', 80000),
    ('16498', 'Lynch', 'CS', 112000),
    ('85732', 'Reynolds', 'MA', 108000),
    ('37801', 'Imtiaz', 'ECE', 115000),
    ('43203', 'Gohl', 'IA', 78000),
    ('34568', 'NEW MA', 'MA', 99000),
    ('56789', 'New Prof.', NULL, NULL),
    ('11001', 'Swati', 'ECE', 15000);

create table
    course(
        course_id varchar(8),
        title varchar(64),
        dept_name varchar(32),
        credits int,
        primary key(course_id),
        foreign key (dept_name) references department(dept_name) on update cascade
    );

INSERT INTO
    course
VALUES
    ('EE468', 'Databases', 'ECE', 3),
    ('EE363', 'Software Components', 'ECE', 3),
    ('EE262', 'Intro to Obj Oriented Prog', 'ECE', 3),
    ('EE221', 'Linear Circuits', 'ECE', 3),
    ('CS344', 'Algorithms and Data Structures', 'CS', 3),
    ('CS452', 'Computer Graphics', 'CS', 3),
    ('CS241', 'Computer Organization', 'CS', '3'),
    ('CS455', 'Computer Networks', 'CS', 3),
    ('EE368', 'Software Engineering', 'ECE', 3),
    ('CS350', 'Software Development and Design', 'CS', 3),
    ('CS444', 'Operating Systems', 'CS', 3),
    ('EE407', 'Computer Networks', 'ECE', 3),
    ('MA339', 'Applied Linear Algebra', 'MA', 3),
    (
        'CS458',
        'Formal Methods for Program Verification',
        'CS',
        3
    ),
    (
        'CS345',
        'Automate Theory and Formal Languages',
        'CS',
        3
    ),
    (
        'EE408',
        'Software Design for Visual Environments',
        'ECE',
        3
    ),
    ('DS241', 'Introduction to Data Science', 'MA', 3),
    ('ES250', 'Electrical Science', 'ES', 3),
    ('STAT381', 'Probability', 'MA', 3),
    ('STAT382', 'Statistics', 'MA', 3),
    ('CS451', 'Artificial Intelligence', 'CS', 3),
    ('CS470', 'Deeping', 'CS', 3),
    ('CS141', 'Intro. To Comp. Sci. I', 'CS', 4),
    ('CS142', 'Intro. To Comp. Sci. II', 'CS', 3),
    (
        'EE361',
        'Fundamentals of Software Engineering',
        'ECE',
        3
    ),
    ('IA628', 'Intro to Big Data Architecture', 'IA', 3),
    ('IA651', 'Applied Machine Learning', 'IA', 3),
    ('IA650', 'Data Mining', 'IA', 3),
    ('EE523', 'Introduction to Biometrics', 'ECE', 3),
    ('CS570', 'Deep Learning', 'CS', 3),
    ('IA640', 'Info Visualization', 'IA', 3),
    ('MA131', 'Calculus I', 'MA', 3),
    ('MA132', 'Calculus II', 'MA', 3),
    ('MA231', 'Calculus III', 'MA', 3),
    ('MA211', 'Discrete Math and Proof', 'MA', 3),
    ('PH131', 'Physics I', 'PH', 3),
    ('EE260', 'Embeded Systems', 'ECE', 3),
    ('EE462', 'Software Systems Architecture', 'ECE', 3),
    ('CS460', 'Database Systems', 'ECE', 3),
    ('CS341', 'Programming Languages', 'ECE', 3);

create table
    prereq(
        course_id varchar(8),
        preq_id varchar(8),
        primary key (course_id, preq_id),
        foreign key (course_id) references course(course_id),
        foreign key (preq_id) references course(course_id)
    );

INSERT INTO
    prereq
VALUES
    ('EE468', 'CS141'),
    ('EE363', 'EE262'),
    ('MA132', 'MA131'),
    ('MA339', 'MA132'),
    ('MA231', 'MA132'),
    ('EE262', 'CS141'),
    ('CS344', 'CS142'),
    ('CS455', 'CS241'),
    ('CS458', 'CS345'),
    ('CS241', 'CS141'),
    ('EE368', 'EE408'),
    ('EE368', 'EE363'),
    ('STAT382', 'STAT381'),
    ('CS451', 'CS142'),
    ('CS470', 'MA339'),
    ('CS142', 'CS141'),
    ('EE361', 'EE262'),
    ('EE260', 'CS141'),
    ('EE407', 'CS141'),
    ('EE462', 'CS141'),
    ('CS460', 'CS141'),
    ('CS341', 'EE361'),
    ('EE408', 'EE262'),
    ('CS344', 'EE262'),
    ('CS344', 'MA211');

create table
    section(
        course_id varchar(8),
        sec_id varchar(4),
        semester int,
        year int,
        building varchar(32),
        room varchar(8),
        capacity int,
        primary key(course_id, sec_id, semester, year),
        foreign key (course_id) references course(course_id)
    );

INSERT INTO
    section
VALUES
    ("CS141", "01", 1, 2019, "CAMP", "194", 60),
    ("CS141", "02", 1, 2019, "CAMP", "194", 60),
    ("CS141", "01", 2, 2019, "CAMP", "194", 60),
    ("CS141", "02", 2, 2019, "CAMP", "194", 60),
    ("CS141", "03", 2, 2019, "CAMP", "194", 60),
    ("CS141", "01", 1, 2020, "CAMP", "194", 60),
    ("CS141", "02", 1, 2020, "CAMP", "194", 60),
    ("CS141", "03", 1, 2020, "CAMP", "194", 60),
    ("EE468", "01", 1, 2019, "CAMP", "194", 40),
    ("EE468", "02", 2, 2019, "CAMP", "194", 40),
    ("EE468", "01", 2, 2019, "CAMP", "194", 40),
    ("EE468", "01", 1, 2020, "CAMP", "194", 40);

create table
    teaches (
        course_id varchar(8),
        sec_id varchar(4),
        semester int,
        year int,
        teacher_id varchar(5),
        primary key (course_id, sec_id, semester, year, teacher_id),
        foreign key (course_id, sec_id, semester, year) references Section(course_id, sec_id, semester, year),
        foreign key (teacher_id) references instructor(id)
    );

INSERT INTO
    teaches
VALUES
    ("EE468", "01", 1, 2019, "12345"),
    ("EE468", "02", 2, 2019, "12345"),
    ("EE468", "01", 2, 2019, "12345"),
    ("EE468", "01", 1, 2020, "12345"),
    ("CS141", "01", 1, 2019, '21433'),
    ("CS141", "02", 1, 2019, '21433'),
    ("CS141", "01", 2, 2019, '21433'),
    ("CS141", "02", 2, 2019, '21433'),
    ("CS141", "03", 2, 2019, '21433'),
    ("CS141", "01", 1, 2020, '21433'),
    ("CS141", "02", 1, 2020, '21433'),
    ("CS141", "03", 1, 2020, '21433');

create table
    student(
        student_id varchar(8),
        name varchar(32),
        dept_name varchar(32),
        total_credits int,
        primary key (student_id),
        foreign key (dept_name) references department(dept_name) on update cascade
    );

INSERT INTO
    student
VALUES
    ('00128', "Zhang", "CS", 102),
    ('12345', "Shankar", "CS", 32),
    ('19991', "Brandt", "HIST", 80),
    ('44553', "Peltier", "PH", 56),
    ('45678', "Levy", "PH", 46),
    ('54321', "Williams", "CS", 54),
    ('70557', "Snow", "PH", 0),
    ('05401', "Megan", "CS", 30),
    ('05405', "Alex", "CS", 93),
    ('76543', "Brown", "CS", 58),
    ('76653', "Aoi", "ECE", 60),
    ('98765', "Bourikas", "ECE", 98),
    ('98988', "Tanaka", "BY", 120);

create table
    takes(
        student_id varchar(8),
        course_id varchar(8),
        sec_id varchar(4),
        semester int,
        year int,
        grade varchar(2),
        primary key (student_id, course_id, sec_id, semester, year),
        foreign key(student_id) references Student(student_id),
        foreign key (course_id, sec_id, semester, year) references section(course_id, sec_id, semester, year)
    );

INSERT INTO
    takes
VALUES
    ('54321', "CS141", "01", 1, 2019, "F"),
    ('98765', "CS141", "02", 1, 2019, "C-"),
    ('00128', "CS141", "02", 1, 2019, "A"),
    ('12345', "CS141", "01", 2, 2019, "C"),
    ('45678', "CS141", "01", 2, 2019, "F"),
    ('45678', "CS141", "02", 1, 2020, "B+"),
    ('54321', "EE468", "02", 2, 2019, "B"),
    ('00128', "EE468", "01", 2, 2019, "A-"),
    ('05401', "EE468", "02", 2, 2019, "C"),
    ('05405', "EE468", "01", 1, 2020, "D"),
    ('98765', "EE468", "01", 1, 2020, "B");

-- research( Title, dept_name, instructor_id, start, end date)
CREATE TABLE research(
    research_id INT AUTO_INCREMENT,
    title VARCHAR(60),
    dept_name VARCHAR(32),
    PI VARCHAR(5),
    start_date DATE,
    end_date DATE,
    PRIMARY KEY (research_id),
    FOREIGN KEY (PI) REFERENCES instructor(id),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name)
);
INSERT INTO research VALUES
                         (1, 'User Authentication Biometrics', 'ECE', '12345', '2019-01-01', '2020-09-06'),
                         (2, 'Best Password Research', 'ECE', '12345', '2019-08-26', '2020-02-07');

CREATE TABLE funding(
    research_id INT NOT NULL,
    funding_amount INT,
    sponsor_org VARCHAR(32),
    FOREIGN KEY (research_id) REFERENCES research(research_id),
    PRIMARY KEY (research_id, funding_amount, sponsor_org)
);
INSERT INTO funding VALUES
                        (2, 13203, 'NASA'),
                        (1, 2242, 'CIA'),
                        (2, 100000, 'NSA'),
                        (1, 3313, 'abc');

CREATE TABLE publication(
    publication_id INT AUTO_INCREMENT,
    title VARCHAR(64),
    publish_date DATE,
    publisher_name VARCHAR(32),
    research_id INT,
    PRIMARY KEY (publication_id),
    FOREIGN KEY (research_id) REFERENCES research(research_id)
);

INSERT INTO publication VALUES
                            (1, 'The Worlds BEST password!', '2020-02-07', 'Clarkson', 2);

CREATE TABLE student_publishes(
    publication_id INT,
    student_id VARCHAR(8),
    PRIMARY KEY (publication_id, student_id),
    FOREIGN KEY (publication_id) REFERENCES publication(publication_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)

);
CREATE TABLE instructor_publishes(
    publication_id INT,
    instructor_id VARCHAR(5),
    PRIMARY KEY (publication_id, instructor_id),
    FOREIGN KEY (publication_id) REFERENCES publication(publication_id),
    FOREIGN KEY (instructor_id) REFERENCES instructor(id)
);
