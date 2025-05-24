import sys
import random
import time
import threading
import queue

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

def get_input(prompt, timeout=1):
    q = queue.Queue()

    def input_thread():
        try:
            q.put(input(prompt))
        except EOFError:
            q.put("")
    
    t = threading.Thread(target=input_thread)
    t.daemon = True
    t.start()

    while not time_up:
        try:
            return q.get(timeout=timeout)
        except queue.Empty:
            continue
    return ""

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
		"points": 0,
		"piece_change": 0
	}

timer_thread = threading.Thread(target=countdown_timer, args=(120,))
timer_thread.daemon = True
timer_thread.start()

while not time_up:
	print("Players:")
	for player_name in player_info:
		print(player_name)
	player_1 = get_input("Enter in the name of the first player: ")
	if time_up:
		break
	if player_1 not in player_info:
		print("Please pick a valid player.")
		continue

	player_2 = get_input("Enter in the name of the second player: ")
	if time_up:
		break
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
	card_option = get_input("> ")
	if time_up:
		break
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
			guess = input(f"What is {player_guessing}'s guess for their number? ")
			if guess == player_info[player_name]["secret_number"]:
				player_info[player_name]["points"] += 5
			else:
				if guess != "":
					player_info[player_name]["points"] -= 5
	if player_info[player_guessing]["points"] == no_of_players + 4:
		player_info[player_guessing]["points"] += 5

points = {info["points"] for info in player_info.values()}
all_same = len(points) == 1

if all_same:
    print("All players must return 1 piece each, as they all have the same number of points.")

ranked_players = sorted(player_info.items(), key=lambda x: x[1]["points"], reverse=True)
min_points = min(info["points"] for info in player_info.values())
lowest_players = [name for name, info in player_info.items() if info["points"] == min_points]

if len(lowest_players) > 1:
	print("Players:")
	for player_name in player_info:
		print(player_name)

	player_picked_last = input(f"Who did {ranked_players[0][0]} pick to require returning 3 pieces? ")
	while player_picked_last not in player_info:
		print("Please pick a valid player.")
		player_picked_last = input(f"Who did {ranked_players[0][0]} pick to require returning 3 pieces? ")

for player_name, info in ranked_players:
	if info["points"] >= 16:
		info["piece_change"] += 3
	elif info["points"] >= 11:
		info["piece_change"] += 2
	elif info["points"] >= 6:
		info["piece_change"] += 1
	elif player_name == lowest_players:
		info["piece_change"] -= 3
	elif info["points"] < 0:
		info["piece_change"] -= 2
	else:
		info["piece_change"] -= 1

	if info["piece_change"] < 0:
		print(f"{player_name}: {info['points']} points (Return {abs(info['piece_change'])} pieces)")
	if info["piece_change"] == 0:
		print(f"{player_name}: {info['points']} points (No pieces given)")
	if info["piece_change"] > 0:
		print(f"{player_name}: {info['points']} points (Receive {info['piece_change']})")
