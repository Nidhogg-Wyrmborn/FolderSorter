import shutil
import sys
import os
import requests
import tkPBar as tkPB
from threading import Thread

def cleanup():
	shutil.move("./tmp/FolderSort.exe", "./FolderSort.exe")
	shutil.rmtree("tmp")
	os.system(f"FolderSort.exe")

def update():
	## check for update, for test cases it will say update until the test.dat file is reset
	updateUrl = "https://pastebin.com/raw/K746829t"
	content = requests.get(updateUrl, verify=False)
	version = content.text
	#print(version)
	return version

def performUpdate(version):
	## pretend to do the update (show a progress bar based on content downloaded and then return true for finish and false for fail)
	try:
		#print("making tmp")
		os.mkdir("./tmp")
		#print("set url")
		url = f"https://raw.github.com/Nidhogg-Wyrmborn/FolderSorterMain/main/{version}/FolderSort.exe"
		filesize = requests.get(url, stream=True, verify=False).headers['Content-length']
		print(filesize)
		#print("open url as stream")
		pbar = tkPB.tkProgressbar(int(filesize), Determinate=True)
		with requests.get(url, stream=True, verify=False) as r:
			#print("raise for status")
			r.raise_for_status()
			#print("open file as f")
			prev = 0
			with open("./tmp/FolderSort.exe", 'wb') as f:
				#print("create counter")
				num = 0
				for chunk in r.iter_content(chunk_size=8192):
					#print(f"opening chunk {chunk}")
					#print("writing chunk")
					f.write(chunk)
					#print("chunk written")
					num += 1
					#print(f"finished chunk No. {num}")
					pbar.update(len(chunk))
					current = prev + (len(chunk)/int(filesize))*100
					prev = current
					pbar.description(Desc=f"%{round(current, 1)}")
		pbar.root.destroy()
		print(num)
		print(num*8192)
		return True
	except Exception as e:
		print(e)
		shutil.rmtree("tmp")
		return False

version = update()
performUpdate(version)
cleanup()