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

class SortingObj(object):
	def __init__(self, line, number):
		self.line = str(line);
		self.number = int(number);

	def getLine(self):
		return self.line;
	def getNumber(self):
		return self.number;

class SrtbyliCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):

		view = self.view;

		for region in view.sel():
			ligne = view.line(region);

			#Sort numbers with letters
			if sort == 'decimalLetter':
				contenue = view.substr(ligne).splitlines(True);

				if contenue[-1][-1] != '\n':
					contenue[-1] += '\n';
					
				removeNewLine(contenue);
				conteneur = [];

				idx = 0;
				obj = [];
				for line in contenue:
					number = re.findall(r'[+-]?\d+(?:\.\d+)?', line);

					if len(number) > 0: #Ok
						obj.append(SortingObj(line, number[0]));
					else: #No number found
						obj.append(SortingObj(line, 0));

					idx = idx + 1;

				obj.sort(key=lambda x: x.getNumber(), reverse=reversed)

				for line in obj:
					conteneur.append(line.getLine());

				chaineFinale = ''.join(conteneur);
				view.replace(edit, region, chaineFinale);


			#Sort numbers
			if  sort == 'octal' or sort == 'hexadecimal' or sort == 'binary': 
				contenue = view.substr(ligne).splitlines();
				contenue  = [i for i in contenue if isBase(i, bases[sort])]; 
				removeNewLine(contenue);
				conteneur = sorted(contenue, key=lambda str: baseToInteger(str, bases[sort]), reverse=reversed); 

				if len(conteneur) != 0:
					conteneur = [str(x) + '\n' for x in conteneur];
					conteneur[-1] = conteneur[-1][:-1];
					chaineFinale = ''.join(conteneur);
					view.replace(edit, region, chaineFinale);

				else:
					print("SortBy error: No number found !");

			#Sort strings
			if sort == 'length' or sort == 'string':
				listeLignes = view.substr(ligne).splitlines(True);

				if listeLignes[-1][-1] != '\n':
					listeLignes[-1] += '\n';
					
				removeNewLine(listeLignes);
				
				if sort == 'length':
					conteneur = sorted(listeLignes, key=lambda str: len(str), reverse=reversed);
				else:
					conteneur = sorted(listeLignes, key=lambda str: str.lower(), reverse=reversed);

				if len(conteneur) != 0:

					chaineFinale = ''.join(conteneur);
					view.replace(edit, region, chaineFinale);
				else:
					print("SortBy error: No string found !");