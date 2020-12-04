# 🚨 Don't change the code below 👇
print("Welcome to the Love Calculator!")
name1 = input("What is your name? \n")
name2 = input("What is their name? \n")
# 🚨 Don't change the code above 👆

#Write your code below this line 👇

combined_name = name1.lower() + ' ' + name2.lower()

# print(combined_name)	

# Count "true" appearances
true_count = 0 

for i in "true":
	true_count += combined_name.count(i)

# print(f"True Count is: {true_count}")

# Count "love" appearances
love_count = 0 

for i in "love":
	love_count += combined_name.count(i)

# print(f"Love Count is: {love_count}")

final_score = int(str(true_count) + str(love_count))

# print(final_score)

# print(type(final_score))

if final_score < 10 or final_score > 90:
	print(f"Your score is {final_score}, you go together like coke and mentos.")
elif final_score >= 40 and final_score =< 50:
	print(f"Your score is {final_score}, you are alright together.")
else:
	print(f"Your score is {final_score}.")
