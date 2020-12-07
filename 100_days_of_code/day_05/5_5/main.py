#Password Generator Project
import random
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

print("Welcome to the PyPassword Generator!")
nr_letters= int(input("How many letters would you like in your password?\n")) 
nr_symbols = int(input(f"How many symbols would you like?\n"))
nr_numbers = int(input(f"How many numbers would you like?\n"))

#Eazy Level - Order not randomised:
#e.g. 4 letter, 2 symbol, 2 number = JduE&!91

# Create random list of numbers to each component of the password
random_letters = random.sample(range(0,nr_letters),nr_letters)
random_symbols = random.sample(range(0,nr_symbols),nr_symbols)
random_numbers = random.sample(range(0,nr_numbers),nr_numbers)

print(random_letters)
print(len(random_letters))

# print(random_symbols)
# print(len(random_symbols))

# print(random_numbers)
# print(len(random_numbers))

letter_section = ''

for num in random_letters:
	letter_section += letters[num]

symbol_section = ''

for num in random_symbols:
	symbol_section += symbols[num]

number_section = ''

for num in random_numbers:
	number_section += numbers[num]	


final_output = letter_section + symbol_section + number_section

print(final_output)


#Hard Level - Order of characters randomised:
#e.g. 4 letter, 2 symbol, 2 number = g^2jk8&P

randomise_final = random.sample(range(0, len(final_output)),len(final_output))

hard_final_output = ''

for num in randomise_final:
	hard_final_output += final_output[num]

print(hard_final_output)
