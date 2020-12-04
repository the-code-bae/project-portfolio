#  Don't change the code below 
print("Welcome to Python Pizza Deliveries!")
size = input("What size pizza do you want? S, M, or L ")
add_pepperoni = input("Do you want pepperoni? Y or N ")
extra_cheese = input("Do you want extra cheese? Y or N ")
#  Don't change the code above 

#Write your code below this line 
bill = 0
msg = print(f"Your final bill is: ${bill}")

if size == "S":
	bill = 15
	if add_pepperoni == "Y":
		bill += 2
	else:
		msg
		if extra_cheese = "Y":
			bill += 1
			msg
elif size == "M":
	bill = 20
	if add_pepperoni == "Y":
		bill += 3
	else:
		msg
		if extra_cheese = "Y":
			bill += 1
			msg
elif size == "L":
	bill = 25 
	if add_pepperoni == "Y":
		bill += 3
	else:
		msg
		if extra_cheese = "Y":
			bill += 1
			msg

# if extra_cheese == "Y":
# 	bill = 1
# 	if size == "S":
# 		bill += 15
# 		if add_pepperoni == "Y":
# 			bill =+ 2
# 			print(f"Your final bill is: ${bill}")
# 	elif size == "M":
# 		bill += 20
# 	else size == "L":
# 		bill += 25



