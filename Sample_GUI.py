'''A GUI program demonstrating the use of Markov Bot Py'''

from breezypythongui import EasyFrame
from tkinter import HORIZONTAL
from tkinter import N,S,E,W

from MarkovBot import MarkovBot
import Formatter
import Tokenizer

class HonorsGUI(EasyFrame):
    """Contains the GUI"""

    def __init__(self):
        EasyFrame.__init__(self, title = 'Markov Bot GUI')

        #row 0
        self.addLabel('Build:', 0, 0)
        self.addLabel('', 0, 9)

        #row 1
        self.addLabel('Input file name:', 1, 0)
        self.input_file_name = self.addTextField('', 1, 1, columnspan = 8, width = 50, sticky = N+W)

        #row 2
        self.addLabel('Tokenizer select:', 2, 0)
        self.tokenizer_select = self.addRadiobuttonGroup(2, 1, columnspan = 7, orient = HORIZONTAL)
        self.tokenizer_select_basic = self.tokenizer_select.addRadiobutton('basic')
        self.tokenizer_select_group_aware = self.tokenizer_select.addRadiobutton('group aware')
        self.tokenizer_select.setSelectedButton(self.tokenizer_select_group_aware)

        #row 3
        self.build_button = self.addButton('Build', 3, 0, columnspan = 9, command = self.build)

        #row 4
        self.addLabel('Generate:', 4, 0)

        #row 5
        self.addLabel('Output select:', 5, 0)
        self.output_select = self.addRadiobuttonGroup(5, 1, columnspan = 2, orient = HORIZONTAL)
        self.output_select_console = self.output_select.addRadiobutton('console')
        self.output_select_file = self.output_select.addRadiobutton('file') 
        self.output_select.setSelectedButton(self.output_select_console)
        self.addLabel('Output file name:', 5, 3)
        self.output_file_name = self.addTextField('', 5, 4, columnspan = 5, width = 50, sticky = N+W)

        #row 6
        self.addLabel('Start string:', 6, 0)
        self.start_string = self.addTextField('', 6, 1, sticky = N+W)
        self.addLabel('Stop string:', 6, 2)
        self.stop_string = self.addTextField('.', 6, 3, sticky = N+W)
        self.addLabel('Limit:', 6, 4)
        self.limit = self.addIntegerField(15, 6, 5, sticky = N+W)

        #row 7
        self.addLabel('Repeat:', 7, 0)
        self.repeat = self.addIntegerField(3, 7, 1, sticky = N+W)
        self.repeat_select = self.addRadiobuttonGroup(7, 2, columnspan = 4, orient = HORIZONTAL)
        self.repeat_select_new_line = self.repeat_select.addRadiobutton('new line')
        self.repeat_select_append = self.repeat_select.addRadiobutton('append')
        self.repeat_select.setSelectedButton(self.repeat_select_new_line)

        #row 8
        self.generate_button = self.addButton('Generate', 8, 0, columnspan = 9, command = self.generate)

        #row 9
        self.console = self.addTextArea('', 9, 0, columnspan = 9)

        #row 10
        self.addLabel('By Jeffrey Matthews', 10, 0)

        #non GUI members
        self.mbot = MarkovBot()

    def build(self):
        fname = self.input_file_name.getText()
        if not fname:
            self.cprint('Error: file name is empty')
            return
        if fname.find('.') == -1:
            fname = fname + '.txt'
            
        try:
            text = Tokenizer.read_all(fname)
        except FileNotFoundError:
            self.cprint('Error: file not found')
            return

        if self.tokenizer_select.getSelectedButton() == self.tokenizer_select_group_aware:
            tokens = Tokenizer.group_aware(text)
        else:
            tokens = Tokenizer.basic(text)

        self.cprint('Building from ' + fname + '...')
        self.mbot.build(tokens)
        self.cprint('Successfully added ' + str(len(tokens)) + ' tokens')

    def cprint(self, s):
        self.console.appendText(s)
        self.console.appendText('\n')

    def generate(self):
        try:
            count = self.limit.getNumber()
        except ValueError:
            self.cprint('Error: limit field is not a number')
            return
        start = self.start_string.getText()
        if start: #if the start string is not empty make sure it is a key
            if start not in self.mbot.keys():
                self.cprint("Error: the start string '" + start + "' is not a key")
                return
        else: #if the start string is empty set it to none
            start = None
        stop = self.stop_string.getText()
        if not stop:
            stop = None
        try:
            repeat = self.repeat.getNumber()
        except ValueError:
            self.cprint('Error: repeat field is not a number')
            return
            
        if self.output_select.getSelectedButton() == self.output_select_file:
            fname = self.output_file_name.getText()
            if not fname:
                self.cprint('Error: output to file selected but no output file name given')
                return
            if fname.find('.') == -1:
                fname = fname + '.txt'
            file = open(fname, mode = 'w')

            self.cprint('Writing result to ' + fname)
            for i in range(repeat):
                tokens = self.mbot.walk(count, start, stop)
                result = Formatter.capped_sentences(tokens)
                if i != 0:
                    if self.repeat_select.getSelectedButton() == self.repeat_select_new_line:
                        file.write('\n')
                    else:
                        file.write(' ')
                file.write(result)
            file.close()
                        
        else:
            for i in range(repeat):
                tokens = self.mbot.walk(count, start, stop)
                result = Formatter.capped_sentences(tokens)
                if i != 0:
                    if self.repeat_select.getSelectedButton() == self.repeat_select_new_line:
                        self.console.appendText('\n')
                    else:
                        self.console.appendText(' ')
                self.console.appendText(result)
            self.console.appendText('\n')

HonorsGUI().mainloop()
