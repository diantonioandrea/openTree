# openTree

import openTree
import os, sys, shutil, platform, random, requests, CLIbrary
from colorama import Fore, Back, Style
from datetime import datetime

CLIbrary.data.setting_fileExtension = ".ot"

# ---
# From an answer of Ciro Santilli on https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
import stat

def get_umask():
    umask = os.umask(0)
    os.umask(umask)

    return umask

def executable(filePath):
    os.chmod(filePath, os.stat(filePath).st_mode | ((stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & ~get_umask()))
# ---

name = "openTree"
version = "rolling"
production = True
if name not in "".join(sys.argv): # Local testing.
	production = False

system = platform.system()
path = os.getenv("PATH")

print("\n" + Back.MAGENTA + Fore.WHITE + " " + version + " " + Back.WHITE + Fore.MAGENTA + " " + name + " " + Style.RESET_ALL) if production else print("\n" + Back.WHITE + Fore.BLUE + " " + name + " " + Style.RESET_ALL)
print("Genealogy utility written in Python and built with CLIbrary")
print("Developed by " + Style.BRIGHT + Fore.MAGENTA + "Andrea Di Antonio" + Style.RESET_ALL + ", more on " + Style.BRIGHT + "https://github.com/diantonioandrea/" + name + Style.RESET_ALL)

# PATHS

if production: # Production.
	homePath = os.path.expanduser("~") + "/"
	installPath = homePath
	
	if system == "Darwin":
		installPath += "Library/" + name + "/"
	
	elif system == "Linux":
		installPath += ".local/bin/" + name + "/"

	elif system == "Windows":
		installPath += "AppData/Roaming/" + name + "/"

else: # Testing.
	installPath = str(os.getcwd()) + "/"

	reportsPath = installPath + "reports/"

dataPath = installPath + "data/"
resourcesPath = installPath + "resources/"

helpPath = resourcesPath + name + "Help.json"

# INSTALLATION

if "install" in sys.argv and production:
	try:
		currentPath = os.getcwd() + "/"
		
		if not os.path.exists(resourcesPath):
			os.makedirs(resourcesPath)

		for file in os.listdir(currentPath + "resources/"):
			shutil.copy(currentPath + "resources/" + file, resourcesPath + file)

		if system != "Windows":
			shutil.copy(currentPath + name, installPath + name)

		else:
			shutil.copy(currentPath + name + ".exe", installPath + name + ".exe")

		CLIbrary.output({"type": "verbose", "string": name.upper() + " INSTALLED SUCCESFULLY TO " + installPath, "before": "\n"})

		if name not in path:
			CLIbrary.output({"type": "warning", "string": "MAKE SURE TO ADD ITS INSTALLATION DIRECTORY TO PATH TO USE IT ANYWHERE", "after": "\n"})
		
		else:
			print("\nGoodbye.\n")
	
	except:
		CLIbrary.output({"type": "error", "string": "INSTALLATION ERROR", "before": "\n", "after": "\n"})
		sys.exit(-1)

	finally:
		sys.exit(0)

# CHECKS

try:
	# Folders.
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)

	if not os.path.exists(resourcesPath):
		raise(FileNotFoundError)

	# Resources
	resources = [helpPath]
	
	for resource in resources:
		if not os.path.exists(resource):
			raise(FileNotFoundError)
	
except:
	if production:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR, TRY REINSTALLING " + name.upper(), "after": "\n"})
	
	else:
		CLIbrary.output({"type": "error", "string": "DATA OR RESOURCES ERROR", "before": "\n", "after": "\n"})

	sys.exit(-1)

# UPDATE NOTIFICATION

if production:
	try:
		latestCommit = datetime.fromisoformat(requests.get("https://api.github.com/repos/diantonioandrea/" + name + "/commits").json()[0]["commit"]["author"]["date"].replace("Z", ""))

		if system == "Darwin":
			localVersion = datetime.fromtimestamp(os.stat(installPath + name).st_ctime)

		else:
			localVersion = latestCommit

		if localVersion < latestCommit:
			CLIbrary.output({"type": "verbose", "string": name.upper() + " HAS BEEN UPDATED, CHECK IT ON https://github.com/diantonioandrea/" + name, "before": "\n"})

		else:
			CLIbrary.output({"type": "verbose", "string": "YOU'RE ON THE LATEST COMMIT", "before": "\n"})

	except:
		CLIbrary.output({"type": "warning", "string": "COULDN'T CHECK FOR UPDATES", "before": "\n"})

# LOGIN OR REGISTER

