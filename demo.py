import psycopg2
def create_table():
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    #creation of a database, we can run any of the sql statements using cursor
    cur = conn.cursor()
    cur.execute("create table students(student_id serial primary key,name text,address text,age int,number text);")
    print("Student table created")
    conn.commit()
    conn.close()

def insert_data():
    #code to accept data from the user
    name = input("Enter name: ")
    address = input("Enter address: ")
    age = input("Enter age: ")
    number = input("Enter number: ")
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("insert into students(name,address,age,number) values (%s,%s,%s,%s);",(name,address,age,number))
    print("Data added in the stuents table")
    conn.commit()
    conn.close()

def update_data():
    student_id = input("Enter id of the student to be updated")
    name = input("Enter name: ")
    address = input("Enter address: ")
    age = input("Enter age: ")
    number = input("Enter number: ")
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("update students set name=%s , address=%s , age=%s , number=%s where student_id=%s",(name,address,age,number,student_id))
    print("The student's data has been updated")
    conn.commit()
    conn.close

def update_single_datafield():
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    student_id = input("Enter id of the student to be updated")
    fields = {
        "1":("name","Enter the new name"),
        "2":("address","Enter the new age"),
        "3":("age","Enter the new age"),
        "4":("number","Enter the new number")
    }
    print("Which field would you like to update?")
    for key in fields:
        print(f"{key}:{fields[key][0]}")
    field_choice = input("Enter the number of the field you want to update: ")
    
    if field_choice in fields:
        field_name, prompt = fields[field_choice]
        new_value = input(prompt)
        sql = f"update students set {field_name}=%s where student_id=%s" #make sure in dynamic queries you don't use the tuple values
        cur = conn.cursor()
        cur.execute(sql,(new_value,student_id))
        print(f"{field_name} updated successfully")
    else:
        print("Invalid choice")
    conn.commit()
    conn.close

def delete_data():
    student_id = input("Enter the ID of the student you would like to delete: ")
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("select * from students where student_id=%s",(student_id,))   #even when you have single value in the tuple end it with comma so, that the python understand that this is tuple
    student = cur.fetchone()   #this fetches the entire student query

    if student:
        print(f"Student to be deleted: ID {student[0]}, Name: {student[1]}, Address: {student[2]}, Age: {student[3]}")
        choice = input("Are you sure you want ot delete the selected student? (yes/no)")
        if choice.lower()=="yes":   #lower used since, if the user even entrs the choice in capital letter it accepts the input and does the desired action
            cur.execute("delete from students where student_id=%s",(student_id,))
            print("The required student record has been deleted successfully :)")
        else:
            print("As,you selected no, hence, the student data has not been deleted :)")
    else:
        print("Student not found")
    conn.commit()
    conn.close()

def read_data():
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("select * from students;")
    students = cur.fetchall()                        #like fetchone fetches only one ropw but fetchall fetches all the rows
    for student in students:
        print(f"ID: {student[0]}, Name: {student[1]}, Address: {student[2]}, Age: {student[3]}, Number: {student[4]}")
    conn.close()

while True:
    print("\n Welcome to the student database management system")
    print("1. Create Table")
    print("2. Insert Data")
    print("3. Read Data")
    print("4. Update Data")
    print("5. Update Single Datafield")
    print("6. Delete Data")
    print("7. Exit")
    choice = input("Enter your choice (1-6): :)")
    if choice =='1':           #the choices are in single quote because the choices entered by the user are the strings
        create_table()
    elif choice=='2':
        insert_data()
    elif choice =='3':
        read_data()
    elif choice=='4':
        update_data()
    elif choice=='5':
        update_single_datafield()
    elif choice=='6':
        delete_data()
    elif choice=='7':
        break
    else: 
        print("Invalid choice, please enter the number between (1-7)")