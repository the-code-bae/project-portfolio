import art 
from replit import clear
#HINT: You can call clear() to clear the output in the console.
print(art.logo)

sealed_bids = {}

end_bidding = False

while end_bidding == False:

	name = input("What is your name?\n")
	bid  = input("What is your bid?: \n$")

	sealed_bids[name] = bid

	other_bidders = input("Are there any other bidders? Type 'yes' or 'no'. \n")

	if other_bidders == 'no':
		end_bidding = True
	else:
		clear()


print(sealed_bids)