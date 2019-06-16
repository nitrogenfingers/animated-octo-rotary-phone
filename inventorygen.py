from random import randint
from random import sample
import sys

buycodes = {-1:2.0, 0:1.75, 1:1.5, 2:1.35, 3:1.25, 4:1.2, 5:1.15,
6:1.1, 7:1.05, 8:1, 9:0.95, 10:0.9, 11:0.85, 12:0.8, 13:0.75, 14:0.7,
15:0.65, 16:0.6, 17:0.55, 18:0.5, 19:0.45, 20:0.4, 21:0.35, 22:0.3,
23:0.25}

sellcodes = {-1:0.3, 0:0.4, 1:0.45, 2:0.5, 3:0.55, 4:0.6, 5:0.65,
6:0.7, 7:0.75, 8:0.8, 9:0.85, 10:0.9, 11:1, 12:1.05, 13:1.1, 14:1.15,
15:1.2, 16:1.25, 17:1.3, 18:1.35, 19:1.4, 20:1.45, 21:1.5, 22:1.55,
23:1.6}

class Good(object):
	#base: The base cost of the good
	#dc: The number of dice to roll when determining amount
	#dx: The multiplier for the dice result
	#tc: Trade codes: set of codes where good appears
	#sc: Sell codes: Dictionary of trade codes and modifiers
	def __init__(self, name, base, dc, dx, tc, sc):
		self.name = name
		self.basecost = base
		self.dicecount = dc
		self.multiplier = dx
		self.tradecodes = tc
		self.modifiers = sc

class TradeEntry(object):
	name = None
	amount = 0
	baseamount = 0
	price = 0
	trademodifier = 0
	
	def __init__(self, tradegood, world, toBuy):
		self.name = tradegood.name
		self.price = tradegood.basecost
		for c in world.tradecodes:
			if (c in tradegood.modifiers): self.trademodifier += tradegood.modifiers[c]
		if (toBuy):
			for x in range(0, tradegood.dicecount): self.baseamount += roll(1)
			self.baseamount *= tradegood.multiplier
			self.amount = self.baseamount
		
	def doubleQuantity(self):
		self.amount += self.baseamount
		
	def toPrettyString(self, brokerRoll):
		priceModifier = max(-1, min(23, brokerRoll + self.trademodifier))
		finalprice = int(self.price * buycodes[priceModifier])
		return "  {0}T Cr {2}: {1} ({3}%)".format(self.amount, self.name, finalprice, int(buycodes[priceModifier]*100))

	def toCSVString(self, brokerRoll):
		buyModifier = max(-1, min(23, brokerRoll + self.trademodifier))
		sellModifier = max(-1, min(23, brokerRoll - self.trademodifier))

		finalBuyPrice = "-" if self.amount == 0 else int(self.price * buycodes[buyModifier])
		finalSellPrice = int(self.price * sellcodes[sellModifier])
		return "{0},{1},{2},{3}".format(self.amount, self.name, finalBuyPrice, finalSellPrice)


