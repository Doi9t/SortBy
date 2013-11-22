import sublime, sublime_plugin, string, re

bases = {'binary' : 2,'octal' : 8,'decimal' : 10, 'hexadecimal' : 16};

#Thanks to Ned Batchelder for this function
#http://nedbatchelder.com/blog/200712/human_sorting.html
def sort_naturel(liste): 
    convertion = lambda e: int(e) if e.isdigit() else e.lower();
    key1 = lambda key: [ convertion(g) for g in re.split('([0-9]+)', key) ];
    return sorted(liste, key = key1)

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
	def sortNumbers(self, edit, region, contenue, sort, estSelect, reversed): #Sort numbers with letters

		conteneur = [];
		idx = 0;
		obj = [];

		for line in contenue:
			number = '';
			if sort == 'decimal':
				number = re.findall(r'[+-]?\d+(?:\.\d+)?', line); 
			if sort == 'octal':
				number = re.findall(r'[0-7]+', line);
			if sort == 'hexadecimal':
				number = re.findall(r'[0-9a-fA-F]+', line);
			if sort == 'binary':
				number = re.findall(r'[01]+', line);

			if len(number) > 0: #Ok
				obj.append(SortingObj(line, number[0], sort));
			else: #No number found
				obj.append(SortingObj(line, 0, sort));

			idx = idx + 1;

		obj.sort(key=lambda x: x.getNumber(), reverse=reversed)

		for line in obj:
			conteneur.append(line.getLine());

		if len(conteneur) != 0:
			conteneur = [str(x) + '\n' for x in conteneur];
			conteneur[-1] = conteneur[-1][:-1];
			chaineFinale = ''.join(conteneur);
		
			if estSelect:
				self.view.replace(edit, region, chaineFinale);
			else:
				self.view.erase(edit, sublime.Region(0, self.view.size()));
				self.view.insert(edit, 0, chaineFinale);


	def sortStrings(self, edit, region, contenue, sort, estSelect, reversed): #Sort strings and natural order

		if contenue[-1][-1] != '\n':
			contenue[-1] += '\n';

		if sort == 'length':
			conteneur = sorted(contenue, key=lambda str: len(str), reverse=reversed);
		elif sort == 'string':
			conteneur = sorted(contenue, key=lambda str: str.lower(), reverse=reversed);
		elif sort == 'naturalOrder':
			conteneur = sort_naturel(contenue);

		if len(conteneur) != 0:
			conteneur[-1] = conteneur[-1][:-1];
			chaineFinale = ''.join(conteneur);

			if estSelect:
				self.view.replace(edit, region, chaineFinale);
			else:
				self.view.erase(edit, sublime.Region(0, self.view.size()));
				self.view.insert(edit, 0, chaineFinale);
		else:
			print("SortBy error: No string found !");

	def run(self, edit, sort = 'length', reversed=False):
		view = self.view;
		lines = [];
		
		if view.sel()[0].empty() and len(view.sel()) == 1: #No selection
			lines = view.substr(sublime.Region(0, self.view.size())).splitlines(True);
			
			if sort == 'length' or sort == 'string' or sort == 'naturalOrder':
				self.sortStrings(edit, view.sel()[-1].end(), lines, sort, False, reversed);
			elif sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
				self.sortNumbers(edit, view.sel()[-1].end(), lines, sort, False, reversed);
		else:
			for region in view.sel():
				lines = view.substr(region).splitlines(True);

				if region.empty():
					continue;
				else:
					if sort == 'length' or sort == 'string' or sort == 'naturalOrder':
						self.sortStrings(edit, region, lines, sort, True, reversed);
					elif sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
						self.sortNumbers(edit, region, lines, sort, True, reversed);