# 🚨 Don't change the code below 👇
student_heights = input("Input a list of student heights ").split()
for n in range(0, len(student_heights)):
  student_heights[n] = int(student_heights[n])
# 🚨 Don't change the code above 👆


#Write your code below this row 👇

sum_heights = 0
num_heights = 0

for height in student_heights:
	sum_heights += height
	num_heights += 1

avg_height = round(sum_heights/num_heights)

print(avg_height)




