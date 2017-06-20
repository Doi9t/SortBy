from __future__ import print_function
from collections import defaultdict
import functools
import re
import sublime
import sublime_plugin

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

bases = {'binary' : 2, 'octal' : 8, 'decimal' : 10, 'hexadecimal' : 16}
fmap = lambda fnlist, argument: reduce(lambda x, fn: fn(x), [argument] + fnlist)

@logInputAndOutput
def compose(functions):
    '''apply functions in order from left to right'''
    return lambda x: functools.reduce(lambda a, f: f(a), functions, x)

#Thanks to Ned Batchelder for this function
#http://nedbatchelder.com/blog/200712/human_sorting.html
@logInputAndOutput
def naturalize(line):
    conversion = lambda e: int(e) if e.isdigit() else e
    return [conversion(g) for g in re.split('([0-9]+)', line)]

@logInputAndOutput
def sort_naturel(liste):
    return sorted(liste, key=naturalize)

@logInputAndOutput
def ignorePatterns(toIgnore):
    return lambda line: [re.sub(pattern, "", line) for pattern in toIgnore]

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

class SrtbyliCommand(sublime_plugin.TextCommand):

    def __init__(self, cmd):
        super().__init__(cmd)
        self.estSelect = None
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

    @logInputAndOutput
    def sortStrings(self, region, contenue, sort): #Sort strings and natural order
        print("sortStrings")

        if sort == 'length':
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
        else:
            keyFuncs = []

            # toIgnore = self.settings.get('ignore_when_sorting')
            # if toIgnore:
            #     keyFuncs.append(ignorePatterns)

            if not self.settings.get('case_sensitive'):
                keyFuncs.append(str.lower)

            if sort == 'naturalOrder':
                keyFuncs.append(naturalize)

            keyFunc = compose(keyFuncs)
            print("final func:", keyFunc)
            conteneur = sorted(contenue, key=keyFunc, reverse=self.settings.get("descending"))

        writeToView(self, region, conteneur)

    def run(self, edit, sort='length'):
        print("---")
        self.edit = edit
        view = self.view
        SrtbyliCommand.edit = edit
        self.settings = sublime.load_settings("SortBy.sublime-settings")

        if view.sel()[0].empty() and len(view.sel()) == 1: #No selection
            self.estSelect = False
            if sort == 'length' or sort == 'string' or sort == 'naturalOrder':
                self.sortStrings(view.sel()[-1].end(), [x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != ''], sort)
            elif sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
                self.sortNumbers(view.sel()[-1].end(), [x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != ''], sort)
        else:
            self.estSelect = True
            for region in view.sel():
                if region.empty():
                    continue
                else:
                    if sort == 'length' or sort == 'string' or sort == 'naturalOrder':
                        self.sortStrings(region, [x for x in view.substr(region).splitlines() if x != ''], sort)
                    elif sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
                        self.sortNumbers(region, [x for x in view.substr(region).splitlines() if x != ''], sort)


class OptionsDescendingCommand(sublime_plugin.TextCommand):

    def is_checked(self):
        settings = sublime.load_settings("SortBy.sublime-settings")
        return settings.get("descending")

    def run(self, edit):
        settings = sublime.load_settings("SortBy.sublime-settings")
        settings.set("descending", not settings.get("descending", False))
        sublime.save_settings("SortBy.sublime-settings")
