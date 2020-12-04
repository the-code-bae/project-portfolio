#  Don't change the code below 
height = float(input("enter your height in m: "))
weight = float(input("enter your weight in kg: "))
#  Don't change the code above 

#Write your code below this line 

height_squared = height ** 2
bmi = round(weight/height_squared, 0)
# msg = f"Your BMI is {bmi}, you {weight_status}"

if bmi < 18.5:
	weight_status = "are overweight."
	print(f"Your BMI is {bmi}, you {weight_status}")
elif bmi < 25:
	weight_status = "have a normal weight."
	print(f"Your BMI is {bmi}, you {weight_status}")
elif bmi < 30:
	weight_status = "are slightly overweight."
	print(f"Your BMI is {bmi}, you {weight_status}")
elif bmi < 35:
	weight_status = "are obese."
	print(f"Your BMI is {bmi}, you {weight_status}")
else:
	weight_status = "are clinically obese."
	print(f"Your BMI is {bmi}, you {weight_status}")
	