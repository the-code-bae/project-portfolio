#If the bill was $150.00, split between 5 people, with 12% tip. 
#Each person should pay (150.00 / 5) * 1.12 = 33.6
#Format the result to 2 decimal places = 33.60
#Tip: You might need to do some research in Google to figure out how to do this.

print("Welcome to the tip calculator.")
total_bill = input("What was the total_bill? $ ")
percent_tip = input("What percentage tip would you like to give? 10, 12, or 15? ")
num_people = input("How many people to split the bill? ")

tot_amount_to_pay = float(total_bill) * (1+(float(percent_tip)/100))
split_per_person = round(tot_amount_to_pay/int(num_people),2)

final_msg = f"Each person should pay: $" +str(split_per_person)
print(final_msg)
