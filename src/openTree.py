import bcrypt, CLIbrary, random
from datetime import datetime
from colorama import Fore

# Utilities

def genCode(otherCodes: list, length: int) -> str:
	characters = list(range(48, 58)) + list(range(97, 123))

	if len(characters) ** (length) * 0.75 < len(otherCodes):
		return genCode(otherCodes, length + 1)

	while True:
		code = "".join([chr(random.choice(characters)) for _ in range(length)])

		if code not in otherCodes:
			return code

# Classes

class user:
	def __init__(self):
		self.name = CLIbrary.strIn({"request": "\nUser", "space": False})

		self.registrationDate = datetime.now()
		self.lastLogin = self.registrationDate

		self.protected = False
		self.passwordHash = ""

		self.darkTheme = False

		self.tree = []
	
	def __str__(self):
		return self.name

	def login(self, passwordHash):
		password = CLIbrary.strIn({"request": "Password", "space": False, "fixedLength": 8})
		self.passwordHash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

		return bcrypt.checkpw(password.encode(), passwordHash)

	def register(self):
		self.passwordHash = bcrypt.hashpw(CLIbrary.strIn({"request": "Password", "space": False, "verification": True, "fixedLength": 8}).encode(), bcrypt.gensalt())
		self.protected = True

class node:
	def __init__(self, ids: list) -> None:
		self.id = genCode(ids, 5)

		self.parents = set()
		self.mates = set()
		self.siblings = set()
		self.children = set()

		while True:
			self.name = CLIbrary.strIn({"request": "Node's name"}) if CLIbrary.boolIn({"request": "Is node's birth name known?"}) else "?"
			self.surname = CLIbrary.strIn({"request": "Node's surname"}) if CLIbrary.boolIn({"request": "Is node's birth surname known?"}) else "?"

			if self.name == self.surname == "?":
				CLIbrary.output({"type": "error", "string": "ONE OF THOSE INFORMATION MUST BE KNOWN", "after": "\n"})
			
			else:
				break

		self.birth = CLIbrary.dateIn({"placeholders": True, "request": "Node's birth date"}) if CLIbrary.boolIn({"request": "Is node's birth date known?"}) else "?"
		self.death = (CLIbrary.dateIn({"placeholders": True, "request": "Node's death date"}) if CLIbrary.boolIn({"request": "Is node's death date known?"}) else "?") if CLIbrary.boolIn({"request": "Is node dead?"}) else ""

	def edit(self) -> None:
		self.name = CLIbrary.strIn({"request": "Node's name"}) if CLIbrary.boolIn({"request": "Edit {}'s name [{}]".format(self.id, self.name)}) else self.name
		self.surname = CLIbrary.strIn({"request": "Node's surname"}) if CLIbrary.boolIn({"request": "Edit {}'s surname [{}]".format(self.id, self.surname)}) else self.surname

		self.birth = CLIbrary.dateIn({"placeholders": True, "request": "Node's birth date"}) if CLIbrary.boolIn({"request": "Edit {}'s birth date [{}]".format(self.id, self.birth)}) else self.birth

		if not self.death:
			self.death = (CLIbrary.dateIn({"placeholders": True, "request": "Node's death date"}) if CLIbrary.boolIn({"request": "Edit {}'s death date [{}]".format(self.id, self.death)}) else self.death) if CLIbrary.boolIn({"request": "Is node dead?"}) else ""
		
		else:
			self.death = CLIbrary.dateIn({"placeholders": True, "request": "Node's death date"}) if CLIbrary.boolIn({"request": "Edit {}'s death date [{}]".format(self.id, self.death)}) else self.death

	def __str__(self, short=False, long=False) -> str:
		name = " ".join([word[0].upper() + word[1:] for word in self.name.split(" ")])
		surname = " ".join([word[0].upper() + word[1:] for word in self.surname.split(" ")])

		connections = ""

		if long:
			connections += "\n\t\u2022 Parents\n\t\t" + "\n\t\t".join(str(parent) for parent in self.parents) if len(self.parents) else ""
			connections += "\n\t\u2022 Mates\n\t\t" + "\n\t\t".join(str(mate) for mate in self.mates) if len(self.mates) else ""
			connections += "\n\t\u2022 Siblings\n\t\t" + "\n\t\t".join(str(sibling) for sibling in self.siblings) if len(self.siblings) else ""
			connections += ("\n\t\u2022 Children\n\t\t" + "\n\t\t".join([str(child) + (" [" + ", ".join([parent.__str__(short=True) for parent in child.parents - {self}]) + "]" if child.parents - {self} != set() else "") for child in self.children])) if len(self.children) else ""

		return "(" + Fore.CYAN + self.id + Fore.RESET + ") " + surname + ", " + name + ((" [" + self.birth + " - " + self.death + "]" if self.death else " [" + self.birth + "]") + connections if not short else "")

	# Parents.
	def addParent(self, parent: "node") -> None:
		self.parents.add(parent)
		parent.children.add(self)

	def removeParent(self, parent: "node") -> None:
		self.parents.remove(parent)
		parent.children.remove(self)

	# Mates.
	def addMate(self, mate: "node") -> None:
		self.mates.add(mate)
		mate.mates.add(self)

	def removeMate(self, mate: "node") -> None:
		self.mates.remove(mate)
		mate.mates.remove(self)

	# Siblings.
	def addSibling(self, sibling: "node") -> None:
		self.siblings.add(sibling)
		sibling.siblings.add(self)

	def removeSibling(self, sibling: "node") -> None:
		self.siblings.remove(sibling)
		sibling.siblings.remove(self)

	# Children.
	def addChild(self, child: "node") -> None:
		self.children.add(child)
		child.parents.add(self)

	def removeChild(self, child: "node") -> None:
		self.children.remove(child)
		child.parents.remove(self)