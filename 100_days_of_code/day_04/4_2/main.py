import random

# Split string method
names_string = input("Give me everybody's names, separated by a comma. ")
names = names_string.split(", ")
# 🚨 Don't change the code above 👆

#Write your code below this line 👇

pick_name = random.randint(0, len(names)-1)

payer = names[pick_name]

print(f"{payer} is going to buy the meal today!")
