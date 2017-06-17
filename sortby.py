from __future__ import print_function
from collections import defaultdict
import re
import unicode
import sublime
import sublime_plugin

bases = {'binary' : 2, 'octal' : 8, 'decimal' : 10, 'hexadecimal' : 16}

#Thanks to Ned Batchelder for this function
#http://nedbatchelder.com/blog/200712/human_sorting.html
def sort_naturel(liste):
    convertion = lambda e: int(e) if e.isdigit() else e.lower()
    key1 = lambda key: [convertion(g) for g in re.split('([0-9]+)', key)]
    print(key1)
    return sorted(liste, key=key1)

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

    def __init__(self):
        self.reverse = False
        self.estSelect = None
        self.settings = None

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

        obj.sort(key=lambda x: x.getNumber(), reverse=self.reverse)

        for line in obj:
            conteneur.append(line.getLine())

        writeToView(self, region, conteneur)

    def sortStrings(self, region, contenue, sort): #Sort strings and natural order
        if sort == 'length':
            if self.settings.get('length_alphabetically_enabled'):
                conteneur = defaultdict(list)

                #Put all values in a defaultdict (Grouped by length)
                for string in sorted(contenue, key=len):
                    conteneur[len(string)].append(string)

                #Sort the groups alphabetically
                for k, v in conteneur.items():
                    conteneur[k] = sorted(v, reverse=self.settings.get('length_alphabetically_reversed'))

                #Sort the groups by length
                conteneur = sorted(conteneur.items(), key=lambda t: t[0], reverse=self.reverse)

                conteneurTmp = []
                for k, v in conteneur:
                    for string in v:
                        conteneurTmp.append(string)
                conteneur = conteneurTmp

            else:
                conteneur = sorted(contenue, key=len, reverse=self.reverse)

        elif sort == 'string':
            if self.settings.get('case_sensitive'):
                conteneur = sorted(contenue, reverse=self.reverse)
            else:
                conteneur = sorted(contenue, key=str.lower, reverse=self.reverse)

        elif sort == 'naturalOrder':
            conteneur = sort_naturel(contenue)

        writeToView(self, region, conteneur)

    def run(self, edit, sort='length', reverse=False):
        self.edit = edit
        view = self.view
        self.reverse = reverse
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
