print("🧾EMPLOYEE MANAGEMENT SYSTEM🧾".center(70, "."))

import sqlite3
from datetime import datetime
import re
from tabulate import tabulate


conn = sqlite3.connect('EMS.db')
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS users  (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    usertype TEXT
);
""")

c.execute("""
CREATE TABLE IF NOT EXISTS employee (
        emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id  INTEGER UNIQUE,
        emp_name TEXT,
        emp_dob  DATE,
        email_id TEXT UNIQUE,
        phone    INTEGER,
        emp_designation  TEXT,
        salary  REAL,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
        );
 """)

c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    att_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    status TEXT ,
    check_in TEXT ,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    UNIQUE(user_id,date)
);
""")
conn.commit()

def check_phone():
    while True:
        phone = input("Enter employee phone number: ")
        if len(phone) == 10:
            return int(phone)
        else:
            print("❌ Invalid phone number! Must be 10 digits.")

def check_email():
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    while True:
        email = input("Enter employee email: ")
        if  re.search(pattern, email):
            return email
        else:
            print("❌ Invalid email format! Please enter a valid email.")

def check_dob():
    while True:
        emp_dob_in= input("Enter employee date of birth (YYYY-MM-DD): ")
        try:
            emp_dob = datetime.strptime(emp_dob_in, "%Y-%m-%d").strftime("%Y-%m-%d")
            break
        except ValueError:
            print("❌ Invalid date format")
    return emp_dob


def add_employee():
    print("\nADD EMPLOYEE➕")
    print("\nExisting employee accounts:")
    c.execute("""
    SELECT user_id,username FROM users WHERE usertype='employee';
    """)
    users = c.fetchall()
    if not users:
        print("❌ No employee login accounts found!")
        return
    print(tabulate(users, headers=["User ID", "Username"], tablefmt="grid"))
    user_id=int(input("Enter user id to create profile: "))
    c.execute("""
    SELECT * FROM employee WHERE user_id=?""",(user_id,))
    if  c.fetchone():
        print("Employee profile already exists❗")
        return
    emp_name=input("enter employee name: ")
    emp_dob=check_dob()
    email_id=check_email()
    phone=check_phone()
    emp_designation=input("enter employee designation: ")
    salary=float(input("enter employee salary: "))

    c.execute("""
    INSERT INTO employee( user_id,emp_name,emp_dob,email_id,phone,emp_designation,salary)
    VALUES (?,?,?,?,?,?,?)""",(user_id,emp_name, emp_dob,email_id, phone, emp_designation, salary,))
    print("Employee profile created successfully✅")
    conn.commit()

def view_employee():
    print("\n EMPLOYEE LIST📋")
    c.execute("""
    SELECT * FROM employee """)
    rows =c.fetchall()
    if not rows :
        print("NO EMPLOYEE FOUND❗")
        return
    headers = ["EMP ID", "USER ID", "NAME", "DOB", "EMAIL", "PHONE", "DESIGNATION", "SALARY"]
    print(tabulate(rows, headers=headers,tablefmt="grid"))

def update_employee():
    print("\nUPDATE EMPLOYEE📝")
    try:
        emp_id=int(input("enter employee id: "))
        c.execute("""
                  SELECT emp_name FROM employee WHERE emp_id = ?""", (emp_id,))
        emp=c.fetchone()
        if not emp:
            print("employee not found❌")
            return
        emp_name = emp[0]
        print(f"\nUpdating profile of employee: 👤 {emp_name}")
        while True:
            print("╭────────────────────────────╮")
            print("│      Choose an Option      │")
            print("├────────────────────────────┤")
            print("│ 1) Employee Name           │")
            print("│ 2) Date of birth           │")
            print("│ 3) Email id                │")
            print("│ 4) Phone number            │")
            print("│ 5) Designation             │")
            print("│ 6) Salary                  │")
            print("│ 7) Exit                    │")
            print("╰────────────────────────────╯")

            try:
                choice = int(input("Enter column to update: "))
            except ValueError:
                print("❌ Enter a number only")
                continue
            if choice == 1:
                emp_name = input("Enter new name: ")
                c.execute("UPDATE employee SET emp_name=? WHERE emp_id=?",
                          (emp_name, emp_id))
            elif choice == 2:
                emp_dob = check_dob()
                c.execute("UPDATE employee SET emp_dob=? WHERE emp_id=?",
                          (emp_dob, emp_id))
            elif choice == 3:
                email_id = check_email()
                c.execute("UPDATE employee SET email_id=? WHERE emp_id=?",
                          (email_id, emp_id))
            elif choice == 4:
                phone = check_phone()
                c.execute("UPDATE employee SET phone=? WHERE emp_id=?",
                       (phone, emp_id))
            elif choice == 5:
                emp_designation = input("Enter new designation: ")
                c.execute("UPDATE employee SET emp_designation=? WHERE emp_id=?",
                          (emp_designation, emp_id))
            elif choice == 6:
                salary = float(input("Enter new salary: "))
                c.execute("UPDATE employee SET salary=? WHERE emp_id=?",
                          (salary, emp_id))
            elif choice == 7:
                conn.commit()
                print("✅ Employee profile updated successfully")
                break
            else:
                print("❌ Invalid choice")
                continue
            conn.commit()
    except ValueError:
        print("Invalid input ❌ Employee ID,  and salary must be numbers.")


