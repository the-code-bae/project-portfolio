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


# print(sealed_bids)
# print(max(sealed_bids.values()))

highest_bid = max(sealed_bids.values())

for key in sealed_bids:
	if sealed_bids[key] == highest_bid:
		highest_bidder = key
# highest_bidder = 

# print(highest_bidder + ":" + highest_bid)

# print("The winner of the bid is James with a bid of $142.")
