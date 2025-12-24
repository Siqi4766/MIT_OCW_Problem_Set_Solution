import random
import string

WORDLIST_FILENAME = 'words.txt'


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are lowercase
    letters_guessed: list (of letters), which letters have been guessed so far; assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed; False otherwise
    '''
    for i in secret_word:
      if i not in letters_guessed:
        return False
    return True    
    



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents which letters in secret_word have been guessed so far.
    '''
    result = ''
    for i in secret_word:
      if i in letters_guessed:
        result += i
      else:
        result += '_ '
    return result
      
  
def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not yet been guessed.
    '''
    not_guessed = ''
    alphabets = string.ascii_lowercase
    for i in alphabets:
      if i not in letters_guessed:
        not_guessed += i
    return not_guessed        
        
    
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.  
    
    Starts up an interactive game of Hangman. 
    '''
    print("Welcome to the game Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print('You have 3 warnings left.')
    guesses = 6
    warning = 3
    letters_guessed = []
    
    while guesses >= 1:
      print('------------')
      print(f'You have {guesses} guesses left.')
      print(f'Available letters: {get_available_letters(letters_guessed)}')
      user_guess = input("Please guess a letter:").lower()
      if str.lower(user_guess) not in string.ascii_lowercase:
        if warning >= 1:
          warning -= 1
          print(f"Oops! That is not a valid letter. You have {warning} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        else:
          guesses -= 1
          print(f"Oops! That is not a valid letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      elif user_guess not in letters_guessed:
        letters_guessed.append(user_guess)
        if user_guess in secret_word:
          print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
          if is_word_guessed(secret_word, letters_guessed):
            print('------------')
            print('Congratulations, you won!')
            unique_letters_in_secret_word = ''
            for i in secret_word:
              if i not in unique_letters_in_secret_word:
                unique_letters_in_secret_word += i
            score = guesses*len(unique_letters_in_secret_word)
            print(f'Your total score for this game is: {score}')
            break
        else:
          if user_guess in ['a', 'e', 'i', 'o', 'u']:
              guesses -= 2
          else:
              guesses -= 1
          print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
      elif user_guess in letters_guessed:
        if warning >= 1:
          warning -= 1
          print(f"Oops! You've already guessed that letter. You now have {warning} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        else:
          guesses -= 1
          print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      
    if is_word_guessed(secret_word, letters_guessed) == False:
      print('------------')
      print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    stripped_my_word = my_word.replace(" ", "")
    if len(stripped_my_word) != len(other_word):
      return False
    for i in range(len(stripped_my_word)):
      current_letter = stripped_my_word[i]
      other_letter = other_word[i]
      if current_letter != '_':
        if current_letter != other_letter:
          return False
      else: # current_letter = '_'
        if other_letter in stripped_my_word:
          return False
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    found_it = False
    for i in wordlist:
      if match_with_gaps(my_word, i):
        print(i, end = ' ')
        found_it = True
    if not found_it:
      print('No matches found')
    else:
      print()
      



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    print("Welcome to the game Hangman!")
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print('You have 3 warnings left.')
    guesses = 6
    warning = 3
    letters_guessed = []
    
    while guesses >= 1:
      print('------------')
      print(f'You have {guesses} guesses left.')
      print(f'Available letters: {get_available_letters(letters_guessed)}')
      user_guess = input("Please guess a letter:").lower()
      if str.lower(user_guess) not in string.ascii_lowercase:
        if user_guess == '*':
          print('Possible word matches are:')
          show_possible_matches(get_guessed_word(secret_word, letters_guessed))
        else:
          if warning >= 1:
            warning -= 1
            print(f"Oops! That is not a valid letter. You have {warning} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
          else:
            guesses -= 1
            print(f"Oops! That is not a valid letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      elif user_guess not in letters_guessed:
        letters_guessed.append(user_guess)
        if user_guess in secret_word:
          print(f"Good guess: {get_guessed_word(secret_word, letters_guessed)}")
          if is_word_guessed(secret_word, letters_guessed):
            print('------------')
            print('Congratulations, you won!')
            unique_letters_in_secret_word = ''
            for i in secret_word:
              if i not in unique_letters_in_secret_word:
                unique_letters_in_secret_word += i
            score = guesses*len(unique_letters_in_secret_word)
            print(f'Your total score for this game is: {score}')
            break
        else:
          if user_guess in ['a', 'e', 'i', 'o', 'u']:
              guesses -= 2
          else:
              guesses -= 1
          print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guessed)}')
      elif user_guess in letters_guessed:
        if warning >= 1:
          warning -= 1
          print(f"Oops! You've already guessed that letter. You now have {warning} warnings left: {get_guessed_word(secret_word, letters_guessed)}")
        else:
          guesses -= 1
          print(f"Oops! You've already guessed that letter. You have no warnings left: {get_guessed_word(secret_word, letters_guessed)}")
      
    if is_word_guessed(secret_word, letters_guessed) == False:
      print('------------')
      print(f"Sorry, you ran out of guesses. The word was {secret_word}.")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    # secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)
