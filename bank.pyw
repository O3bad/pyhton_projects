class E_Mail:
  def __init__(self):
    self.E_Mail = None
    self.password = None
    self.name = None
    self.last_name = None
    self.Visa_id = None

  def set_info(self):
    while True:
      self.Visa_id = input("Enter your National ID (Must be 16 digits): ")
      if len(self.Visa_id) == 16 and self.Visa_id.isdigit():  # Check for 16 digits and all numbers
        break
      else:
        print("Invalid National ID. Please enter 16 digits.")

    print("Enter your E-Mail:")
    self.E_Mail = input()
    print("Enter your Password:")
    self.password = input()

  def new_client(self):
    print("Enter your First Name:")
    self.name = input()
    print("Enter your Last Name:")
    self.last_name = input()
    self.set_info()
    print(f"Welcome to our bank MR {self.name} {self.last_name}")
    print(f"Your National ID: {self.Visa_id}")

def main():
  print("Welcome to our bank.")
  choice = 1
  balance = 0
  while choice:
    print("\n1) New client\n2) Old client")
    choice = int(input())
    if choice == 1:
      client = E_Mail()
      client.new_client()
      password = input("Enter your Bank password: ")
      print(f"Your Bank password is {password}")
      confirm = 1
      while confirm:
        print("\n1) Confirm.\n2) Edit.")
        confirm = int(input())
        if confirm == 1:
          print(f"Your Bank password is: {password}")
          break
        elif confirm == 2:
          password = input("Enter your Bank password: ")
    elif choice == 2:
      email = input("Enter your National ID: ")
      password = input("Enter your Password: ")
      if client.password == password:  # Assuming there's only one client object (`client`)
        choice = 0  # Exit loop for old client
      else:
        print("Wrong Bank Password.\nTry again.")
        while True:  # Infinite loop until correct password entered
          email = input("Enter your National ID: ")
          password = input("Enter your Password: ")
          if client.password == password:
            choice = 0  # Exit loop for old client
            break  # Exit inner loop

  while True:
    print("\n\nWhat operation do you want?")
    print("1) Deposit\n2) Withdraw\n3) Exit")
    option = int(input())
    if option == 1:
      print(f"Your balance = {balance}")
      while True:
        deposit = float(input("What is the amount you want to deposit? "))
        if deposit > 0:  # Check for positive deposit amount
          balance += deposit
          print(f"Your new balance = {balance}")
          break
        else:
          print("Deposit amount cannot be negative. Please enter a positive value.")
    elif option == 2:
      print(f"Your balance = {balance}")
      while True:
        withdraw = float(input("What is the amount you want to withdraw? "))
        if withdraw > 0 and withdraw <= balance:  # Check for positive and sufficient withdraw amount
          balance -= withdraw
          print(f"Your new balance = {balance}")
          break
        elif withdraw <= 0:
          print("Withdrawal amount cannot be negative. Please enter a positive value.")
        else:
          print("Insufficient funds. You cannot withdraw more than your balance.")
    elif option == 3:
      break

if __name__ == "__main__":
  main()
