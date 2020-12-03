#  Don't change the code below 
height = input("enter your height in m: ")
weight = input("enter your weight in kg: ")
#  Don't change the code above 

#Write your code below this line 

height_squared = int(height) ** 2
bmi = int(weight)/height_squared

print(int(bmi))