while True:
	user = openTree.user()

	fileHandler = {"path": dataPath + user.name, "ignoreMissing": True}
	userData = CLIbrary.aLoad(fileHandler)

	if userData != None:
		if userData.protected:
			if user.login(userData.passwordHash):
				user.protected = True

			else:
				CLIbrary.output({"type": "error", "string": "LOGIN ERROR"})

				if CLIbrary.boolIn({"request": "Exit"}):
					print("\nGoodbye.\n")
					sys.exit(-1)
				else:
					continue
		
		user.tree = userData.tree
		user.registrationDate = userData.registrationDate

		try:
			if userData.darkTheme:
				CLIbrary.style.setting_darkMode = True
				user.darkTheme = userData.darkTheme
		
		except:
			user.darkTheme = False

		print("\nWelcome back, " + str(user) + "\nLast login: " + userData.lastLogin.strftime("%A, %B %d, %Y at %H:%M"))
		break

	else:
		if not CLIbrary.boolIn({"request": "User \"" + user.name + "\" does not exist. Would you like to create it?"}):
			if CLIbrary.boolIn({"request": "Exit"}):
				print("\nGoodbye.\n")
				sys.exit(-1)
			continue

		print("\nWelcome, " + str(user))
		break

print("Type \'help\' if needed\n")

# INTERFACE

# Genealogy tree.
tree = user.tree

# Prompt.
cmdHandler = {"request": "[" + user.name + "@" + name + "]"}
cmdHandler["style"] = Fore.MAGENTA

# The help that gets printed and the commands depend on the environment.
cmdHandler["helpPath"] = helpPath

