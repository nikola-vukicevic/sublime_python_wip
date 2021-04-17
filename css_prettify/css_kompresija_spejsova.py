import sublime
import sublime_plugin


class css_kompresija_spejsova(sublime_plugin.TextCommand):
	maks_duzina = 0

	def run(self, edit):

		selekcije = self.view.sel()
		for s in selekcije:
			if s.empty():
				r = sublime.Region(0, self.view.size() - 1)
			else:
				r = sublime.Region(s.begin(), s.end())

			s1     = self.view.substr(r)

			redovi = s1.split("\n")
			tokeni = []

			self.rastavljanje_tokena(redovi, tokeni)
			self.racunaje_duzina(tokeni)

			s2     = self.ispis_tokena(tokeni)

			self.view.replace(edit, r, s2)

#-------------------------------------------------------------------------------

	def rastavljanje_tokena(self, redovi, tokeni):
		for r in redovi:
			t = r.rstrip()
			if t.endswith(";"):
				if t.lstrip().startswith("//") or t.lstrip().startswith("@"):
					tokeni.append([False, t])
				else:
					p = t.split(":")
					a = p[0].rstrip()
					v = p[1].strip()
					tokeni.append([True, a, v, len(a)])
			else:
				tokeni.append([False, t])

#-------------------------------------------------------------------------------

	def racunaje_duzina(self, tokeni):
		pom = ""

		for t in tokeni:
			if t[0] == True:
				if t[3] > self.maks_duzina:
					self.maks_duzina = t[3]

		self.maks_duzina = self.maks_duzina - 1

#-------------------------------------------------------------------------------

	def ispis_tokena(self, tokeni):
		s = ""

		for t in tokeni:
			if t[0] == True:
				s = s + str(t[1]) + ": " + str(t[2]) + "\n"
			else:
				s = s + str(t[1]) + "\n"
		return s[ 0 : len(s)-1 ]

#-------------------------------------------------------------------------------

	def dodavanje_spejsova(self, n):
		s = ""
		n = n + 1

		for i in range(0, n):
			s = s + " "

		return s

#-------------------------------------------------------------------------------

	def ucitavanje(self):
		f = open("ulaz.css", "r")
		return f.read()

#-------------------------------------------------------------------------------

	def zapis(self, s):
		f = open("izlaz.css", "w")
		return f.write(s)

#-------------------------------------------------------------------------------
