import sublime, sublime_plugin, string

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
	for item in xrange(x.count(u'\n')):
		x.remove(u'\n');
	for item in xrange(x.count(u'\r')):
		x.remove(u'\r');


class SrtbyliCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):
		view = self.view;

		for region in view.sel():
			ligne = view.line(region);

			if sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary': 
				contenue = view.substr(ligne).splitlines();
				contenue  = [i for i in contenue if isBase(i, bases[sort])]; 
				removeNewLine(contenue);
				conteneur = sorted(contenue, key=lambda str: baseToInteger(str, bases[sort]), reverse=reversed); 

				if len(conteneur) != 0:
					conteneur = [str(x) + '\n' for x in conteneur];
					conteneur[-1] = conteneur[-1][:-1];
					chaineFinale = ''.join(map(str, conteneur));
					view.replace(edit, region, chaineFinale);

				else:
					print("SortBy error: No number found !");

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
					chaineFinale = ''.join(map(str, conteneur));
					view.replace(edit, region, chaineFinale);
				else:
					print("SortBy error: No string found !");