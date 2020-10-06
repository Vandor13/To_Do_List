# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import random
import datetime

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='')
    deadline = Column(Date, default=datetime.datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def add_task():
    name = input("Enter task:\n")
    dead_line_raw = input("Enter deadline (YYYY-MM-DD):\n")
    if dead_line_raw != "":
        dead_line = datetime.datetime.strptime(dead_line_raw, "%Y-%m-%d").date()
    else:
        dead_line = datetime.datetime.today()
    new_row = Task(id=random.randint(1, 9999), task=name, deadline=dead_line)
    session.add(new_row)
    session.commit()
    print("The task has been added!")
    print()


def get_tasks_week():
    today = datetime.datetime.now()
    # next_week = datetime.datetime.now() + datetime.timedelta(days=7)
    # tasks = session.query(Task).\
    #     filter(today.date() <= Task.deadline, Task.deadline < next_week.date()). \
    #     order_by(Task.deadline).all()
    # print("This week:")
    for i in range(7):
        complete_date = today + datetime.timedelta(days=i)
        date = complete_date.date()
        tasks = session.query(Task).filter(Task.deadline == date).all()
        print(date.strftime("%A %d %b") + ":")
        if len(tasks) > 0:
            for j in range(len(tasks)):
                # print(type(task_object.deadline))
                print("{}. {}".format(str(j + 1), str(tasks[j])))
        else:
            print("Nothing to do!")
        print()


def get_tasks_today():
    today = datetime.datetime.now()
    tasks = session.query(Task).filter(today.date() == Task.deadline).all()
    print("Today {}:".format(today.strftime("%d %b")))
    if tasks:
        for i in range(len(tasks)):
            # print(type(task_object.deadline))
            print("{}. {}".format(str(i + 1), str(tasks[i])))
    else:
        print("Nothing to do!")
    print()


def get_missed_tasks():
    today = datetime.datetime.now()
    tasks = session.query(Task).filter(today.date() > Task.deadline).all()
    print("Missed tasks:")
    if tasks:
        for i in range(len(tasks)):
            date_string = tasks[i].deadline.strftime("%d %b").replace("0", "")
            print("{}. {}. {}".format(str(i + 1), str(tasks[i]), date_string))
    else:
        print("Nothing is missed!")
    print()


def get_all_tasks():
    tasks = session.query(Task).order_by(Task.deadline).all()
    print("All tasks:")
    if tasks:
        for i in range(len(tasks)):
            # print(type(task_object.deadline))
            date_string = tasks[i].deadline.strftime("%d %b").replace("0", "")
            print("{}. {}. {}".format(str(i + 1), str(tasks[i]), date_string))
    else:
        print("Nothing to do!")
    print()


def delete_task():
    tasks = session.query(Task).all()
    print("Choose the number of the task you want to delete:")
    if tasks:
        for i in range(len(tasks)):
            # print(type(task_object.deadline))
            date_string = tasks[i].deadline.strftime("%d %b").replace("0", "")
            print("{}. {}. {}".format(str(i + 1), str(tasks[i]), date_string))
        chosen_task_index = int(input())
        session.delete(tasks[chosen_task_index - 1])
        session.commit()
        print("The task has been deleted!")
    else:
        print("Nothing to delete!")
    print()


def delete_all_tasks():
    tasks = session.query(Task).all()
    if tasks:
        for task in tasks:
            session.delete(task)


def main_menu():
    user_choice = ""
    while user_choice != "0":
        print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")
        user_choice = input("> ")
        print()
        if user_choice == "1":
            get_tasks_today()
        if user_choice == "2":
            get_tasks_week()
        elif user_choice == "3":
            get_all_tasks()
        elif user_choice == "4":
            get_missed_tasks()
        elif user_choice == "5":
            add_task()
        elif user_choice == "6":
            delete_task()
        else:
            print("Unknown Choice. Please select a valid option.")
            print()
    print("Bye!")


# delete_all_tasks()
main_menu()
