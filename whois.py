import tkinter as tk
import requests as rq
import re

url = "http://dotnul.com/api/whois/"
window = tk.Tk()
urlreg = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

def lookup():
	val = window.grid_slaves(0, 1)[0].get()
	ret = re.search(urlreg, val)
	if ret == None:
		return
	val = val.split("://")[1]
	json = rq.get(url + val)
	print(json.content)

def setup_gui(win):
	win.title("Who Is Domain Checker")
	win.resizable = False
	win.geometry("500x300")
	lbl = tk.Label(win, text="Domain To Lookup : ").grid(row=0, padx=20, pady=10)
	inp = tk.Entry(win, name="domainin")
	inp.grid(row=0, column=1, padx=20, pady=10)
	go = tk.Button(win, text="Look Up", command=lookup, name="search").grid(row=0, column=2, padx=20, pady=10)

def main():
	setup_gui(window)
	window.mainloop()

if __name__ == '__main__':
	main()
