# system functionality
import os
import random
import sys

# lists for each game category that stores possible keywords
# fruits and vegetables from top 20 sold in us (used https://goo.gl/Cnw6nd)
fruits = []
vegetables = []
candies = []

# initialize the game by reading file line by line (used https://goo.gl/d8egZk)
def initialize():
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
def draw(bad_guesses, good_guesses, secret_word, chosen_set):
    # clear the screen
    clear()

    # print category and draw the strikes
    print("Category: " + chosen_set + " | " + "Strikes: {}/7".format(len(bad_guesses)))
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


def play(done):
    clear()
    initialize()

    print("1 - Fruits" + "\n" + "2 - Vegetables" + "\n" + "3 - Candies")
    category = int(input("Which category do you want to play with? "))
    if(category == 1):
        chosen_set = fruits
        chosen_name = "Fruits"
    elif(category == 2):
        chosen_set = vegetables
        chosen_name = "Vegetables"
    elif(category == 3):
        chosen_set = candies
        chosen_name = "Candies"
    secret_word = ""
    if " " in secret_word:
        secret_word = random.choice(chosen_set)
    else:
        secret_word = random.choice(chosen_set)[:-1]
    bad_guesses = []
    good_guesses = []

    # game manager
    while True:
        draw(bad_guesses, good_guesses, secret_word, chosen_name)
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
            if len(bad_guesses) == 7:
                draw(bad_guesses, good_guesses, secret_word)
                print("You lost!")
                print("The secret word was {}.".format(secret_word))
                done = True

        # game over --> play again
        if done:
            play_again = input("Play again? Y/N ")
            if play_again.lower() != 'n':
                return play(done=False)
            else:
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
print('Welcome to Letter Guess!')

done = False

while True:
    clear()
    welcome()
    play(done)
