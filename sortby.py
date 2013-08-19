import sublime, sublime_plugin, string

bases = {'binary' : 2,'octal' : 8,'decimal' : 10, 'hexadecimal' : 16}

def estBase(x,base):
    try:
        int(x, base);
        return True;
    except ValueError:
        return False;

def baseToInteger(x,base):
	return int(x,base);

class SbyCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):
		view = self.view;

		for region in view.sel():
			ligne = view.line(region);

			if sort == 'decimal' or sort == 'octal' or sort == 'hexadecimal' or sort == 'binary': 
				contenue = view.substr(ligne).splitlines();
				contenue  = [i for i in contenue if estBase(i, bases[sort])]; 
				conteneur = sorted(contenue, key=lambda str: baseToInteger(str, bases[sort]), reverse=reversed); 

				if len(conteneur) != 0:
					conteneur = [str(x) + '\n' for x in conteneur]; #On ajoute \n a chaque element
					conteneur[-1] = conteneur[-1][:-1]; #On enleve le \n du dernier element
					chaineFinale = ''.join(map(str, conteneur));
					view.replace(edit, region, chaineFinale);
				else:
					print("SortBy error: No number found !");


			if sort == 'length':
				listeLignes = view.substr(ligne).splitlines(True);
				#Pour le dernier mot
				if listeLignes[-1][-1] != '\n':
					listeLignes[-1] += '\n';
				
				conteneur = sorted(listeLignes, key=lambda str: len(str), reverse=reversed);
				if len(conteneur) != 0:
					chaineFinale = ''.join(map(str, conteneur));
					view.replace(edit, region, chaineFinale);
				else:
					print("SortBy error: No string found !");
