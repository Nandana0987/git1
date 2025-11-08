import time
def add_exp():
    f=open("expense1.txt","a")
    x = input("enter name of your expense:")
    y=int(input("amount:"))
    z=time.ctime()
    f.write(f"{x} {y} {z}\n")
    print("expense added.")
    f.close()
def view_exp():
    f = open("expense1.txt", "r")
    print("category|amount|date")
    print("_____________________")
    for i in f:
        print(i)
def tot_exp():
    my_exp=[]
    f = open("expense1.txt", "r")
    for i in f:
         exp= i.split()
         my_exp.append(int(exp[1]))
    print(f"Total expense: {sum(my_exp)}")

while True:
    print("\n1.Add Expense\n2.View Expense\n3.Total Expense\n4.Exit\n")
    choice=int(input("enter yor choice:"))
    if choice==1:
        add_exp()
    elif choice==2:
        view_exp()
    elif choice==3:
        tot_exp()
    elif choice==4:
        print("exit")
        break

    else:

        print("invalid choice")
