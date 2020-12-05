import random 

rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

# Create list of options to print
options = [rock, paper, scissors]

# Store player's choice
p_choice = input("What do you choose? Type 0 for Rock, 1 for Paper or 2 for Scissors\n")
player_choice = int(p_choice)

# Create random computer choice 
computer_choice = random.randint(0,2)

# Print what the player chose
if player_choice == 0:
  print(options[player_choice])
elif player_choice == 1:
  print(options[player_choice])
elif player_choice == 2:
  print(options[player_choice])
else:
  "Try again, your entry is not valid."

# Print what the computer chose
if computer_choice == 0:
  print(f"Computer chose: \n{options[computer_choice]}")
elif computer_choice == 1:
  print(f"Computer chose: \n{options[computer_choice]}")
elif computer_choice == 2:
  print(f"Computer chose: \n{options[computer_choice]}")
else:
  "Something went wrong here."

# So who won?
if player_choice == computer_choice:
  print("It's a draw")
elif (player_choice == 0 and computer_choice == 2) or (player_choice == 2 and computer_choice == 1) or (player_choice == 1 and computer_choice == 0):
  print("You win!")
elif (computer_choice == 0 and player_choice == 2) or (computer_choice == 2 and player_choice == 1) or (computer_choice == 1 and player_choice == 0):
  print("You lose :(")
else:
  "Something has gone drastically wrong."





