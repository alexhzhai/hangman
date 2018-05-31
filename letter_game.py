# system functionality
import os
import random
import sys
import time

# lists for each game category that stores possible keywords
# fruits and vegetables from top 20 sold in us (used https://goo.gl/Cnw6nd)
fruits = []
vegetables = []
candies = []

# initialize the game by reading file line by line (used https://goo.gl/d8egZk)
def initialize():
    #"r" in open --> open for reading, default
    f1=open(os.path.join("categories", "fruits.txt"), "r")
    f1 = f1.readlines()
    for x in f1:
        fruits.append(x)
    f2 = open(os.path.join("categories", "vegetables.txt"), "r")
    f2 = f2.readlines()
    for x in f2:
        vegetables.append(x)
    f3=open(os.path.join("categories", "candies.txt"), "r")
    f3 = f3.readlines()
    for x in f3:
        candies.append(x)

# clears the screen before playing
def clear():
    # windows clear window
    if os.name == 'nt':
        # call system level utility cls
        os.system('cls')
    # mac clear window
    else:
        os.system('clear')

# 'draw' game interface
def draw(bad_guesses, good_guesses, secret_word, chosen_set, chosen_level, level_name, hints_on):
    # clear the screen
    clear()

    # print category and draw the strikes
    if hints_on:
        print("Category: " + chosen_set + " | " + "Level: " + level_name + " | "
            + "Strikes: {}/{}".format(len(bad_guesses), chosen_level) + " | " + "Hints: ON")
    else:
        print("Category: " + chosen_set + " | " + "Level: " + level_name + " | "
            + "Strikes: {}/{}".format(len(bad_guesses), chosen_level) + " | " + "Hints: OFF")
    print('')

    print('Bad guesses: ')
    for letter in bad_guesses:
        print(letter, end=' ')
    print('\n')

    # draws the line for the word
    for letter in secret_word:
        if letter in good_guesses:
            print(letter, end='')
        elif letter == " ":
            # checks if letter is a space (i.e: kit kat, swedish fish, sweet potatoes)
            print(' ', end ='')
        else:
            print('_', end='')
    print('')

# gets the user's guesses
def get_guess(bad_guesses, good_guesses):
    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1:
            # make sure user does not guess multiple letters
            print("You can only guess a single letter!")
        elif guess in bad_guesses or guess in good_guesses:
            # make sure user does not guess the same letter multiple times
            print("You've already guessed that letter!")
        elif not guess.isalpha():
            # isalpha checks for alphanumeric
            print("You can only guess letters!")
        else:
            return guess

# prompts user for level/difficulty for game
def choose_dificulty():
    try:
        lev = int(input("What level do you want to play? "))
        if (lev == 1 or lev == 2 or lev == 3):
            return lev
        else:
            raise ValueError()
    except (ValueError):
        input("Not a valid input. Press enter to continue.")
        choose_dificulty()

def display_hint(chosen_name, line_number):
    myLine = ""
    with open("{}_hints.txt".format(chosen_name.lower())) as fp:
        for i, line in enumerate(fp):
            if i == (line_number-1):
                myLine = line
    myLine = myLine[3:]
    myLine = myLine.replace('"', '')
    myLine = myLine.split(" / ")
    return myLine

def play(done):
    clear()
    initialize()

    print("1 - Fruits" + "\n" + "2 - Vegetables" + "\n" + "3 - Candies")
    try:
        category = int(input("Which category do you want to play with? "))
        if (category != 1 and category != 2 and category != 3):
            raise ValueError()
    except (ValueError):
        input("Not a valid input. Press enter to continue.")
        play(done)
    if(category == 1):
        chosen_set = fruits
        chosen_name = "Fruits"
    elif(category == 2):
        chosen_set = vegetables
        chosen_name = "Vegetables"
    elif(category == 3):
        chosen_set = candies
        chosen_name = "Candies"

    print("1 - Easy (15 strikes, hints)" + "\n" + "2 - Medium (12 strikes, hints)" + "\n" + "3 - Hard (10 strikes, no hints)")
    level = choose_dificulty()
    # chosen level helps with number of alloted strikes and level_name is displayed
    chosen_level = 0
    level_name= ""
    hints_on = False
    if(level == 1):
        chosen_level = 15
        level_name = "Easy"
        hints_on = True
    elif(level == 2):
        chosen_level = 12
        level_name = "Medium"
        hints_on = True
    elif(level == 3):
        chosen_level = 7
        level_name = "Hard"

    secret_word = ""
    if " " in secret_word:
        non_edit = random.choice(chosen_set)[:-1]
        # non_edit = kit kat 13, secret_word = kit kat, line_number = 13
        secret_word = non_edit[:-3]
        line_number = int(non_edit[-2:])
    else:
        non_edit = random.choice(chosen_set)
        secret_word = non_edit[:-4]
        line_number = int(non_edit[-3:])
    bad_guesses = []
    good_guesses = []

    hint_number = 0
    # game manager
    while True:
        draw(bad_guesses, good_guesses, secret_word, chosen_name, chosen_level, level_name, hints_on)
        guess = get_guess(bad_guesses, good_guesses)

        actual_word = secret_word.replace(" ", "")
        if guess in actual_word:
            good_guesses.append(guess)
            found = True
            for letter in actual_word:
                if letter not in good_guesses:
                    found = False
            if found:
                print("You win!")
                print("The secret word was {}".format(secret_word))
                done = True
        else:
            bad_guesses.append(guess)
            numb_bad = len(bad_guesses)
            hints = display_hint(chosen_name, line_number)
            if numb_bad == chosen_level-2:
                hint = hints[0]
                hint = hint.replace('"', '')
                print("Hint: {}".format(hint))
                time.sleep(2)
            elif numb_bad == chosen_level-1:
                hint = hints[1]
                hint = hint.replace('"', '')
                print("Hint: {}".format(hint))
                time.sleep(2)

            # number of bad guesses equals chosen level alloted guesses
            if numb_bad == chosen_level:
                draw(bad_guesses, good_guesses, secret_word, chosen_name, chosen_level, level_name, hints_on)
                print("You lost!")
                print("The secret word was {}.".format(secret_word))
                done = True

        # game over --> play again
        if done:
            play_again = input("Play again? Y/N ")
            if play_again.lower() != 'n':
                return play(done=False)
            else:
                print("Thanks for playing!")
                sys.exit()

# prompts user to start game
def welcome():
    start = input("Press enter/return to start or Q to quit ").lower()
    if start == 'q':
        print("Bye!")
        sys.exit()
    else:
        return True

# welcome message
print('Welcome to Hangman!')

done = False

while True:
    clear()
    welcome()
    play(done)
