import sublime, sublime_plugin, string

class SbyCommand(sublime_plugin.TextCommand):
	def run(self, edit, sort = 'length', reversed=False):
		view = self.view;

		if sort == 'length':
			for region in view.sel():
				ligne = view.line(region)  
				contenue = view.substr(ligne);
				conteneur = sorted(contenue.split('\n'), key = lambda str: len(str), reverse=reversed);

				#ajout du caractere
				i = 0;
				for mot in conteneur:
					conteneur[i] = mot + '\n';
					i = i + 1;

				chaineFinale = ''.join(map(str, conteneur));
				view.replace(edit, region, chaineFinale.strip())