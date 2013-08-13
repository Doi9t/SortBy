import sublime, sublime_plugin, string

class SbyCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):
		view = self.view;
		
		if sort == 'length':
			for region in view.sel():
				ligne = view.line(region)  
				contenue = view.substr(ligne);
				conteneur = sorted(contenue.split('\n'), key=lambda str: len(str), reverse=reversed);

				for (i, mot) in enumerate(conteneur):
					conteneur[i] = mot + '\n';

				chaineFinale = ''.join(map(str, conteneur));
				view.replace(edit, region, chaineFinale.strip());

				
		if sort == 'integer':
			for region in view.sel():
				ligne = view.line(region)  
				contenue = view.substr(ligne);
				conteneur = sorted(contenue.split('\n'), key=float ,reverse=reversed);
				
				for (i, mot) in enumerate(conteneur):
					conteneur[i] = mot + '\n';

				chaineFinale = ''.join(map(str, conteneur));
				view.replace(edit, region, chaineFinale.strip());
