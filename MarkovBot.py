'''Contains the MarkovBot class'''

from collections import Counter
import random

class MarkovBot(object):
    '''A class representing a markov chain of strings.

    Data members:
    self.__data

    Data is held in an adjacency list represented by a dictionary that maps strings to collections.Counter objects.
    The counter holds counts of the number of times specific strings have followed the dictionary string.
    That is, self.__data[s1][s2] contains a count of the number of times the token s2 has followed s1.
    '''

    def __init__(self, tokens = None):
        '''Initializes the MarkovBot. If an optional list of tokens is provided then build(tokens) is immediately called.'''
        
        self.__data = {}
        if tokens: #if tokens is not None or an empty list
            self.build(tokens)

    def __str__(self):
        '''Returns a string representation of the MarkovObject.'''

        if self.empty():
            return 'MarkovBot object: empty'
        
        verts = sorted(self.__data.keys())
        for i in range(len(verts)):
            s = "'" + verts[i] + "'\t{"
            counts = sorted(self.__data[verts[i]].items())
            counts = list(map(lambda t : "'" + t[0] + "': " + str(t[1]), counts))
            s += ', '.join(counts) + '}'
            verts[i] = s
        return 'MarkovBot object:\n' + '\n'.join(verts)

    
    def build(self, tokens):
        '''Accepts a list of tokens and adds them to the MarkovBot.

        Counts the number of times each token is immediately followed by another.
        The last token is added to the dictionary but is not considered to have any token following it.
        Calling build repeatedly will not cause the first element of the second call to be considered following the last element of the first.
        To acheive this behavior combine the lists of tokens.
        Tokens are case sensitive. Using all lowercase tokens then formatting afterwards is recommended.
        Passing anything other than a list or tuple of strings causes undefined behavior.
        tokens -- a list of stings representing the tokens. Use of a function from the Tokenizer module is recommended.
        '''
        
        if len(tokens) == 0:
            return
        elif len(tokens) == 1:
            if tokens[0] not in self.__data:
                self.__data[tokens[0]] = Counter()
            return

        #For each token except the last
        for i in range(len(tokens) - 1):
            if tokens[i] not in self.__data: #if the token is not already in the dict add it
                self.__data[tokens[i]] = Counter()
            self.__data[tokens[i]][tokens[i + 1]] += 1 #Increment the counter
        #Add the last item if it doesn't already exist
        if tokens[-1] not in self.__data:
            self.__data[tokens[-1]] = Counter()

    def empty(self):
        '''Returns true if this objects dictionary is empty.'''
        return not self.__data #an empty dict evaluates to false

    def keys(self):
        '''Returns a list of all tokens that have been encountered.'''

        return list(self.__data.keys())


    def walk(self, count, start = None, stop = None):
        '''Performs a weighted random walk of the graph stored by the MarkovBot.

        First chooses a starting node with an unwieghted choice of all encountered tokens.
        If start is not None it uses the value provided instead.
        From there the next node is chosen by a weighted choice of all nodes that have followed the last chosen node.
        The weights are the counts of the number of times the node has been followed.
        This is repeated until the number of nodes exceeds count, or until a token matching stop is encountered.
        The walk is returned as a list of strings.
        count -- the maximum number of nodes to return. A large number is recommended if you want to generate until stop is reached.
        start -- the string to start the walk at. Must be a token that has been encountered by the MarkovBot during building. Defaults to None.
        stop -- the string to stop at if it is encountered during the walk.
        return -- the list of strings that were encountered during the walk.
        '''
        
        result = []
        if self.empty():
            return result
        
        if start:
            result.append(start)
        else:
            result.append(random.choice(self.keys())) #choose a random starting point
        
        for i in range(count):
            if result[-1] == stop: #if the list ends with the stop string exit
                break
            
            k = list(self.__data[result[-1]].keys()) #keys
            w = list(self.__data[result[-1]].values()) #weights
            if not w: #if we have reached a vertex with no outgoing edges stop
                break
            result.append(random.choices(k, weights = w)[0])
        
        return result