while True:
	tree.sort(key = lambda node: node.birth)
	
	fileHandler["data"] = user
	CLIbrary.aDump(fileHandler)

	cmdHandler["allowedCommands"] = ["set", "password", "delete", "new"]

	if len(tree):
		cmdHandler["allowedCommands"] += ["list", "details", "edit", "remove"]

	if len(tree) > 1:
		cmdHandler["allowedCommands"] += ["connect", "disconnect"]

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]

	# EXIT

	if cmd == "exit": # Exits the program.
		break

	# SET

	if cmd == "set": # Exits the program.
		if "t" in sdOpts:
			if sdOpts["t"] == "light":
				CLIbrary.style.setting_darkMode = False
				user.darkTheme = False
				CLIbrary.output({"type": "verbose", "string": "THEME SET TO LIGHT"})
				continue
			
			elif sdOpts["t"] == "dark":
				CLIbrary.style.setting_darkMode = True
				user.darkTheme = True
				CLIbrary.output({"type": "verbose", "string": "THEME SET TO DARK"})
				continue

			else:
				CLIbrary.output({"type": "error", "string": "UNKNOWN OPTION"})
				continue
		
		else:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue

	# PASSWORD

	elif cmd == "password": # Toggles the password protection.
		if user.protected:
			if user.login(user.passwordHash):
				CLIbrary.output({"type": "verbose", "string": "PASSWORD DISABLED"})
				user.protected = False
				user.passwordHash = ""
				continue
				
			else:
				CLIbrary.output({"type": "error", "string": "WRONG PASSWORD"})
				continue

		user.register()
		CLIbrary.output({"type": "verbose", "string": "PASSWORD SET"})
		continue

	# DELETE
		
	elif cmd == "delete": # Deletes the profile.
		deletionCode = str(random.randint(10**3, 10**4-1))

		if CLIbrary.strIn({"request": "Given that this action is irreversible, insert \"" + deletionCode + "\" to delete your profile"}) == deletionCode:
			os.remove(dataPath + user.name + CLIbrary.settings.data.setting_fileExtension)

			CLIbrary.output({"type": "verbose", "string": "PROFILE DELETED"})
			break

		CLIbrary.output({"type": "error", "string": "WRONG VERIFICATION CODE"})
		continue

	# NEW

	elif cmd == "new": # Creates a new node.
		newNode = openTree.node([node.id for node in tree])
		tree.append(newNode)

		CLIbrary.output({"type": "verbose", "string": "ADDED NEW NODE"})
		continue

	elif cmd == "edit": # Edits a node.
		if "n" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue

		try:
			target = [node for node in tree if node.id == sdOpts["n"]].pop()
		
		except:
			CLIbrary.output({"type": "error", "string": "NODE NOT FOUND"})
			continue

		target.edit()
		CLIbrary.output({"type": "verbose", "string": "TARGET EDITED"})
		continue

	elif cmd == "remove": # Removes a node.
		if "n" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue

		try:
			target = [node for node in tree if node.id == sdOpts["n"]].pop()
		
		except:
			CLIbrary.output({"type": "error", "string": "NODE NOT FOUND"})
			continue

		if not CLIbrary.boolIn({"request": "Would you like to remove \"{}\"".format(target)}):
			CLIbrary.output({"type": "verbose", "string": "TARGET NOT REMOVED"})
			continue
		
		# Removes node and its connections.
		tree.remove(target)

		for parent in [parent for parent in target.parents]:
			target.removeParent(parent)

		for mate in [mate for mate in target.mates]:
			target.removeMate(mate)

		for sibling in [sibling for sibling in target.siblings]:
			target.removeSibling(sibling)

		for child in [child for child in target.children]:
			target.removeChild(child)
		
		CLIbrary.output({"type": "verbose", "string": "TARGET REMOVED"})
		continue

	# list

	elif cmd == "list": # Prints the list of nodes.
		print("List of nodes:\n\n" + "\n".join([str(tree.index(node) + 1) + ". " + str(node) for node in tree]))
		continue

	# CONNECTIONS

	elif cmd == "details": # Prints the connections of a single node.
		if "n" not in sdOpts:
			CLIbrary.output({"type": "error", "string": "MISSING OPTION"})
			continue

		try:
			target = [node for node in tree if node.id == sdOpts["n"]].pop()
		
		except:
			CLIbrary.output({"type": "error", "string": "NODE NOT FOUND"})
			continue

		print(target.__str__(long=True))
		continue

	# CONNECT

	elif cmd == "connect": # Connect nodes.
		if "n" not in sdOpts or ("c" not in sdOpts and "s" not in sdOpts and "m" not in sdOpts and "p" not in sdOpts):
			CLIbrary.output({"type": "error", "string": "MISSING OPTION(S)"})
			continue
		
		try:
			target = [node for node in tree if node.id == sdOpts["n"]].pop()
		
		except:
			CLIbrary.output({"type": "error", "string": "NODE NOT FOUND"})
			continue

		if "c" in sdOpts:
			try:
				child = [node for node in tree if node.id == sdOpts["c"]].pop()
				target.addChild(child)
				CLIbrary.output({"type": "verbose", "string": "ADDED NEW CHILD FOR " + target.id.upper() + ": " + child.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "CHILD NOT FOUND"})
				continue

		if "s" in sdOpts:
			try:
				sibling = [node for node in tree if node.id == sdOpts["s"]].pop()
				target.addSibling(sibling)
				CLIbrary.output({"type": "verbose", "string": "ADDED NEW SIBLING FOR " + target.id.upper() + ": " + sibling.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "SIBLING NOT FOUND"})
				continue

		if "m" in sdOpts:
			try:
				mate = [node for node in tree if node.id == sdOpts["m"]].pop()
				target.addMate(mate)
				CLIbrary.output({"type": "verbose", "string": "ADDED NEW MATE FOR " + target.id.upper() + ": " + mate.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "MATE NOT FOUND"})
				continue
					
		if "p" in sdOpts:
			try:
				parent = [node for node in tree if node.id == sdOpts["p"]].pop()
				target.addParent(parent)
				CLIbrary.output({"type": "verbose", "string": "ADDED NEW PARENT FOR " + target.id.upper() + ": " + parent.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "PARENT NOT FOUND"})
				continue
			
	# DISCONNECT

	if cmd == "disconnect": # Disconnect nodes.
		if "n" not in sdOpts or ("c" not in sdOpts and "s" not in sdOpts and "m" not in sdOpts and "p" not in sdOpts):
			CLIbrary.output({"type": "error", "string": "MISSING OPTION(S)"})
			continue
		
		try:
			target = [node for node in tree if node.id == sdOpts["n"]].pop()
		
		except:
			CLIbrary.output({"type": "error", "string": "NODE 8NOT FOUND"})
			continue

		if "c" in sdOpts:
			try:
				child = [node for node in tree if node.id == sdOpts["c"]].pop()
				target.removeChild(child)
				CLIbrary.output({"type": "verbose", "string": "REMOVED CHILD FOR " + target.id.upper() + ": " + child.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "CHILD NOT FOUND"})
				continue

		if "s" in sdOpts:
			try:
				sibling = [node for node in tree if node.id == sdOpts["s"]].pop()
				target.removeSibling(sibling)
				CLIbrary.output({"type": "verbose", "string": "REMOVED SIBLING FOR " + target.id.upper() + ": " + sibling.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "SIBLING NOT FOUND"})
				continue

		if "m" in sdOpts:
			try:
				mate = [node for node in tree if node.id == sdOpts["m"]].pop()
				target.removeMate(mate)
				CLIbrary.output({"type": "verbose", "string": "REMOVED MATE FOR " + target.id.upper() + ": " + mate.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "MATE NOT FOUND"})
				continue
					
		if "p" in sdOpts:
			try:
				parent = [node for node in tree if node.id == sdOpts["p"]].pop()
				target.removeParent(parent)
				CLIbrary.output({"type": "verbose", "string": "REMOVED PARENT FOR " + target.id.upper() + ": " + parent.id.upper()})
			
			except:
				CLIbrary.output({"type": "error", "string": "PARENT NOT FOUND"})
				continue

print("\nGoodbye, " + str(user) + ".\n")