import sys

maks_duzina = 0

#-------------------------------------------------------------------------------

def rastavljanje_tokena(redovi, tokeni):
	for r in redovi:
		if r != "":
			t = r.strip()
			if t.startswith("}") or t.endswith("{"):
				tokeni.append([False, t])
			else:
				p = t.split(": ")
				a = p[0].strip()
				v = p[1].strip()
				tokeni.append([True, a, v, len(a)])

#-------------------------------------------------------------------------------

def racunaje_duzina(tokeni):
	global maks_duzina
	pom = ""

	for t in tokeni:
		if t[0] == True:
			if t[3] > maks_duzina:
				maks_duzina = t[3]

#-------------------------------------------------------------------------------

def ispis_tokena(tokeni):
	s = ""

	for t in tokeni:
		if t[0] == True:
			s = s + "\t" + str(t[1]) + ": " + dodavanje_spejsova(maks_duzina - t[3])  + str(t[2]) + "\n"
		else:
			s = s + str(t[1]) + "\n"
			if t[1] == "}":
				s = s + "\n"
	return s

#-------------------------------------------------------------------------------

def dodavanje_spejsova(n):
	s = ""

	for i in range(0, n):
		s = s + " "

	return s

#-------------------------------------------------------------------------------

def ucitavanje():
	f = open("ulaz.css", "r")
	return f.read()

#-------------------------------------------------------------------------------

def zapis(s):
	f = open("izlaz.css", "w")
	return f.write(s)

#-------------------------------------------------------------------------------

redovi = ucitavanje().split("\n")
tokeni = []

rastavljanje_tokena(redovi, tokeni)
racunaje_duzina(tokeni)
s = ispis_tokena(tokeni)
zapis(s)
print("Sve ok")