legalgoods = {
Good("Electronics", 20000, 2, 10, {"All"}, {"Lt":-1, "NI":-2, "Po":-1, "Ht":3, "In":2, "Ri":1}),
Good("Industrial Goods", 10000, 2, 10, {"All"}, {"Ag":-2, "NI":-3, "In":5, "Na":2}),
Good("Manufactured Goods", 20000, 2, 10, {"All"}, {"Hi":-2, "NI":-3, "In":5, "Na":2}),
Good("Raw Materials", 5000, 2, 20, {"All"}, {"In":-2, "Po":-2, "Ag":3, "Ga":2, "Wa":2}),
Good("Consumables", 500, 2, 20, {"All"}, {"As":-5, "Fl":-1, "Hi":-1, "Ic":-1, "Ag":3, "Ga":1, "Wa":2}),
Good("Common Ore", 1000, 2, 20, {"All"}, {"In":-3, "NI":-1, "As":4}),
Good("Advanced Electronics", 100000, 1, 5, {"In", "Ht"}, {"As":-3, "NI":-1, "Ri":-2, "Ht":3, "In":2}),
Good("Advanced Machine Parts", 75000, 1, 5, {"In", "Ht"}, {"As":-2, "NI":-1, "Ht":1, "In":2}),
Good("Advanced Manufactured Goods", 100000, 1, 5, {"In", "Ht"}, {"Hi":-1, "Ri":-2, "In":1}),
Good("Advanced Weapons", 150000, 1, 5, {"In", "Ht"}, {"Po":-1, "A":-2, "R":-4, "Ht":2}),
Good("Advanced Vehicles", 180000, 1, 5, {"In", "Ht"}, {"As":-2, "Ri":-2, "Ht":2}),
Good("Biochemicals", 50000, 1, 5, {"Ag", "Wa"}, {"In":-2, "Ag":-1}),
Good("Crystals & Gems", 20000, 1, 5, {"As", "De", "Ic"}, {"As":-2, "De":-1, "Ic":-1, "In":2}),
Good("Cybernetics", 250000, 1, 1, {"Ht"}, {"As":-1, "Ic":-1, "Po":-2, "Ht":1}),
Good("Live Animals", 10000, 1, 10, {"Ag", "Ca"}, {"Lo":-3, "Ag":2}),
Good("Luxury Consumables", 20000, 1, 10, {"Ag", "Ga", "Wa"}, {"Hi":-2, "Ri":-2, "Ag":2, "Wa":1}),
Good("Luxury Goods", 200000, 1, 1, {"Hi"}, {"Ri":-4, "Hi":1}),
Good("Medical Supplies", 50000, 1, 4, {"Ht", "Hi"}, {"In":-2, "Po":-1, "Ri":-1, "Ht":2}),
Good("Petrochemicals", 10000, 1, 10, {"De", "Fl", "Ic", "Wa"}, {"Ag":-1, "In":-2, "Lt":-2, "De":2}),
Good("Pharmaceuticals", 100000, 1, 1, {"As", "De", "Hi", "Wa"}, {"Lt":-1, "As":2, "Hi":1}),
Good("Polymers", 7000, 1, 10, {"In"}, {"NI":-1, "Ri":-2, "In":1}),
Good("Precious Metals", 50000, 1, 1, {"As", "De", "Hi", "Wa"}, {"Ht":-1, "In":-2, "Ri":-3, "As":3, "De":1, "Ic":2}),
Good("Radioactives", 1000000, 1, 1, {"As", "De", "Lo"}, {"Ag":3, "Ht":-1, "In":-3, "NI":2, "As":2, "Lo":2}),
Good("Robots", 400000, 1, 5, {"In"}, {"Ag":-2, "Ht":-1, "In":1}),
Good("Spices", 6000, 1, 5, {"Ga", "De", "Wa"}, {"Hi":-2, "Po":-3, "Ri":-3, "De":2}),
Good("Textiles", 3000, 1, 20, {"Ag", "NI"}, {"Hi":-3, "Na":-2, "Ag":7}),
Good("Uncommon Ore", 5000, 1, 20, {"As", "Ic"}, {"In":-3, "NI":-1, "As":4}),
Good("Uncommon Raw Materials", 20000, 1, 10, {"Ag", "De", "Wa"}, {"Ht":-1, "In":-2, "Ag":2, "Wa":1}),
Good("Wood", 1000, 1, 20, {"Ag", "Ga"}, {"In":-1, "Ri":-2, "Ag":6}),
Good("Vehicles", 15000, 1, 10, {"In", "Ht"}, {"In":-6, "Wa":2})
}

sicodes = {0:"tiny orbital", 1:"small moon", 2:"moon",
3:"dwarf planet", 4:"small planet", 5:"small planet", 6:"planet", 7:"planet", 8:"planet", 9:"large planet", 10:"superplanet"}

atcodes = {0:"no", 1:"a trace", 2:"a very thin, tainted", 3:"a very thin",
4:"a thin, tainted", 5:"a thin", 6:"an earth-like", 7:"a tainted earth-like", 
8:"a dense", 9:"a tainted, dense", 10:"an exotic", 11:"a corrosive",
12:"a highly corrosive", 13:"a very dense", 14:"a low-lying", 15:"an unusual"}

hycodes = {0:"less than 5%", 1:"10%", 2:"20%", 3:"30%", 4:"40%", 5:"50%", 6:"60%", 7:"70%", 8:"80%", 9:"90%", 10:"more than 95%"}

tecodes= {2:"frozen", 3:"icy", 4:"cold", 5:"cool", 6:"temperate", 7:"temperate", 8:"temperate", 9:"warm", 10:"hot", 11:"searing", 12:"boiling"}

pocodes= {0:"", 1:"", 2:"hundred ", 3:"thousand", 4:"thousand", 
5:"hundred thousand", 6:"million", 7:"million", 8:"hundred million", 
9:"billion", 10:"billion", 11:"hundred billion", 12:"trillion"}