def delete_employee():
    print("\n DELETE EMPLOYEE❗")
    try:
        emp_id=int(input("enter employee id: "))
        c.execute("""
         SELECT * FROM employee WHERE emp_id=?""", (emp_id,))
        if not c.fetchone():
            print("employee not found❌")
            return
        c.execute("""
        DELETE FROM employee WHERE emp_id=?
        """,(emp_id,))
        print("EMPLOYEE DETAILS REMOVED🗑️")
        conn.commit()
    except ValueError:
        print("Invalid input❌.Enter numeric value")
def search_employee():
    print("\n SEARCH EMPLOYEE🔎")
    try:
        emp_id=int(input("enter employee id to search: "))
        c.execute("""
        SELECT * FROM employee WHERE emp_id=?""",(emp_id,))
        rows=c.fetchall()
        if not rows:
            print("employee not found❌")
            return
        headers = ["EMP ID", "USER ID", "NAME", "DOB", "EMAIL", "PHONE", "DESIGNATION", "SALARY"]
        print(tabulate(rows, headers=headers,tablefmt="grid"))
    except ValueError:
        print("Invalid input❌.Enter numeric value")


def update_self(user_id):
    print("\nUPDATE SELF📝")
    c.execute("""
    SELECT * FROM employee WHERE user_id=?""",(user_id,))
    if not c.fetchone():
        print("employee not found❌")
        return
    while True:
        print("╭────────────────────────────╮")
        print("│      Choose an Option      │")
        print("├────────────────────────────┤")
        print("│ 1) Employee Name           │")
        print("│ 2) Date of birth           │")
        print("│ 3) Phone number            │")
        print("│ 4) Exit                    │")
        print("╰────────────────────────────╯")

        try:
            choice = int(input("Enter column to update: "))
        except ValueError:
            print("❌ Enter a number only")
            continue

        if choice == 1:
            emp_name = input("Enter new name: ")
            c.execute("UPDATE employee SET emp_name=? WHERE user_id=?",
                      (emp_name, user_id))
        elif choice == 2:
            emp_dob = check_dob()
            c.execute("UPDATE employee SET emp_dob=? WHERE user_id=?",
                      (emp_dob, user_id))
        elif choice==3:
            phone = check_phone()
            c.execute("UPDATE employee SET phone=? WHERE user_id=?",
                      (phone, user_id))
        elif choice == 4:
            conn.commit()
            print("✅ Your profile updated successfully")
            break
        else:
            print("❌ Invalid choice")
            continue

        conn.commit()
        print("✔ Field updated successfully")

