from __future__ import print_function
from collections import defaultdict
import functools
import re
import sublime
import sublime_plugin

bases = {'binary' : 2, 'octal' : 8, 'decimal' : 10, 'hexadecimal' : 16}

################################################################################
# helpers

def logInputAndOutput(func):
    '''decorator to help with debugging'''
    def function_wrapper(*args, **kwargs):
        print("Before calling " + func.__name__ + ":")
        for arg in args:
            print("\t", type(arg), "|", arg)
        for arg in kwargs:
            print("\t", type(arg), "|", arg)
        output = func(*args, **kwargs)
        print("After calling " + func.__name__ + ":", type(output), "|", output)
        return output
    return function_wrapper

def compose(functions):
    '''apply functions in order from left to right'''
    return lambda x: functools.reduce(lambda a, f: f(a), functions, x)

################################################################################
# functions to modify keys

def naturalize(line):
    '''http://nedbatchelder.com/blog/200712/human_sorting.html'''
    conversion = lambda e: int(e) if e.isdigit() else e
    return [conversion(g) for g in re.split('([0-9]+)', line)]

def ignorePatterns(toIgnore, caseSensitive):
    '''remove a string or regular expression from the line'''
    def regexFunc(line, pattern):
        return re.sub(pattern, "", line)
    return lambda line: functools.reduce(regexFunc, toIgnore, line)

################################################################################

def putEndLines(arr):
    if int(sublime.version()) < 3000:
        arr = [unicode(x.encode('utf-8'), 'utf-8') + '\n' for x in arr]
    else:
        arr = [str(x.encode('utf-8'), encoding='utf-8') + '\n' for x in arr]

    arr[-1] = arr[-1][:-1]
    return arr

def writeToView(self, region, conteneur):
    if len(conteneur) != 0:
        if self.estSelect:
            self.view.replace(self.edit, region, ''.join(putEndLines(conteneur)))
        else:
            self.view.erase(self.edit, sublime.Region(0, self.view.size()))
            self.view.insert(self.edit, 0, ''.join(putEndLines(conteneur)))
    else:
        print("SortBy error: No string found !")

class SortingObj(object):
    def __init__(self, line, number, base):
        self.line = str(line).strip()
        self.number = number
        self.base = base
    def getLine(self):
        return self.line
    def getNumber(self):
        if self.number == 0:
            return 0
        return int(self.number, bases[self.base])

################################################################################
# sort command

class SrtbyliCommand(sublime_plugin.TextCommand):

    def __init__(self, cmd):
        super().__init__(cmd)
        self.estSelect = None
        self.edit = None
        self.settings = sublime.load_settings("SortBy.sublime-settings")

    def sortNumbers(self, region, contenue, sort): #Sort numbers with letters
        conteneur = []
        obj = []

        for line in contenue:
            number = ''
            if sort == 'decimal':
                number = re.findall(r'[+-]?\d+(?:\.\d+)?', line)
            if sort == 'octal':
                number = re.findall(r'[0-7]+', line)
            if sort == 'hexadecimal':
                number = re.findall(r'(?:0[xX])?[0-9a-fA-F]+', line)
            if sort == 'binary':
                number = re.findall(r'[01]+', line)

            if len(number) > 0: #Ok
                obj.append(SortingObj(line, number[0], sort))
            else: #No number found
                obj.append(SortingObj(line, 0, sort))

        obj.sort(key=lambda x: x.getNumber())

        for line in obj:
            conteneur.append(line.getLine())

        writeToView(self, region, conteneur)

    def sortStrings(self, region, contenue, sort):
        '''sort alphabetically or naturally'''

        keyFuncs = []
        caseSensitive = self.settings.get('alphabetical_case_sensitive', False)
        toIgnore = self.settings.get('alphabetical_ignore_patterns', [])

        if not caseSensitive:
            keyFuncs.append(str.lower)
            toIgnore = [pattern.lower() for pattern in toIgnore]

        if toIgnore:
            keyFuncs.append(ignorePatterns(toIgnore, caseSensitive))

        if sort == 'naturalOrder':
            keyFuncs.append(naturalize)

        keyFunc = compose(keyFuncs)
        conteneur = sorted(contenue, key=keyFunc, reverse=self.settings.get("descending"))

        writeToView(self, region, conteneur)

    def sortLength(self, region, contenue, sort):
        '''sort by string length'''
        if self.settings.get('length_alphabetically_enabled'):
            conteneur = defaultdict(list)

            #Put all values in a defaultdict (Grouped by length)
            for string in sorted(contenue, key=len):
                conteneur[len(string)].append(string)

            #Sort the groups alphabetically
            for k, v in conteneur.items():
                conteneur[k] = sorted(v, reverse=self.settings.get("descending"))

            #Sort the groups by length
            conteneur = sorted(conteneur.items(), key=lambda t: t[0], reverse=self.settings.get("descending"))

            conteneurTmp = []
            for k, v in conteneur:
                for string in v:
                    conteneurTmp.append(string)
            conteneur = conteneurTmp
        else:
            conteneur = sorted(contenue, key=len, reverse=self.settings.get("descending"))

        writeToView(self, region, conteneur)

    def chooseSortMethod(self, region, lines, sort):
        if sort == 'string' or sort == 'naturalOrder':
            self.sortStrings(region, lines, sort)
        elif sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
            self.sortNumbers(region, lines, sort)
        elif sort == 'length':
            self.sortLength(region, lines, sort)

    def run(self, edit, sort='string'):
        view = self.view
        self.edit = edit
        self.settings = sublime.load_settings("SortBy.sublime-settings")

        if view.sel()[0].empty() and len(view.sel()) == 1: #No selection
            self.estSelect = False
            region = view.sel()[-1].end()
            lines = [x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != '']
            self.chooseSortMethod(region, lines, sort)
        else:
            self.estSelect = True
            for region in view.sel():
                if region.empty():
                    continue
                else:
                    lines = [x for x in view.substr(region).splitlines() if x != '']
                    self.chooseSortMethod(region, lines, sort)

################################################################################
# options checkboxes

class OptionBase(sublime_plugin.TextCommand):
    def __init__(self, cmd):
        super().__init__(cmd)
        self.option = ""

    def is_checked(self):
        settings = sublime.load_settings("SortBy.sublime-settings")
        return settings.get(self.option)

    def run(self, edit):
        settings = sublime.load_settings("SortBy.sublime-settings")
        settings.set(self.option, not settings.get(self.option, False))
        sublime.save_settings("SortBy.sublime-settings")

class OptionsDescendingCommand(OptionBase):
    def __init__(self, cmd):
        super().__init__(cmd)
        self.option = "descending"

class OptionsCaseSensitiveCommand(OptionBase):
    def __init__(self, cmd):
        super().__init__(cmd)
        self.option = "alphabetical_case_sensitive"

class OptionsLengthAlphaCommand(OptionBase):
    def __init__(self, cmd):
        super().__init__(cmd)
        self.option = "length_alphabetical_enabled"
