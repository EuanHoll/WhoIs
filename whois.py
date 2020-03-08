import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import requests as rq
import re
import json as js

url = "http://dotnul.com/api/whois/"
window = tk.Tk()
urlreg = '(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
bgcolour = "#222629"
btncolour = "#86c232"
btnpcolour = "#61892F"
fnt = Font(family='Fixedsys', size=8, weight='normal')
txtcolour = "#ffffff"
txtbcolour = "#6b6e70"
lsthcolour = "#474A4F"

def popup(msg):
	popup = tk.Tk()
	popup.title("Popup")
	popup.iconbitmap("logo.ico")
	w = 250
	h = 150
	sw = popup.winfo_screenwidth()
	sh = popup.winfo_screenheight()
	popup.geometry('%dx%d+%d+%d' % (w, h, (sw / 2) - (w / 2), (sh / 2) - (h / 2)))
	lbl = tk.Label(popup, text=msg, anchor="center")
	lbl.pack()
	popup.mainloop()

def lookup(frm, lst):
	val = frm.grid_slaves(0, 1)[0].get()
	ret = re.search(urlreg, val)
	if ret == None:
		return
	val = val.replace("http://", "")
	val = val.replace("https://", "")
	val = val.replace("www.", "")
	if "/" in val:
		val = val.split("/")[0]
	response = rq.get(url + val)
	json = js.loads(response.content)
	if "No match for " in json["whois"]:
		popup("The Response was invalid")
		return
	info = json["whois"].split("<br />")
	lst.delete(0, lst.size())
	i = 0
	while not "DNSSEC:" in info[i]: 
		lst.insert(i, info[i])
		i += 1

def setup_gui(win):
	win.title("Who Is Domain Checker")
	win.resizable = False
	win.iconbitmap("logo.ico")
	win.configure(background=bgcolour)
	sw = win.winfo_screenwidth()
	sh = win.winfo_screenheight()
	win.geometry('920x500+%d+%d' % ((sw / 2) - 250, (sh / 2) - 150))
	frm = tk.Frame(win, height=150, width=500, bg=bgcolour)
	lbl = tk.Label(frm, text="Domain To Lookup : ", bg=bgcolour, font=fnt, fg=txtcolour)
	lbl.grid(row=0, column=0, pady=10)
	inp = tk.Entry(frm, name="domainin", width=50, bg=txtbcolour, font=fnt, fg=txtcolour, bd=0)
	inp.grid(row=0, column=1, pady=10)
	lst = tk.Listbox(frm, name="lstbox", height=25, width=85, bg=txtbcolour, font=fnt, fg=txtcolour, selectbackground=lsthcolour)
	lst.grid(row=1, column=1)
	lst.configure(bd=0, highlightthickness=0)
	go = tk.Button(frm, text="Look Up", command= lambda: lookup(frm, lst), name="search", bg=btncolour, font=fnt, fg=txtcolour, activebackground=btnpcolour, activeforeground=txtcolour)
	go.grid(row=0, column=2, pady=10)
	frm.pack()

def main():
	setup_gui(window)
	window.mainloop()

if __name__ == '__main__':
	main()