gocodes= {0:"anarchy", 1:"control of a corporation", 2:"a direct democracy",
3:"a plutocratic oligarchy", 4:"a representative democracy",
5:"a fuedal technocracy", 6:"a colonial authority", 7:"a balkanized government",
8:"a meritocratic bureaucracy", 9:"an insulated bureaucracy",
10:"a popularly-supported dictatorship", 11:"a despotic dictatorship",
12:"a popular oligarchy", 13:"an theocratic oligarchy", 
14:"a religious autocracy", 15:"a totalitarian regime"}

cucodes= {11:"sexist culture", 12:"highly religious culture", 
13:"artistic culture", 14:"ritualistic and traditional moray", 
15:"conservative culture", 16:"xenophobic atmosphere",
21:"culture sensitive to taboos", 22:"culture of corruption",
23:"liberal culture", 24:"strict honour code", 
25:"culture highly influenced by a neighbouring world", 26:"blend of cultures", 
31:"barbaric culture", 32:"culture built in the remnants of a fallen society",
33:"decaying social order and is on the brink of societal collapse",
34:"progressive culture", 35:"long road to recovering from a recent disaster",
36:"melting pot of different cultures and species",
41:"number of tourist attractions", 42:"a violent, warlike culture",
43:"peaceful, pacifist society", 44:"monomaniacal culture",
45:"fashion-obsessed culture", 46:"active war",
51:"emphasis on space travellers in their culture",
52:"major focus on their local starports",
53:"bizarre media and communications system",
54:"unusual relationship with technology",
55:"particular obsession with geneology and age",
56:"a distinct caste system", 61:"a complicated relationship with trade",
62:"strange set of customs concerning the nobility",
63:"strange relationship with reproduction and sex",
64:"bizarre eating culture", 65:"set of unusual travel customs",
66:"conspiracy within the local government"}

tlcodes = {0:"stone-age technology", 1:"bronze-age technology",
2:"enlightnment-age technology", 3:"primitive industrial technology",
4:"simple industrial technology", 5:"simple electronic technology",
6:"primitive rocket-level technology", 7:"orbital satellite technology",
8:"inter-planetary travel techonlogy", 
9:"inter-planetary colonial technology", 
10:"early interstellar technology",  11:"jump-2 interstellar technology", 
12:"typical interstellar technology", 13:"jump-4 interstellar technology",
14:"advanced interstellar technology", 15:"cutting-edge interstellar technology"
}

lacodes = {0:"is largely non-existant", 
1:"restricts WMDs and tools of mass warfare", 
2:"restrics portable energy weapons and combat armour", 
3:"restrics military grade weapons and flak armour",
4:"restrics light assault weapons/SMGs and cloth armour",
5:"restrics personal concealable weapons and mesh armour",
6:"restricts most lethal firearms and discourages openly carrying weapons",
7:"restrics shotguns and other firearms, and discourages carrying weapons",
8:"restrics all bladed and projectile weapons, and personal armour of any kind",
9:"forbids weapons and armour of any kind"
}

consnips = {"b": ("", "h", "l", "r", "w"), 
			"c": ("", "h", "l", "r", "s", "z"),
			"d": ("", "h", "r"), "f": ("", "l", "r"), 
			"g": ("", "h", "l", "n", "r", "w"),
			"h": ("", "l", "r", "w"), "j": ("",),
			"k": ("", "h", "l", "n", "r", "w"),
			"l": ("", "l"), "m": ("", "c", "r"),
			"n": ("", "n"), "p": ("", "h", "l", "p", "r"),
			"q": ("u",), "r": ("", "h", "r"),
			"s": ("", "c", "h", "k", "l", "m", "n", "p", "qu", "r", "s",
					"t", "w", "z"), "t": ("", "h", "r", "w"),
			"v": ("",), "w": ("", "h"), "x": ("", "h"), "z": ("", "h")}
vosnips = [ "a", "e", "i", "o", "u", "y" ]

def genName():
	name = ""
	ckeys = list(consnips)
	syl = randint(2,3)
	for i in range(1,syl+1):
		if randint(1,3) == 1 and i == 1:
			name += vosnips[randint(0,len(vosnips)-1)]
		c = ckeys[randint(0,len(ckeys)-1)]
		cent = consnips[c]
		name += c + cent[randint(0,len(cent)-1)]
		if i < syl or randint(1,3) == 1:
			name += vosnips[randint(0, len(vosnips)-1)]
	return name.capitalize()

