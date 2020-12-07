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

accepted_entries = [0,1,2]

if player_choice in accepted_entries:
  # Print what the player chose
  print(options[player_choice])

  # Print what the computer chose
  print(f"Computer chose: \n{options[computer_choice]}")
  if player_choice == computer_choice:
    print("It's a draw")
  elif (player_choice == 0 and computer_choice == 2) or (player_choice == 2 and computer_choice == 1) or (player_choice == 1 and computer_choice == 0):
    print("You win!")
  elif (computer_choice == 0 and player_choice == 2) or (computer_choice == 2 and player_choice == 1) or (computer_choice == 1 and player_choice == 0):
    print("You lose :(")
  else:
    print("Something has gone drastically wrong.")
else:
  print("You typed an invalid number, you lose!")




