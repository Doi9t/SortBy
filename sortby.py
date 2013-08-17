import sublime, sublime_plugin, string, re

def isNombre(x):
	try:
		float(x)
		return True;
	except ValueError:
		return False;

class SbyCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):
		view = self.view;
		
		if sort == 'length':
			for region in view.sel():
				ligne = view.line(region);
				listeLignes = view.substr(ligne).splitlines(True);

				#Pour le dernier mot
				if listeLignes[-1][-1] != '\n':
					listeLignes[-1] += '\n';
				
				conteneur = sorted(listeLignes, key=lambda str: len(str), reverse=reversed);
				chaineFinale = ''.join(map(str, conteneur));
				view.replace(edit, region, chaineFinale);


		if sort == 'number':
			for region in view.sel():
				ligne = view.line(region)  
				contenue = view.substr(ligne).splitlines();
				contenue  = [i for i in contenue if isNombre(i)]; #Enleve tout les non nombres
				conteneur = sorted(contenue, key=float, reverse=reversed); #trie le tableau
				conteneur = [str(x) + '\n' for x in conteneur]; #On ajoute \n a chaque element
				conteneur[-1] = conteneur[-1][:-1]; #On enleve le \n du dernier element
				chaineFinale = ''.join(map(str, conteneur));
				view.replace(edit, region, chaineFinale);