def view_self(user_id):
    c.execute("SELECT * FROM employee WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    if not rows:
        print("employee not found❌")
        return
    headers = ["EMP ID", "USER ID", "NAME", "DOB", "EMAIL", "PHONE", "DESIGNATION", "SALARY"]
    print(tabulate(rows, headers=headers,tablefmt="grid"))


def mark_attendance(user_id):
    today = datetime.now().strftime("%Y-%m-%d")
    now=datetime.now().strftime("%H:%M:%S")

    try:
        c.execute("""
        INSERT INTO attendance (user_id,date,check_in, status)
        VALUES (?, ?, ?,'Present')
        """, (user_id,today,now))
        conn.commit()
        print("Attendance marked successfully ✅")
    except sqlite3.IntegrityError:
        print("Attendance already marked for today ❗")

def view_my_attendance(user_id):
    c.execute("""
    SELECT  date,status, check_in FROM attendance WHERE user_id=?
    """, (user_id,))

    rows = c.fetchall()
    if not rows:
        print("No attendance records found❗")
        return
    headers = ["DATE", "STATUS", "CHECK-IN"]
    print(tabulate(rows, headers=headers,tablefmt="grid"))


def view_all_attendance():
    print("\nALL EMPLOYEES ATTENDANCE📋")

    c.execute("""
    SELECT e.emp_name, e.emp_id,a.date, a.status, a.check_in
    FROM attendance a
    JOIN users u ON a.user_id = u.user_id
    JOIN employee e ON a.user_id = e.user_id
    """)

    row = c.fetchall()
    if not row:
        print("No attendance records found❗")
        return
    headers = ["NAME", "EMP ID", "DATE", "STATUS", "CHECK-IN"]
    print(tabulate(row, headers=headers,tablefmt="grid"))

def register():
    usertype = input("Enter user type (HR/employee): ").strip()
    usertype = usertype.lower()
    if usertype not in ["hr", "employee"]:
        print("Invalid user type ❌")
        return
    u = input("Enter username: ")
    p1 = input("Enter password: ")
    p2 = input("Confirm password: ")
    if p1 == p2:
        try:
            c.execute("""
            INSERT INTO users (username, password, usertype)
            VALUES (?, ?, ?);
            """, (u, p1, usertype))
            conn.commit()
            print(f"Registered successfully as {usertype} ✅")
        except sqlite3.IntegrityError:
            print("User name already Exists‼️.")
            if usertype=="employee":
                employee_login()
            else:
                hr_login()
    else:
        print("❌ Passwords do not match!")

    conn.commit()

def hr_login():
    print("\nLOGIN WINDOW 💻 (HR)")
    u = input("Enter username: ")
    p = input("Enter password: ")

    c.execute("""
    SELECT * FROM users
    WHERE username=? AND password=? AND usertype='hr'
    """, (u, p))

    user = c.fetchone()

    if user:
        print("HR Login successful ✅")
        hr_window()
    else:
        print("❌ Invalid credentials ")

def employee_login():
    print("\nLOGIN WINDOW 💻 (Employee)")
    u = input("Enter username: ")
    p = input("Enter password: ")

    c.execute("""
    SELECT * FROM  users
    WHERE username=? AND password=? AND usertype='employee'
    """, (u, p))

    user = c.fetchone()

    if user:
        print("Employee Login successful ✅")
        user_id = user[0]
        employee_window(user_id)
    else:
        print("❌ Invalid credentials")

def hr_window():
    print("\n")
    print('HR Dashboard 🖥️'.center(70,"."))
    while True:
        print("╭────────────────────────────╮")
        print("│      Choose an Option      │")
        print("├────────────────────────────┤")
        print("│ 1) Add Employee            │")
        print("│ 2) View Employee           │")
        print("│ 3) Update Employee         │")
        print("│ 4) Delete Employee         │")
        print("│ 5) Search Employee         │")
        print("│ 6) View Employee Attendance│")
        print("│ 7) Logout                  │")
        print("╰────────────────────────────╯")

        try:
            ch = int(input("Enter your choice: "))
        except ValueError:
            print("❌ Please enter a number only")
            continue
        if ch == 1:
            add_employee()
        elif ch == 2:
            view_employee()
        elif ch == 3:
            update_employee()
        elif ch == 4:
            delete_employee()
        elif ch == 5:
            search_employee()
        elif ch == 6:
            view_all_attendance()
        elif ch == 7:
            print("Logging out 🏃‍♀️‍➡️")
            break
        else:
            print("Invalid choice ❗")


def employee_window(user_id):
    while True:
        print("\n")
        print("Employee Dashboard 🖥️".center(70, "."))
        print("╭────────────────────────────╮")
        print("│      Choose an Option      │")
        print("├────────────────────────────┤")
        print("│ 1) View self               │")
        print("│ 2) Update self             │")
        print("│ 3) Mark Attendance         │")
        print("│ 4) View Attendance         │")
        print("│ 5) Logout                  │")
        print("╰────────────────────────────╯")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("❌ Please enter a number only")
            continue
        if choice==1:
            view_self(user_id)
        elif choice==2:
            update_self(user_id)
        elif choice==3:
            mark_attendance(user_id)
        elif choice==4:
            view_my_attendance(user_id)
        elif choice==5:
            print('Logging out🏃‍♀️‍➡️')
            break
        else:
            print("Invalid  choice❗")

def main_menu():
    while True:
        print("╭────────────────────────────╮")
        print("│      Choose an Option      │")
        print("├────────────────────────────┤")
        print("│ 1) Register                │")
        print("│ 2) HR Login                │")
        print("│ 3) Employee Login          │")
        print("│ 4) Exit                    │")
        print("╰────────────────────────────╯")
        try:
            ch = int(input("Enter your choice: "))
        except ValueError:
            print("❌ Please enter a number only")
            continue
        if ch == 1:
            register()
        elif ch == 2:
            hr_login()
        elif ch == 3:
            employee_login()
        elif ch == 4:
            print("Exiting... Goodbye👋")
            break
        else:
            print("Oops‼️ Wrong option")
main_menu()
conn.close()