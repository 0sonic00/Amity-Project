import sqlite3


# defining function to create the database and table
def setup_database():
    conn = sqlite3.connect('hcl_employees.db')  # connecting to database
    cur = conn.cursor()  # cursor interacting with database

    # creating the table if it does not exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dob TEXT,
            blood_group TEXT,
            contact TEXT UNIQUE
        )
    ''')

    conn.commit() # saving command
    conn.close()  # closing the database connection


# defining function to add an employee
def add_employee(name, dob, blood_group, contact):
    conn = sqlite3.connect('hcl_employees.db')  # command to connect to the database
    cur = conn.cursor()

    # trying to add the employee
    try:
        cur.execute('''
            INSERT INTO employees (name, dob, blood_group, contact)
            VALUES (?, ?, ?, ?)
        ''', (name, dob, blood_group, contact))  # insert the employee data

        conn.commit()  # save command
        employee_id = cur.lastrowid  # get the new employee ID
        conn.close()  # closing the database
        return employee_id
    except sqlite3.IntegrityError:
        conn.close()  # close the database if there is an error
        return None  # return to None if there is a duplicate


# defining function to check if an employee already exists
def check_employee(contact):
    conn = sqlite3.connect('hcl_employees.db')  # connecting to the company database
    cur = conn.cursor()

    # checking if there is an existing employee
    cur.execute('SELECT id, name FROM employees WHERE contact = ?', (contact,))
    result = cur.fetchone()
    conn.close()
    return result


# defining function to create an email of employee
def make_email(name):
    name_parts = name.split()  # split the name into parts
    first_name = name_parts[0].lower()  # changing first name in lowercase
    last_name = name_parts[-1].lower()  # changing last name in lowercase
    email = f"{last_name}.{first_name}@hcltech.com"  # email created
    return email


# Defining function to print the details of employee
def show_details(name, employee_id, blood_group, email):
    name_parts = name.split()
    display_name = f"{name_parts[0]} {name_parts[-1]}"
    print("\nEmployee Details:")
    print("Name:", display_name)
    print("Company email:", email)
    print("Company ID:", str(employee_id).zfill(7))
    print("Blood group:", blood_group)



def main():
    setup_database()

    # asking for user input
    print("Enter employee details:")
    name = input("Name: ")
    dob = input("Date of Birth (DD/MM/YYYY): ")
    blood_group = input("Blood Group: ")
    contact = input("Contact Number: ")

    # checking if the employee already exists
    existing = check_employee(contact)
    if existing:
        print("\nEmployee already exists!")
        print("Name:", existing[1])
        print("Company ID:", str(existing[0]).zfill(7))
    else:
        # if it is not adding the employee
        employee_id = add_employee(name, dob, blood_group, contact)
        if employee_id:
            email = make_email(name)
            show_details(name, employee_id, blood_group, email)
        else:
            print("Error: Employee with this contact already exists.")


# let's run the program
if __name__ == "__main__":
    main()
