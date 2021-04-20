# ------------------------------------------------------------------------------
# Sublime-ov plugin koji koristim za markdown, ne uvlači tagove i vraća
# rezultat koji je malo previše 'zvaničan' (što znači da posle ionako
# moram da skidam nepotrebne informacije koje plugin doda i naravno,
# da sredim uvlačenje.
#
# U člancima koje pišem, u najvećoj meri  koristim samo paragrafe, 
# naslove (h1, h2, h3, h4) i ulančane liste (sve ostalo lako rešavam
# preko snipeta), pa se čini da je ovakav, 'idiosinkratični' DIY plugin
# pravo stvar za takvu situaciju. :)
#
# Sintaksa (donekle se poklapa sa zvaničnom specifikacijom):
# 
#     #    - Dodaje "<h1>" i "</h1>" oko reda koji počinje sa "#"
#     ##   - Dodaje "<h2>" i "</h2>" oko reda koji počinje sa "##"
#     ###  - Dodaje "<h3>" i "</h3>" oko reda koji počinje sa "###
#     #### - Dodaje "<h4>" i "</h4>" oko reda koji počinje sa "####"
#            (h5 i h6 mi, za sada, ne trebaju, ali, prisutan je kod
#             i za njih, pod komentarom; ako se stavi pet ili
#             šest zvezdica, skripta će to preppoznati kao h4)
#     *    - Menja zvezdicu u "<ul>"
#     **   - Menja dve zvezdice u "</ul>"
#     \t   - Dodaje "<li>" i "</li>" oko reda koji počinje sa "\t"
#     ``   - Početak HTML bloka (koji će biti direktno preslikan)
#     ~~   - Završetak HTML bloka
#     !!   - Komentar (red koji počinje sa "!!" biće zanemaren)
#
# Copyright (C) 2021. Nikola Vukićević
#
# ------------------------------------------------------------------------------

import sublime
import sublime_plugin
import re

class idiosync_markdown(sublime_plugin.TextCommand):
	
	def run(self, edit):

		r = sublime.Region(0, self.view.size())
		s = self.view.substr(r)
		s = self.idiosyncParse(s)
		#s = self.zamena_tokena_slike(s)
		self.view.replace(edit, r, s)

	def idiosyncParse(self, s):
		redovi = s.split("\n")
		tokeni = []
		s      = ""
		parse  = True

		for r in redovi:
			if not r:
				continue
			
			if parse == True:
				if r.startswith("``"):
					parse = False
					continue
				self.ucitavanje_tokena(r, tokeni)
				
			else:
				if r.startswith("~~"):
					parse = True
					tokeni.append(["", "", ""])
					continue
				tokeni.append([r, "", ""])

		for t in tokeni:
			s = s + t[0] + t[1] + t[2] + "\n"

		return s

	def ucitavanje_tokena(self, r, tokeni):
		if r.startswith("!!"):
			return
		# Za sada mi ne trebaju h5 i h6, ali, ako zatreba ....
		# if r.startswith("######"):
		# 	tokeni.append(["<h6>", r.lstrip('#').strip(), "</h6>\n"])
		# 	continue
		# if r.startswith("#####"):
		# 	tokeni.append(["<h5>", r.lstrip('#').strip(), "</h5>\n"])
		# 	continue
		if r.startswith("####"):
			tokeni.append(["<h4>", r.lstrip('#').strip(), "</h4>\n"])
			return
		if r.startswith("###"):
			tokeni.append(["<h3>", r.lstrip('#').strip(), "</h3>\n"])
			return
		if r.startswith("##"):
			tokeni.append(["<h2>", r.lstrip('#').strip(), "</h2>\n"])
			return
		if r.startswith("#"):
			tokeni.append(["<h1>", r.lstrip('#').strip(), "</h1>\n"])
			return
		if r.startswith("**"):
			tokeni.append(["</ul>\n", "",        ""])
			return
		if r.startswith("*"):
			tokeni.append(["<ul>", "",        ""])
			return
		if r.startswith("\t"):
			tokeni.append(["\t<li>", r.strip(), "</li>"])
			return

		# Ako red nije ništa 'posebno', onda je <p> :)
		tokeni.append(["<p>\n\t", r.strip(), "\n</p>\n"])

	# --------------------------------------------------
	# Automatska numeracija slika u tekstu. Za ovo
	# koristim i posebne snipete, a sve zajedno to
	# verovatno ne bi bilo zanimljivo svima, pa se
	# zato metoda ne poziva po default-u
	# --------------------------------------------------

	def zamena_tokena_slike(self, s):
	    lista = re.split("#s#", s)

	    n = ""
	    i = 1

	    for l in lista:
	    	n = n + l + str(i)
	    	i = i + 1

	    return n.rstrip('0123456789\n ') + "\n"
