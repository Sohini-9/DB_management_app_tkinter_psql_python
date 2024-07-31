from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import psycopg2

def run_query(query,parameters=()):   #we are accepting the parameters in the form of tuple as during fetching in the sql query we were fetching in the form of the tuple
    conn = psycopg2.connect(dbname="studentdb",user="postgres",password="admin123",host="localhost",port="5432")
    cur = conn.cursor()
    query_result=None
    try:
        cur.execute(query,parameters)
        if query.lower().startswith("select"):   #only if like it is a select query then, we are wanting to fetch the data hence we are first converting the everything of the string to the lower and then checking whether it starts with the keyword select
            query_result = cur.fetchall()
        conn.commit()
    except psycopg2.Error as e:
        messagebox.showerror("Database Error",str(e))
    finally:
        cur.close()
        conn.close()
    return query_result

def refresh_treeview():
    for item in tree.get_children(): #this we are doing in order to get rid of the duplicate entries, get_children() menthod gives all the records prsent inside the treeview
        tree.delete(item)
    records = run_query("select * from students;")
    for record in records:
        tree.insert('',END,values=record)

def insert_data():
    query = "insert into students(name,address,age,number) values (%s,%s,%s,%s);"  #here we are fetching the parameters from the tkinter window itself hence, the parameters in tuples as in the previous example are not present
    parameters = (name_entry.get(),address_entry.get(),age_entry.get(),phone_entry.get())
    run_query(query,parameters)
    messagebox.showinfo("Information","Data inserted successfully")
    refresh_treeview()

def delete_data():
    selected_item = tree.selection()[0]   #this selection method of the tree gives the data which is selected from the console
    #print(selected_item)
    student_id = tree.item(selected_item)['values'][0]
    query = "delete from students where student_id=%s"
    parameters = (student_id,)
    run_query(query,parameters)
    messagebox.showinfo("Information","Data has been deleted successfully")
    refresh_treeview()

def update_data():
    selected_item = tree.selection()[0]
    student_id = tree.item(selected_item)['values'][0]
    query = "update students set name=%s, address=%s, age=%s, number=%s where student_id=%s;"
    parameters = (name_entry.get(),address_entry.get(),age_entry.get(),phone_entry.get(),student_id)
    run_query(query,parameters)
    messagebox.showinfo("Information","Data updated successfully")
    refresh_treeview()

def create_table():
    query = "create table if not exists(student_id serial primary key,name text,address text,age int,number text);"
    run_query(query)
    messagebox.showinfo("Information","Table created")
    refresh_treeview()

root = Tk()
root.title("Student management system")

frame = LabelFrame(root,text="Student Data")
frame.grid(row=0,column=0,padx=10,pady=10,sticky="ew")   #sticky is for the alignment and ew stands for east and west which means it will stretch from east to westmeasn from left to right

Label(frame,text="Name:").grid(row=0,column=0,padx=2,sticky="w")    #sticky west means left,   we are not passing root in this label because we are not placing the label on the root but on the frame
#if you are thinking the frame and label both are having the row and column as same then, it shoukd be focused on that the frame is presnt in the row and column of the root and the label is present on the frame's row and column
name_entry = Entry(frame)
name_entry.grid(row=0,column=1,pady=2,sticky="ew")

Label(frame,text="Address").grid(row=1,column=0,padx=2,sticky="w")
address_entry = Entry(frame)
address_entry.grid(row=1,column=1,pady=2,sticky="ew")

Label(frame,text="Age:").grid(row=2,column=0,padx=2,sticky="w")
age_entry = Entry(frame)
age_entry.grid(row=2,column=1,pady=2,sticky="ew")

Label(frame,text="Phone Number:").grid(row=3,column=0,padx=2,sticky="w")
phone_entry = Entry(frame)
phone_entry.grid(row=3,column=1,pady=2,sticky="ew")

button_frame = Frame(root)
button_frame.grid(row=1,column=0,pady=5,sticky="ew")

Button(button_frame,text="Create Table",command=create_table).grid(row=0,column=0,padx=5)
Button(button_frame,text="Add Data",command=insert_data).grid(row=0,column=1,padx=5)
Button(button_frame,text="Update Data").grid(row=0,column=2,padx=5)
Button(button_frame,text="Update Choosen Field Data",command=update_data).grid(row=0,column=3,padx=5)
Button(button_frame,text="Delete Data",command=delete_data).grid(row=0,column=4,padx=5)

#creatinga treeview

tree_frame = Frame(root)
tree_frame.grid(row=2,column=0,padx=10,sticky="nsew")

#scrollbar creation
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT,fill=Y)

tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="browse")   #yscrollcommand is used to set the scrollbar to the treeview and the set method is used to position the scrollbar when the treeview moves, the selectmode is used to select from the treeview i.e. we can select one item at a time
tree.pack()
tree_scroll.config(command=tree.yview) #to update the values in the treeview

tree['columns']=("student_id","name","address","age","number")
tree.column("#0",width=0,stretch=NO)
tree.column("student_id",anchor=CENTER,width=10)   #anchor is for the alignment
tree.column("name",anchor=CENTER,width=120)
tree.column("address",anchor=CENTER,width=120)
tree.column("age",anchor=CENTER,width=50)
tree.column("number",anchor=CENTER,width=120)

tree.heading("student_id",text="ID",anchor=CENTER)
tree.heading("name",text="NAME",anchor=CENTER)
tree.heading("address",text="ADDRESS",anchor=CENTER)
tree.heading("age",text="AGE",anchor=CENTER)
tree.heading("number",text="NUMBER",anchor=CENTER)

refresh_treeview()
root.mainloop()