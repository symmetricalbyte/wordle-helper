from rich.console import Console
from rich.prompt import Prompt
from pathlib import Path
import random
import time
from functools import wraps

print = Console().print
_wordlist = Path("words5-from-OSPD4")
# _words = _wordlist.read_text().split("\n")
_words = _wordlist.read_text().splitlines()
_startingWords = ['salet', 'crate', 'crane', 'slate', 'adieu', 'least', 'start']
_startingWord = _startingWords[random.randint(0, len(_startingWords) - 1)]
_modifiedWords = []

def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        retval = func(*args, **kwargs)
        print(f"⌛Time taken to process: [bold green]{(time.time() - start_time)*1000:.4f} ms")
        return retval
    return inner

def correctPlace(_inputWordlist, _place, _letter):
    _localModifiedList = []
    for word in _inputWordlist:
        if word[_place] == _letter:
            _localModifiedList.append(word)
    return _localModifiedList

def wrongPlace(_inputWordlist, _place, _letter):
    _localModifiedList = []
    for word in _inputWordlist:
        if word[_place] != _letter and _letter in word:
            _localModifiedList.append(word)
    return _localModifiedList

def notInWord(_inputWordlist, _letter):
    _localModifiedList = []
    for word in _inputWordlist:
        if _letter not in word:
            _localModifiedList.append(word)
    return _localModifiedList

@timer
def checkUserInput(word: str, result: str):
    global _modifiedWords
    _source = _modifiedWords if _modifiedWords else _words
    result = (result or "").strip().upper()
    word = (word or "").strip().lower()
    _confirmedLetters = set()
    for i in range(5):
        if result[i] in ('G', 'Y'):
            _confirmedLetters.add(word[i])
    for i in range(5):
        if result[i] == 'G':
            _source = correctPlace(_source, i, word[i])
        elif result[i] == 'Y':
            _source = wrongPlace(_source, i, word[i])
        elif result[i] == 'X':
            if word[i] not in _confirmedLetters:
                _source = notInWord(_source, word[i])
    _modifiedWords = _source


def main():
    global _startingWord
    global _modifiedWords
    print('[bold yellow underline]- Wordle Helper -', justify='center')
    print('🤹This script takes input like [red bold]XXGYX[/red bold] where [italic green bold]X[/italic green bold] means it doesnt exist in the final word [italic green bold]G[/italic green bold] means its in the correct place [italic green bold]Y[/italic green bold] means its in the wrong place')
    print(f'😎 Lets start with the word : [bold underline white on black]{_startingWord}')
    wordleSolved: bool = False
    _word = _startingWord
    while not wordleSolved:
        userInput = Prompt.ask('Enter your result')
        checkUserInput(_word ,userInput)
        n = len(_modifiedWords)

        if n == 0:
            print('[bold red]⚠No possible words found, please check your inputs and try again.[/bold red]')
            break
        elif len(_modifiedWords) == 1:
            print(f'🎉The Word is : [bold yellow underline]{_modifiedWords[0]}')
            wordleSolved = True
            break
        if len(_modifiedWords) <= 20:
            print(f'💎List of Possible Answers: [bold yellow]{_modifiedWords}')
            _word = _modifiedWords[random.randint(0, len(_modifiedWords) - 1)]
            print(f'🔔Lets use the word [bold underline red]{_word}[/bold underline red] next')
        elif len(_modifiedWords) >= 20:
            print(f'🤔Possible Answers: [bold yellow]{len(_modifiedWords)}')
            _word = _modifiedWords[random.randint(0, 10)]
            print(f'🔔Lets use the word [bold underline red]{_word}[/bold underline red] next')
            continue
        else:
            _startingWord = _modifiedWords[0]
            print(f'✨[bold underline white on black]Next word to try : {_startingWord}')
            _modifiedWords = []


if __name__ == "__main__":
    main()

