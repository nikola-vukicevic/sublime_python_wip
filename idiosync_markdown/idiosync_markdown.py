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
# Sintaksa (donekle se poklapa sa zvaničnom specifikacijom):
# 
#     #    - Dodaje "<h1>" i "</h1>" oko reda koji počinje sa "#" i briše tarabe
#     ##   - Dodaje "<h2>" i "</h2>" oko reda koji počinje sa "##" i briše tarabe
#     ###  - Dodaje "<h3>" i "</h3>" oko reda koji počinje sa "###" i briše tarabe
#     #### - Dodaje "<h4>" i "</h4>" oko reda koji počinje sa "####" i briše tarabe
#            (h5 i h6 mi, za sada, ne trebaju, ali, prisutan je kod
#             i za njih, pod komentarom; ako se stavi pet ili
#             šest zvezdica, skripta će to preppoznati kao h4)
#     *    - Menja zvezdicu u "<ul>"
#     **   - Menja dve zvezdice u "</ul>"
#     \t   - Dodaje "<li>" i "</li>" oko reda koji počinje sa "\t"
#
# Copyright (C) 2021. Nikola Vukićević
#
# ------------------------------------------------------------------------------

import sublime
import sublime_plugin

class idiosync_markdown(sublime_plugin.TextCommand):
	
	def run(self, edit):

		r = sublime.Region(0, self.view.size())
		s = self.view.substr(r)
		s = self.idiosyncParse(s)
			
		self.view.replace(edit, r, s)

	def idiosyncParse(self, s):
		redovi = s.split("\n")
		tokeni = []
		s      = ""

		for r in redovi:
			if not r:
				continue
			
			# Za sada mi ne trebaju h5 i h6, ali, nikad se ne zna ....

			# if r.startswith("######"):
			# 	tokeni.append(["<h6>", r.lstrip('#').strip(), "</h6>\n"])
			# 	continue
			# if r.startswith("#####"):
			# 	tokeni.append(["<h5>", r.lstrip('#').strip(), "</h5>\n"])
			# 	continue
			
			if r.startswith("!!"):
				tokeni.append([r.lstrip('!'), "", ""])
				continue
			if r.startswith("####"):
				tokeni.append(["<h4>", r.lstrip('#').strip(), "</h4>\n"])
				continue
			if r.startswith("###"):
				tokeni.append(["<h3>", r.lstrip('#').strip(), "</h3>\n"])
				continue
			if r.startswith("##"):
				tokeni.append(["<h2>", r.lstrip('#').strip(), "</h2>\n"])
				continue
			if r.startswith("#"):
				tokeni.append(["<h1>", r.lstrip('#').strip(), "</h1>\n"])
				continue
			if r.startswith("**"):
				tokeni.append(["</ul>\n", "",        ""])
				continue
			if r.startswith("*"):
				tokeni.append(["<ul>", "",        ""])
				continue
			if r.startswith("\t"):
				tokeni.append(["\t<li>", r.strip(), "</li>"])
				continue

			# Ako red nije ništa 'posebno', onda je <p> :)

			tokeni.append(["<p>\n\t", r.strip(), "\n</p>\n"])

		for t in tokeni:
			s = s + t[0] + t[1] + t[2] + "\n"

		return s
