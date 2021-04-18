import sublime
import sublime_plugin


class tag_surround(sublime_plugin.TextCommand):
	
	def run(self, edit):

		selekcije = self.view.sel()
		for s in selekcije:
			if not s.empty():
				r = sublime.Region(s.begin(), s.end())

			s1 = self.view.substr(r)
			# promeniti u drugi par tagova po potrebi
			t1 = "<span class='klasa_1'>"
			t2 = "</span>"
			
			self.view.replace(edit, r, t1 + s1 + t2)