def codedesc(code, tc, te, cu, tr):
	pop = randint(1,10)
	if int(code[4], 16) in [4,7,10]: pop *= 10
#	desc = ("This world is a {0} {1} with {2} atmosphere. Oceans cover {3} of the surface." + ("It is uninhabited." if int(code[4], 16) == 0 else "It has a population of {4} {5} people living under {6}. The planet has {7} and a {8}. Law enforcement {9}. It has the following trade codes: {10}")).format(tecodes[te], sicodes[int(code[1], 16)], atcodes[int(code[2], 16)], hycodes[int(code[3], 16)], pop, pocodes[int(code[4], 16)], gocodes[int(code[5], 16)], tlcodes[int(code[8], 16)], cucodes[cu], lacodes[int(code[6], 16)], tr)
	desc = ("This world is a {0}").format(tecodes[te])
	return desc

def roll(times):
	sum = 0
	for i in range(0, times):
		sum = sum + randint(1,6)
	return sum

def portmod(po):
	if po >= 10: return 2
	elif po >= 8: return 1
	elif po <= 2: return -2
	elif po <= 4: return -1
	else: return 0

def hymod(si, at, te):
	tm = 0
	if te in [10,11]: tm = -2
	elif te > 11: tm = -6
	
	if si <= 1: return -12
	if at <=1 or (at >=10 and at <= 12):
		return at - 11 + tm
	return at - 7 + tm

def gentec(sp, si, at, hy, po, go):
	tl = roll(2)
	if sp == 'A': tl += 6
	elif sp == 'B': tl += 4
	elif sp == 'C': tl += 2
	elif sp == 'X': tl -= 4

	if si <= 1: tl += 2
	elif si <= 4: tl += 1 

	if at <= 3: tl += 1
	elif at >= 10: tl += 1

	if hy == 0: tl += 1
	elif hy == 9: tl += 1
	elif hy == 10: tl += 2

	if po <= 5 and po >= 1: tl += 1
	elif po == 8: tl += 1
	elif po == 9: tl += 2
	elif po == 10: tl += 4

	if go == 0: tl += 1
	elif go == 5: tl += 1
	elif go == 7: tl += 2
	elif go == 13: tl -= 2
	elif go == 14: tl -= 2
	
	if at in [0,1,10,15]: tl = max(8, tl)
	elif at in [2,3,13,14]: tl = max(5, tl)
	elif at in [4,7,9]: tl = max(3, tl)
	elif at == 11: tl = max(9, tl)
	elif at == 12: tl = max(10, tl)
	else: tl = max(1,tl)
	tl = min(15, tl)

	return tl
	
def gencodefromcode(code):
	si = int(code[1], 16)
	at = int(code[2], 16)
	hy = int(code[3], 16)
	po = int(code[4], 16)
	go = int(code[5], 16)
	la = int(code[6], 16)
	tl = int(code[8], 16)
	return gencodes(si, at, hy, po, go, la, tl)

def gencodes(si, at, hy, po, go, la, tl):	
	tc = {"All"}
	if at in range(4,9) and hy in range(4,8) and po in range(5,7):
		tc.add('Ag')
	if po == 0 and at == 0 and hy == 0: 
		tc.add('As')
	if po == 0 and go == 0 and la == 0: 
		tc.add('Ba')
	if at >= 2 and hy == 0: 
		tc.add('De')
	if at >= 10 and hy >= 1: 
		tc.add('Fl')
	if si in range(6,8) and at in [5,6,8] and hy in range(5,7):
		tc.add('Ga')
	if po >= 9: 
		tc.add('Hi')
	if tl >= 12: 
		tc.add('Ht')
	if at in [0,1] and hy >= 1: 
		tc.add('Ic')
	if at in [0,1,2,4,7,9] and po >= 9: 
		tc.add('In')
	if po <= 3: 
		tc.add('Lo')
	if tl <= 5: 
		tc.add('Lt')
	if at in range(0,3) and hy in range(0,3) and po >= 6:
		tc.add('Na')
	if po in range(0,6): 
		tc.add('NI')
	if at in range(2,5) and hy in range(0,3): 
		tc.add('Po')
	if at in [6,8] and po in range(6,8) and go in range(4,9):
		tc.add('Ri')
	if at == 0: 
		tc.add('Va')
	if hy >= 10: 
		tc.add('Wa')
	return tc


