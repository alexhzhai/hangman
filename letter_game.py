# system functionality
import os
import random
import sys

fruits = [
    'apple',
    'banana',
    'orange',
    'coconut',
    'strawberry',
    'lime',
    'grapefruit',
    'lemon',
    'kumquat',
    'blueberry',
    'melon'
]

vegetables = [
    'asparagus',
    'brocolli',
    'spinach',
    'cauliflower',
    'arugula',
    'cabbage'
]

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
def draw(bad_guesses, good_guesses, secret_word):
    # clear the screen
    clear()

    # draw the strikes
    print('Strikes: {}/7'.format(len(bad_guesses)))
    print('')

    print('Bad guesses: ')
    for letter in bad_guesses:
        print(letter, end=' ')
    print('\n')

    for letter in secret_word:
        if letter in good_guesses:
            print(letter, end='')
        else:
            print('_', end='')

    print('')

# gets the user's guesses
def get_guess(bad_guesses, good_guesses):
    while True:
        guess = input("Guess a letter: ").lower()

        if len(guess) != 1:
            print("You can only guess a single letter!")
        elif guess in bad_guesses or guess in good_guesses:
            print("You've already guessed that letter!")
        elif not guess.isalpha():
            print("You can only guess letters!")
        else:
            return guess


def play(done):
    clear()
    print("1 - Fruits" + "\n" + "2 - Vegetables")
    category = int(input("Which category do you want to play with? "))
    if(category == 1):
        chosen_set = fruits
    elif(category == 2):
        chosen_set = vegetables
    secret_word = random.choice(chosen_set)
    bad_guesses = []
    good_guesses = []

    while True:
        draw(bad_guesses, good_guesses, secret_word)
        guess = get_guess(bad_guesses, good_guesses)

        if guess in secret_word:
            good_guesses.append(guess)
            found = True
            for letter in secret_word:
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
                print("The secret word was {}".format(secret_word))
                done = True

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
