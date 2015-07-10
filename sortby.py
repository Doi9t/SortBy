import sublime, sublime_plugin, string, re
from collections import defaultdict

bases = {'binary' : 2,'octal' : 8,'decimal' : 10, 'hexadecimal' : 16};

#Thanks to Ned Batchelder for this function
#http://nedbatchelder.com/blog/200712/human_sorting.html
def sort_naturel(liste): 
    convertion = lambda e: int(e) if e.isdigit() else e.lower();
    key1 = lambda key: [ convertion(g) for g in re.split('([0-9]+)', key) ];
    return sorted(liste, key = key1);

def putEndLines(arr):
	arr = [str(x) + '\n' for x in arr];
	arr[-1] = arr[-1][:-1];
	return arr;

def writeToView(self, region, conteneur):
	if len(conteneur) != 0:
		if self.estSelect:
			self.view.replace(self.edit, region, ''.join(putEndLines(conteneur)));
		else:
			self.view.erase(self.edit, sublime.Region(0, self.view.size()));
			self.view.insert(self.edit, 0, ''.join(putEndLines(conteneur)));
	else:
		print("SortBy error: No string found !");

class SortingObj(object):
	def __init__(self, line, number, base):
		self.line = str(line).strip();
		self.number = number;
		self.base = base;
	def getLine(self):
		return self.line;
	def getNumber(self):
		if self.number == 0:
			return 0;
		else:
			return int(self.number, bases[self.base]);

class SrtbyliCommand(sublime_plugin.TextCommand):

	def sortArray(self, contenue):
		conteneur = [];
		obj = [];

		if self.sort == 'length':

			if self.settings.get('length_alphabetically_enabled'):
				conteneur = defaultdict(list)

				#Put all values in a defaultdict (Grouped by length)
				for str in sorted(contenue, key=lambda str: len(str)) :
					conteneur[len(str)].append(str)

				#Sort the groups alphabetically 
				for k, v in conteneur.items():
					conteneur[k] = sorted(v, reverse=self.settings.get('length_alphabetically_reversed'))

				#Sort the groups by length
				conteneur = sorted(conteneur.items(), key=lambda t: t[0], reverse=self.reversed)

				conteneurTmp = []
				for k, v in conteneur:
					for str in v:
						conteneurTmp.append(str)
				conteneur = conteneurTmp;

			else:
				conteneur = sorted(contenue, key=lambda str: len(str), reverse=self.reversed)

		elif self.sort == 'string':
			if self.settings.get('alphabetical_case_sensitive'):
				conteneur = sorted(contenue, reverse=self.reversed);
			else:
				conteneur = sorted(contenue, key=lambda str: str.lower(), reverse=self.reversed);

		elif self.sort == 'naturalOrder':
			conteneur = sort_naturel(contenue);

		else:
			for line in contenue:
				number = '';
				
				if self.sort == 'octal': number = re.findall(r'[0-7]+', line);
				if self.sort == 'binary': number = re.findall(r'[01]+', line);
				if self.sort == 'decimal': number = re.findall(r'[+-]?\d+(?:\.\d+)?', line); 
				if self.sort == 'hexadecimal': number = re.findall(r'(?:0[xX])?[0-9a-fA-F]+', line);
					
				if len(number) > 0: #Ok
					obj.append(SortingObj(line, number[0], self.sort));
				else: #No number found
					obj.append(SortingObj(line, 0, self.sort));

			obj.sort(key=lambda x: x.getNumber(), reverse=self.reversed)

			for line in obj:
				conteneur.append(line.getLine());

		return conteneur;

	def run(self, edit, sort = 'length', reversed=False):
		lines = [];
		view = self.view;
		self.edit = edit; 
		self.sort = sort;
		self.reversed = reversed;
		self.settings = sublime.load_settings("SortBy.sublime-settings");

		if view.sel()[0].empty() and len(view.sel()) == 1: #No selection
			self.estSelect = False;
			result = self.sortArray([x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != '']);
			writeToView(self, view.sel()[-1].end(), result);
		else:
			self.estSelect = True;
			for region in view.sel():
				if region.empty():
					continue;
				else:
					result = self.sortArray([x for x in view.substr(region).splitlines() if x != '']);
					writeToView(self, region, result);