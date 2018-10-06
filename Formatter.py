'''Contains functions for formatting a list of tokens into human readable text

Intended for use with the output of MarkovBot.MarkovBot.walk()
'''

def _is_punctuation(c):
    '''Returns true if c is in ('!', ',', '.', ':', ';', '?')'''
    return c in ('!', ',', '.', ':', ';', '?')

def _is_send(c):
    '''Returns true is c is sentence ending puctuation.

    Specifically, returns true if c is in ('!', '.', ';', '?').
    '''
    
    return c in ('!', '.', ';', '?')

def capped_sentence_list(tokens):
    '''Formats the tokens into a list of capitalized sentences.

    Sentence ending puctuation is joined to the previous token.
    The first letter of the first token after the punctuation is capitalized.
    tokens -- a list of tokens to be formatted.
    return -- a list of strings where each string is a sentence
    '''

    if not tokens: #if tokens is empty
        return ['']
    
    result = [[]]

    for token in tokens:        
        if _is_punctuation(token):
            result[-1].append(token)
            if _is_send(token):
                result.append([])
        else:
            if result[-1]: #if the current list is not empty
                result[-1].append(' ')
                if token == 'i': #if the token is the letter i capitalize it
                    token = 'I'
                result[-1].append(token)
            else: #if it is empty
                result[-1].append(token[0].upper() + token[1:]) #capitalize the word              
                
    if not result[-1]: #if the last list is empty remove it
        result.pop()

    for i in range(len(result)):
        result[i] = ''.join(result[i])

    return result

def capped_sentences(tokens):
    '''Formats the tokens into capitalized sentences.

    Sentence ending puctuation is joined to the previous token.
    The first letter of the first token after the punctuation is capitalized.
    tokens -- a list of tokens to be formatted
    return -- a string containing the sentences
    '''

    return ' '.join(capped_sentence_list(tokens))

