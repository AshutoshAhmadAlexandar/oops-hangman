from .exceptions import *
import random


class GuessAttempt(object):
    def __init__(self,character,hit=None,miss=None):
        if hit and miss:
            raise InvalidGuessAttempt('Both hit and miss cant be true')
        
        self.character = character
        self.hit = hit
        self.miss = miss
    
    def is_miss(self):
        if self.miss:
            return True
        return False
    
    def is_hit(self):
        if self.hit:
            return True
        return False


class GuessWord(object):
    def __init__(self,word):
        if not word:
            raise InvalidWordException('Give a word')
        self.answer = word
        self.masked = '*' * len(word)
    
    def perform_attempt(self,character):
        if len(character) > 1:
            raise InvalidGuessedLetterException("Please enter only 1 character to guess")
        
        if character.lower() not in self.answer.lower():
            return GuessAttempt(character,miss = True)
        
        new_answer =''
        for answer_char, masked_char in zip(self.answer.lower(),self.masked.lower()):
            if character.lower() == answer_char:
                new_answer += answer_char
            else:
                new_answer += masked_char
        self.masked = new_answer
        return GuessAttempt(character,hit = True)
    


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, list_of_words=None, number_of_guesses=5):
        if not list_of_words:
            list_of_words = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        #self.word = GuessWord(self.select_random_word(list_of_words))
        self.previous_guesses = []
        #GuessWord(self.word)
        self.list_of_words = list_of_words
        random_word = self.select_random_word(list_of_words)
        self.word = GuessWord(random_word)
       
    @classmethod
    def select_random_word(self, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException('Give a list of words')
        return random.choice(list_of_words)
    
    
    def is_won(self):
        return self.word.answer == self.word.masked
    
    def is_lost(self):
        return self.remaining_misses == 0
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
    
    def guess(self,character):
        if character.lower() in self.previous_guesses:
            raise InvalidGuessedLetterException('This word is used already')
        
        if self.is_finished():
            raise GameFinishedException('Game is over')
        
        self.previous_guesses.append(character.lower())
        current_attempt = self.word.perform_attempt(character.lower())
        if current_attempt.is_miss():
            self.remaining_misses -= 1
        
        if self.is_won():
            raise GameWonException('Game already won')
        
        if self.is_lost():
            raise GameLostException('Game is lost')
        
        return current_attempt
    

            
