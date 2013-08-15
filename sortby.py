import sublime, sublime_plugin, string, re

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
				view.replace(edit, region, chaineFinale.strip());

"""
		if sort == 'integer':
			for region in view.sel():
				ligne = view.line(region)  
				contenue = view.substr(ligne);
				conteneurTemp = contenue.split('\n');

				for nombre in conteneurTemp:
					isFloat = False;
					isInteger = False;
					
					try:
					   val = int(nombre);
					   isInteger = True;
					except ValueError:
					   print("Pas integer => " + nombre);

					try:
					   val = float(nombre);
					   isFloat = True;
					except ValueError:
					   print("Pas float => " + nombre);

"""
