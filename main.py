import sys
import random
import time
import threading

time_up = False

def division(no1, no2):
	if no2 > no1:
		no1, no2 = no2, no1
	return no1 // no2

def zero(no1, no2):
	if no1 > no2:
		no1, no2 = no2, no1
	first = (no1 + 9) // 10 * 10
	last = (no2 // 10) * 10
	if first > last:
		return 0
	return ((last - first) // 10) + 1

def countdown_timer(minutes):
	global time_up
	time.sleep(minutes * 60)
	time_up = True

print("Welcome to Secret Number")

try:
	no_of_players = int(input("Please enter the number of players.: "))
	if no_of_players <= 1:
		print("Please enter a positive whole number that is not 1.")
		sys.exit()
except ValueError:
	print("Please enter a positive whole number that is not 1.")
	sys.exit()

player_info = {}
assigned_numbers = set()

for i in range(1, no_of_players + 1):
	player_name = input(f"Enter in the name for player {i}: ")
	secret_number = random.randint(1, 100)
	while secret_number in assigned_numbers:
		secret_number = random.randint(1, 100)
	assigned_numbers.add(secret_number)
	player_info[player_name] = {
		"secret_number": secret_number,
		"points": 0
	}

timer_thread = threading.Thread(target=countdown_timer, args=(120,))
timer_thread.daemon = True
timer_thread.start()

while not time_up:
	print("Players:")
	for player_name in player_info:
		print(player_name)
	player_1 = input("Enter in the name of the first player.: ")
	if player_1 not in player_info:
		print("Please pick a valid player.")
		continue
	player_2 = input("Enter in the name of the second player.: ")
	if player_2 not in player_info:
		print("Please pick a valid player.")
		continue
	if player_1 == player_2:
		print("Please pick two different players.")
		continue
	print("""Please pick a card type to use.
(a) Addition
(b) Multiplication
(c) Division
(d) Zero""")
	card_option = input()
	if card_option == "a":
		result = player_info[player_1]["secret_number"] + player_info[player_2]["secret_number"]
		if result > 180:
			print("The result is between 180 and 199.")
			continue
		if result < 20:
			print("The result is between 3 and 20.")
			continue
		print(f"Result of {player_1} and {player_2} using the addition card: {result}.")
	elif card_option == "b":
		result = (player_info[player_1]["secret_number"] * player_info[player_2]["secret_number"]) % 10
		print(f"Result of {player_1} and {player_2} using the multiplication card: {result}.")
	elif card_option == "c":
		result = division(player_info[player_1]["secret_number"], player_info[player_2]["secret_number"])
		print(f"Result of {player_1} and {player_2} using the division card: {result}.")
	elif card_option == "d":
		result = zero(player_info[player_1]["secret_number"], player_info[player_2]["secret_number"])
		print(f"Result of {player_1} and {player_2} using the zero card: {result}.")
	else:
		print("Please pick a valid option.")

print("\nThe timer has reached zero.")
print("\nThe checking of answer sheets will now begin.")
print("Please type in nothing if there was no answer given.")

for player_name in player_info:
	print(f"Checking {player_name}")
	player_guessing = player_name
	for player_name in player_info:
		if player_name != player_guessing:
			guess = input(f"What is {player_guessing}'s guess for {player_name}'s number?")
			if guess == player_info[player_name]["secret_number"]:
				player_info[player_guessing]["points"] += 1
				player_info[player_name]["points"] -= 1
			else:
				if guess != "":
					player_info[player_guessing]["points"] -= 1
		else:
			guess = input(f"What is {player_guessing}'s guess for their number?")
			if guess == player_info[player_name]["secret_number"]:
				player_info[player_name]["points"] += 5
			else:
				if guess != "":
					player_info[player_name]["points"] -= 5
	if player_info[player_guessing]["points"] == no_of_players + 4:
		player_info[player_guessing]["points"] += 5

ranked_players = sorted(player_info.items(), key=lambda x: x[1]["points"], reverse=True)
for player_name, info in ranked_players:
	print(f"{player_name}: {info['points']} points")
