import random
us_pt = 0
cmptr = 0
def game():
    global us_pt,cmptr
    us=input("enter your choice{stone,paper,scissors}: ").lower()
    ch=["stone","paper","scissors"]
    computer=random.choice(ch)

    if us==computer:
        print("it is a tie!")
    elif us=="stone" and computer=="scissors":
        us_pt+=1
        print("you win this round")

    elif us=="paper" and computer=="stone":
        us_pt+=1
        print("you win this round")
    elif   us=="scissors" and computer=="paper" :
        us_pt+=1
        print("you win this round")
    else:
        cmptr+=1
        print("computer win this round")
while True:
    print("\n1.Play \n2.Exit")
    us_ch=int(input("choose one:"))
    if us_ch==1:
        game()
    else:
        break
    print(f'user total point:{us_pt}')
    print(f'computer total point :{cmptr}')
    if us_pt==cmptr:
        print("it is a tie!")
    elif us_pt>cmptr:
        print("USER WON!!!")
    else:
        print("COMPUTER WON!!!!")


