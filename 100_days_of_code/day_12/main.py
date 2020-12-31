from random import randint

EASY_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5

answer = randint(1,100)
print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100")

def check_answer(guess, answer):
	if guess > answer:
		print ("Too high.")
	elif guess < answer:
		print("Too low.")
	else:
		print(f"You've got it! The answer was {answer}")

def set_difficulty():
	level = input("Choose a difficulty. Type 'easy' or 'hard': ")
	if level == 'easy':
		return EASY_LEVEL_TURNS
	else:
		return HARD_LEVEL_TURNS

turns = set_difficulty()


guess = int(input("Make a guess: "))
check_answer(guess, answer)

print(f"You have {turns} attempts remaining to guess the number.")
print(f"The correct answer is {answer}")
