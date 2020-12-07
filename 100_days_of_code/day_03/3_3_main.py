# 🚨 Don't change the code below 👇
year = int(input("Which year do you want to check? "))
# 🚨 Don't change the code above 👆

#Write your code below this line 👇

if year % 4 != 0:
	print("Not a leap year")
elif year % 100 != 0:
	print("Leap year")
elif year % 400 == 0:
	print("Leap year")
else:
	print("Not a leap year")

# Solution by teacher

# #  Don't change the code below 
# year = int(input("Which year do you want to check? "))
# #  Don't change the code above 

# #Refer to the flow chart here: https://bit.ly/36BjS2D

# if year % 4 == 0:
#   if year % 100 == 0:
#     if year % 400 == 0:
#       print("Leap year.")
#     else:
#       print("Not leap year.")
#   else:
#     print("Leap year.")
# else:
#   print("Not leap year.")