class World(object):
	portclass = {2:'X', 3:'E', 4:'E', 5:'D', 6:'D', 
				7:'C', 8:'C', 9:'B', 10:'B', 11:'A'}
	tempmod = { 0:0, 1:0, 2:-2, 3:-3, 4:-1, 5:-1, 6:0, 7:0, 
				8:1, 9:1, 10:2, 11:6, 12:6, 13:2, 14:-1, 15:2 }
	
	def __init__(self, code = None):
		if (code is not None):
			self.name = genName()
			self.code = code
			self.starport = code[0]
			self.temperature = roll(2)
			self.size = int(code[1], 16)
			self.atmosphere = int(code[2], 16)
			self.hydrosphere = int(code[3], 16)
			self.population = int(code[4], 16)
			self.government = int(code[5], 16)
			self.culture = roll(1)*10 + roll(1)
			self.law = int(code[6], 16)
			self.tl = int(code[8], 16)
		else:
			self.name = genName()
			self.size = max(0, min(10, roll(2) - 2))
			self.atmosphere = max(0, min(15, roll(2) - 7 + self.size)) 
			self.temperature = max(2, min(12, roll(2) + World.tempmod[self.atmosphere]))
			self.hydrosphere = max(0, min(10, roll(2) + hymod(self.size, self.atmosphere, self.temperature)))
			self.population = roll(2) - 2
			if self.population <=0:
				self.government = 0
				self.law = 0
				self.starport = 'X'
				self.tl= 0
				self.culture = 0
			else:
				self.government = max(0, min(15, roll(2) - 7 + self.population))
				self.law = max(0, min(9, roll(2) - 7 + self.government))
				self.starport = World.portclass[max(2, min(11, portmod(self.population) + roll(2)))]
				self.tl = gentec(self.starport, self.size, self.atmosphere, self.hydrosphere, self.population, self.government)
				self.culture = roll(1)*10 + roll(1)
			self.code = "{0}{1:x}{2:x}{3:x}{4:x}{5:x}{6:x}-{7:x}".format(self.starport, self.size, self.atmosphere, self.hydrosphere, self.population, self.government, self.law, self.tl).upper()
		self.tradecodes = gencodes(self.size, self.atmosphere, self.hydrosphere, self.population, self.government, self.law, self.tl)
		self.desc = codedesc(self.code, self.tradecodes, self.temperature, self.culture, self.tradecodes)
	
	def generateTradeInventory(self):
		#Buy entries
		tradegoods = set([])
		for good in legalgoods:
			if len(good.tradecodes & self.tradecodes) != 0: 
				tradegoods.add(good)
		othergoods = legalgoods - tradegoods
		tradegoods = list(tradegoods)
		
		tradegoods += sample(othergoods, roll(1))
		tradegoods.sort(key=lambda x: x.basecost)
		
		self.tradeentries = []
		last = None
		for good in tradegoods:
			if last != None and good.name == last.name:
				last.doubleQuantity()
			else:
				last = TradeEntry(good, self, True)
				self.tradeentries.append(last)

		#Sale entries
		othergoods = legalgoods - set(tradegoods)
		self.saleentries = []
		for good in othergoods:
			self.saleentries.append(TradeEntry (good, self, False))
				
	def displayInventory(self, brokerRoll):
		print("I have the following goods available for sale:")
		if self.tradeentries == None: return
		for entry in self.tradeentries:
			print(entry.toPrettyString(brokerRoll))

	def outputInventoryToCSV(self, brokerRoll):
		with open("./tradegoods_" + self.code + ".csv", "w") as f:
			f.write("Amount (T),Good Type,Purchase Cost (Cr),Sale Price (Cr)\n")
			for entry in self.tradeentries:
				f.write(entry.toCSVString(brokerRoll) + "\n")
			for entry in self.saleentries:
				f.write(entry.toCSVString(brokerRoll) + "\n")
		

def displayUsage():
	print("inventorygen.py: Tabulates a trading inventory given a planetary profile with the format <X623F64-6> and a broker roll.\n\nusage:\n" +
		"\tpython inventorygen.py <profile> <brokerroll>")

def main():
	if (len(sys.argv) == 0):
		displayUsage()
		return

	w = World(sys.argv[1])
	w.generateTradeInventory()
	if (len(sys.argv) == 1):
		pass
	else:
		brokerRoll = int(sys.argv[2])
		w.outputInventoryToCSV(brokerRoll)

main()
#print(gencodefromcode(sys.argv[1]))