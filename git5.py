class ATM():
    def __init__(self,n,p):
        self.account_holder=n
        self.pin=p
        self.balance=0
    def c_accnt(self):
        print("*************** ACCOUNT DETAILS **************")
        print("account_holder",self.account_holder)
        print("PIN",self.pin)
    def check_balance(self,entered_pin):
        if self.pin==entered_pin:
            print(f"Current Balance : {self.balance}")
        else:
            print("incorrect pin")
    def deposit(self,entered_pin):
        if self.pin == entered_pin:
             amount=float(input("Enter depositing amount:"))
             print("amount deposited:",amount)
             self.balance=self.balance+amount
        else:
            print("incorrect pin")
    def withdrawal(self,entered_pin):
        if self.pin == entered_pin :
            withdrawal_amount=int(input("Enter amount to withdraw: "))
            if withdrawal_amount>self.balance:
               print("Insufficient Balance")
            else:
                self.balance=self.balance- withdrawal_amount
                print("amount withdrawen:", withdrawal_amount)
        else:
            print("incorrect pin")
    def change_pin(self):
        old_pin=int(input("enter your old pin number: "))
        if old_pin==self.pin:
            new_pin=int(input("enter your new pin:"))
            self.pin=new_pin
person1=ATM("Nandana",2004)
while True:
    print("\n======= MENU =======")
    print("1. Deposit Money")
    print("2. Withdraw Money")
    print("3. View Balance")
    print("4. Change PIN")
    print("5. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        pin = int(input("Enter PIN: "))
        person1.deposit(pin)

    elif choice == "2":
        pin = int(input("Enter PIN: "))
        person1.withdrawal(pin)

    elif choice == "3":
        pin = int(input("Enter PIN: "))
        person1.check_balance(pin)

    elif choice == "4":
        person1.change_pin()

    elif choice=="5":
        print("exiting")
        break
    else:
        print("invalid choice")