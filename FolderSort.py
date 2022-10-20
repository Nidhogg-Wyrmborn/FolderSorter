## PLAN
#
# Allow user to choose whether to search for keywords in folder and specify folder and keyword/s

# import -
import easygui
import os
import shutil
import sys
import hashlib
import random
import requests

# import - as -


# from - import -
from glob import glob
from threading import Thread
from git import Repo

# functions


# class
#print("starting main program")
class main:
	def __init__(self):
		self.version = "0.7.0"
		v1, v2, v3 = self.version.split(".")
		print(self.version)
		print(f"v1: {v1}, v2: {v2}, v3: {v3}")
		self.v1 = v1
		self.v2 = v2
		self.v3 = v3
		self.choices = ["select a folder",
						"state keyphrases",
						"select save location",
						"search",
						"search recent"]
		update, version = self.update()
		if update:
			yesno = ["yes", "no"]
			c = easygui.buttonbox("update available, would you like to update?", choices = yesno)
			if c == yesno[0]:
				f = self.performUpdate(version)
				if f:
					easygui.msgbox("update complete, restarting program")
					Thread(target=self.cleanup, daemon=False).start()
					#print("quit")
					quit()
				if not f:
					easygui.msgbox("update failed, try to reconnect to the internet.\n\nfor the meantime the current update will still work.")

		self.GUI()

	def cleanup(self):
		shutil.move("./tmp/FolderSort.exe", "./FolderSort.exe")
		os.system(f"FolderSort.exe")

	def update(self):
		## check for update, for test cases it will say update until the test.dat file is reset
		updateUrl = "https://pastebin.com/raw/K746829t"
		content = requests.get(updateUrl, verify=False)
		version = content.text
		print(version)
		v1, v2, v3 = version.split(".")
		if v1 > self.v1:
			return True, version
		if v1 <= self.v1:
			if v2 > self.v2:
				return True, version
			if v2 <= self.v2:
				if v3 > self.v3:
					return True, version
				if v3 <= self.v3:
					return False, version

	def performUpdate(self,version):
		## pretend to do the update (show a progress bar based on content downloaded and then return true for finish and false for fail)
		try:
			print("making tmp")
			os.mkdir("./tmp")
			print("set url")
			url = f"https://raw.github.com/Nidhogg-Wyrmborn/FolderSorterMain/main/{version}/FolderSort.exe"
			print("open url as stream")
			with requests.get(url, stream=True, verify=False) as r:
				print("raise for status")
				r.raise_for_status()
				print("open file as f")
				with open("./tmp/FolderSort.exe", 'wb') as f:
					print("create counter")
					num = 0
					for chunk in r.iter_content(chunk_size=8192):
						print(f"opening chunk {chunk}")
						print("writing chunk")
						f.write(chunk)
						print("chunk written")
						num += 1
						print(f"finished chunk No. {num}")
			return True
		except Exception as e:
			print(e)
			return False

	def GUI(self):
		folder = None
		Keywords = None
		SaveLocation = None
		while True:
			method = easygui.choicebox("please select an option", choices = self.choices)
			if method == self.choices[0]:
				folder = self.selectFolder()

			if method == self.choices[1]:
				Keywords = self.stateKWord()

			if method == self.choices[3]:
				easygui.msgbox(self.search(folder, Keywords, SaveLocation))

			if method == self.choices[2]:
				SaveLocation = easygui.diropenbox(msg="select a folder to save to", title="save to", default=None)

			if method == self.choices[4]:
				with open("recent.settings", 'r') as f:
					recent = f.readlines()
					f.close()

				print(recent)

				for i in range(len(recent)):
					recent[i] = recent[i].replace("\n", '')

				print(recent)

				recent.reverse()

				print(recent)

				if len(recent) < 2:
					easygui.msgbox("not enough history, please create a new search paramter first")
					continue
				ch = easygui.choicebox("please select one of your recent choices", choices = recent)

				if ch == None:
					continue

				folder, Keywords = ch.split("    <SEP>    ")
				Keywords = Keywords.split("|")
				easygui.msgbox(self.search(folder, Keywords, SaveLocation))

			if method == None:
				print("Quitting")
				break

	def selectFolder(self, msg="please select a Folder"):
		Folder = easygui.diropenbox(msg=msg, title="Folder to search", default=None)
		return Folder

	def stateKWord(self, msg="Please enter your keyphrases, use a \"|\" to separate phrases"):
		KWords = easygui.enterbox(msg).lower().split("|")
		#print(type(KWords))
		return KWords

	def search(self, folder, Keywords, SaveLocation):
		if SaveLocation == None:
			easygui.msgbox(f"no save location set, default is\nC:/Users/{os.getlogin()}/Desktop/Sorted")
			SaveLocation = f"C:/Users/{os.getlogin()}/Desktop/Sorted"
		if folder == None:
			folder = self.selectFolder(msg="no folder has been specified, please select a folder")
		if Keywords == None:
			Keywords = self.stateKWord(msg="no keyphrase has been specified, please enter your keyphrases. use a \"|\" to separate phrases")

		if not os.path.exists("./recent.settings"):
			with open("recent.settings", 'w') as f:
				f.close()

		with open("recent.settings", 'a') as f:
			f.write(f"{folder}    <SEP>    {'|'.join(Keywords)}\n")

		output = {}
		for word in Keywords:
			tmpoutput = list()
			for (dirpath, dirnames, filenames) in os.walk(folder):
				ftest = [os.path.join(dirpath,file) for file in filenames]
				if len(ftest) == 1:
					if word in os.path.basename(ftest[0]).lower():
						#print(f"[!!!] hasTestWord: {test}")
						tmpoutput.append(ftest)
						continue
				#print(f"test: {test}")
				for tst in range(len(ftest)):
					#print(f"tst: {tst}")
					if word in os.path.basename(ftest[tst]).lower():
						#print(f"[***] hasTestWord: {tst}")
						tmpoutput.append(ftest[tst])
						#print(f"[OUT] tmpoutput: {tmpoutput}")
			output[word] = tmpoutput

		#print(output)

		if not os.path.exists(SaveLocation):
			os.mkdir(f"{SaveLocation}")

		for word in Keywords:
			if not os.path.exists(f"{SaveLocation}/{os.path.basename(folder)} - {word}"):
				os.mkdir(f"{SaveLocation}/{os.path.basename(folder)} - {word}")

		numresult = 0
		for word in Keywords:
			#print(output[word])
			if isinstance(output[word], list):
				for i in range(len(output[word])):
					if isinstance(output[word][i], list):
						shutil.copy(output[word][i][0], f"{SaveLocation}/{os.path.basename(folder)} - {word}")
						numresult += 1
					if not isinstance(output[word][i], list):
						shutil.copy(output[word][i], f"{SaveLocation}/{os.path.basename(folder)} - {word}")
						numresult += 1
			if not isinstance(output[word], list):
				shutil.copy(output[word][0], f"{SaveLocation}/{os.path.basename(folder)} - {word}")
				numresult += 1

		return f"Your files have been saved to {SaveLocation}\n\nThere was a total of {numresult} results"


# program

if __name__ == '__main__':
	main()