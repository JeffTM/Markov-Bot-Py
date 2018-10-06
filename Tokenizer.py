'''Contains functions for tokenizing string input.

Ouputs are intended for use with MarkovBot.MarkovBot.build()
'''

#private functions --------------------------------

#Dictionary of opening characters and their closers. Should not be modified
_groupchars = {'(': ')', '[': ']', '<': '>', '{': '}'}
        
def _closer(c):
    '''Returns the closing tag equivalent of c.

    c -- the character to find a closing tag for.
    return -- the closing character or None if c is not an opening char character.
    '''
    return _groupchars.get(c, None)
        
def _find_closing_char(s, c, start = 0):
    '''Returns the index of the closing character of c in src starting at start.

    s -- the string to search in.
    c -- the opening character.
    start -- the index to start the search.
    return -- the index of the closing tag as an integer. -1 if not found.
    '''

    if start >= len(s):
        return -1
    c = _closer(c)
    return s.find(c, start)

def _find_stopper(s, start = 0):
    '''Returns the index of the first character in s for which is_stopper returns true.

    s -- the string to search in.
    start -- the index to start the search.
    return -- the index of the first stopper in s[start:]. -1 if end of string reached.
    '''
    
    while start < len(s):
        if _is_stopper(s[start]):
            return start
        start += 1
    return -1
        
def _is_opening_char(c):
    '''Returns true if c is in ('(', '[', '<', '{')'''
    return c in _groupchars

def _is_punctuation(c):
    '''Returns true if c is in ('!', ',', '.', ':', ';', '?')'''
    return c in ('!', ',', '.', ':', ';', '?')

def _is_stopper(c):
    '''Returns true if c is a stopping character.

    C is a stopping character if is_punctuation(c) or c.isspace() returns true.
    '''

    return c.isspace() or _is_punctuation(c)

#public functions --------------------------------

def read_all(txtfile):
    '''Reads the entirety of a text file and returns it as a string.

    txtfile -- the path of the text file.
    return -- a string containing the entirety of the file.
    '''

    f = open(txtfile, 'r')
    s = f.read()
    f.close()
    return s
    
def basic(s):
    '''Minimal tokenizer. Returns s.lower().split()'''
    return s.lower().split()

def group_aware(s):
    '''Group aware tokenizer.

    Keeps text between (), [], <>, {} as a single token.
    Also keeps punctuation and groups of the same punctuation as a token.
    For example: 'Hello World...' would be tokenized as [hello, world, ...].
    s -- the string to be tokenized.
    return -- a list of tokens.
    '''
    
    #Preprocessing
    s = s.strip().lower()
    if (len(s) == 0):
        return []

    i = 0 #Current character
    tokens = [] #List of tokens
    while i < len(s):
        #Advance past any whitespace characters
        while i < len(s) and s[i].isspace():
            i += 1
        if i == len(s):
            break

        #If src[i] is an opening char add the substring contained between i and its closing char
        if _is_opening_char(s[i]):
            close_index = _find_closing_char(s, s[i], i + 1)
            if close_index == -1:
                tokens.append(s[i:])
                break
            close_index += 1 #Index 1 after the closing char
            tokens.append(s[i:close_index])
            i = close_index
        #Else if scr[i] is a punctuation character add it and any following equal characters
        elif _is_punctuation(s[i]):
            stop_index = i + 1
            while stop_index < len(s) and s[stop_index] == s[i]:
                stop_index += 1
            if stop_index == len(s):
                tokens.append(s[i:])
                break
            tokens.append(s[i:stop_index])
            i = stop_index
        #else the token is the substring from i up to but not including the next stop character
        else:
           stopper_index = _find_stopper(s, i)
           if stopper_index == -1:
               tokens.append(s[i:])
               break
           tokens.append(s[i:stopper_index])
           i = stopper_index
           
    return tokens
