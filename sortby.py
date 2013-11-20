import sublime, sublime_plugin, string, re

bases = {'binary' : 2,'octal' : 8,'decimal' : 10, 'hexadecimal' : 16};

def isBase(x,base):
    try:
        int(x, base);
        return True;
    except ValueError:
        return False;

def baseToInteger(x, base):
	return int(x,base);

def removeNewLine(x):
	for item in range(0, x.count(u'\n')):
		x.remove(u'\n');
	for item in range(0, x.count(u'\r')):
		x.remove(u'\r');

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
			return baseToInteger(self.number, bases[self.base]);

class SrtbyliCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):

		view = self.view;

		for region in view.sel():
			ligne = view.line(region);

			#Sort numbers with letters
			if sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary':
				contenue = view.substr(ligne).splitlines(True);

				if contenue[-1][-1] != '\n':
					contenue[-1] += '\n';
					
				removeNewLine(contenue);
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
				view.replace(edit, region, chaineFinale);
				
			#Sort strings and natural order
			if sort == 'length' or sort == 'string' or sort == 'naturalOrder':
				listeLignes = view.substr(ligne).splitlines(True);

				if listeLignes[-1][-1] != '\n':
					listeLignes[-1] += '\n';
					
				removeNewLine(listeLignes);
				
				if sort == 'length':
					conteneur = sorted(listeLignes, key=lambda str: len(str), reverse=reversed);
				elif sort == 'string':
					conteneur = sorted(listeLignes, key=lambda str: str.lower(), reverse=reversed);
				elif sort == 'naturalOrder':
					conteneur = sort_naturel(listeLignes);

				if len(conteneur) != 0:
					chaineFinale = ''.join(conteneur);
					view.replace(edit, region, chaineFinale);
				else:
					print("SortBy error: No string found !");