import art 
from replit import clear
#HINT: You can call clear() to clear the output in the console.
print(art.logo)

sealed_bids = {}

end_bidding = False

while end_bidding == False:

	name = input("What is your name?\n")
	bid  = int(input("What is your bid?: \n$"))

	sealed_bids[name] = bid

	other_bidders = input("Are there any other bidders? Type 'yes' or 'no'. \n")

	if other_bidders == 'no':
		end_bidding = True
	else:
		clear()

# Find highest bid
highest_bid = max(sealed_bids.values())

# Find highest bidder based on their bid
for key in sealed_bids:
	if sealed_bids[key] == highest_bid:
		highest_bidder = key

# Print winner
print(f"The winner of the bid is {highest_bidder} with a bid of ${highest_bid}.")
