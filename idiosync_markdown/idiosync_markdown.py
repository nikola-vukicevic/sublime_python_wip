# ------------------------------------------------------------------------------
# Sublime-ov plugin koji koristim za markdown, ne uvlači tagove i vraća
# rezultat koji je malo previše 'zvaničan' (što znači da posle ionako
# moram da skidam nepotrebne informacije koje plugin doda i naravno,
# da sredim uvlačenje.
#
# U člancima koje pišem, u najvećoj meri  koristim samo paragrafe, 
# naslove (h1, h2, h3, h4) i ulančane liste, pa se čini da je
# ovakav, 'idiosinkratični' DIY plugin pravo rešenje za takvu situaciju. :)
#
# Sintaksa:
# 
#     #1 - h1
#     #2 - h1
#     #3 - h1
#     #4 - h1
#     *  - ul
#     \t - li
#
# Napomena: za "<ul>" mora ručno da se doda zatvarajući tag.
#
# Copyright (C) 2021. Nikola Vukićević
#
# ------------------------------------------------------------------------------

import sublime
import sublime_plugin

class idiosync_markdown(sublime_plugin.TextCommand):
	
	def run(self, edit):

		r = sublime.Region(0, self.view.size() - 1)

		s = self.view.substr(r)
		
		s = self.idiosyncParse(s)
		s = self.formatiranje(s)
			
		self.view.replace(edit, r, s)

	def formatiranje(self, s):
		s = s.replace("</h1>", "</h1>\n")
		s = s.replace("</h2>", "</h2>\n")
		s = s.replace("</h3>", "</h3>\n")
		s = s.replace("</h4>", "</h4>\n")
		s = s.replace("</ul>", "</ul>\n")
		s = s.replace("<li>",  "\t<li>")

		s = s.replace("<p>", "<p>\n\t")
		s = s.replace("</p>", "\n</p>\n")

		return s

	def idiosyncParse(self, s):
		redovi = s.split("\n")
		tokeni = []
		s      = ""
		
		for r in redovi:
			if not r:
				continue
			if r.startswith("#1"):
				r = r + " "
				tokeni.append(["<h1>", r[ 2 : len(r) ].strip(), "</h1>"])
				continue
			if r.startswith("#2"):
				tokeni.append(["<h2>", r[ 2 : len(r) ].strip(), "</h2>"])
				continue
			if r.startswith("#3"):
				tokeni.append(["<h3>", r[ 2 : len(r) ].strip(), "</h3>"])
				continue
			if r.startswith("#4"):
				tokeni.append(["<h4>", r[ 2 : len(r) ].strip(), "</h4>"])
				continue
			if r.startswith("*"):
				tokeni.append(["<ul>", "",        ""])
				continue
			if r.startswith("\t"):
				tokeni.append(["<li>", r.strip(), "</li>"])
				continue

			tokeni.append(["<p>", r.strip(), "</p>"])

		for t in tokeni:
			s = s + t[0] + t[1] + t[2] + "\n"

		return s
