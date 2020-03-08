import tkinter as tk
import tkinter.ttk as ttk
from tkinter.font import Font
import requests as rq
import re
import json as js
import webbrowser as wb

url = "http://dotnul.com/api/whois/"
window = tk.Tk()
urlreg = '(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)'
bgcolour = "#222629"
btncolour = "#86c232"
btnpcolour = "#61892F"
fnt = Font(family='Fixedsys', size=8, weight='normal')
txtcolour = "#ffffff"
txtbcolour = "#6b6e70"
lsthcolour = "#474A4F"

def reportpopup(og_url):
	print("hey")

def create_mailto(email, domain, webaddress):
	url = "mailto:" + email
	url += "?subject=Possible abuse at " + domain + "&"
	url +="body=Hello,\n\nI have recently come across what seems to be a spam/abusive" + \
		" URL which seems to have been\npurchased  from your company. The domain name is " + domain + \
		" . The web address I came across which appeared to be spam/abusive was " + webaddress + \
		" .\n\nKind Regards\n"
	url = url.replace(' ', '%20')
	url = url.replace('\n', '%0D%0A')
	return url

def reportabuse(lst):
	ary = lst.get(0, 'end')
	if (len(ary) == 0):
		return
	wb.open(create_mailto("e", "e", "e"), new=1)

def popup(msg):
	popup = tk.Tk()
	popup.title("Popup")
	popup.iconbitmap("logo.ico")
	popup.configure(bg=bgcolour)
	w = 350
	h = 150
	sw = popup.winfo_screenwidth()
	sh = popup.winfo_screenheight()
	popup.geometry('%dx%d+%d+%d' % (w, h, (sw / 2) - (w / 2), (sh / 2) - (h / 2)))
	lbl = tk.Label(popup, text=msg, anchor="center", bg=bgcolour, font=fnt, fg=txtcolour)
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
		popup("The response or domain was invalid")
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
	win.geometry('920x500+%d+%d' % ((sw / 2) - 460, (sh / 2) - 250))
	frm = tk.Frame(win, height=150, width=500, bg=bgcolour)
	lbl = tk.Label(frm, text="Domain To Lookup : ", bg=bgcolour,
		font=fnt, fg=txtcolour)
	lbl.grid(row=0, column=0, pady=10)
	inp = tk.Entry(frm, name="domainin", width=50, bg=txtbcolour,
		font=fnt, fg=txtcolour, bd=0)
	inp.grid(row=0, column=1, pady=10)
	lst = tk.Listbox(frm, name="lstbox", height=25, width=85, bg=txtbcolour,
		font=fnt, fg=txtcolour, selectbackground=lsthcolour)
	lst.grid(row=1, column=1)
	lst.configure(bd=0, highlightthickness=0)
	go = tk.Button(frm, text="Look Up", command= lambda: lookup(frm, lst),
		name="search", bg=btncolour,
		font=fnt, fg=txtcolour, activebackground=btnpcolour,
		activeforeground=txtcolour)
	go.grid(row=0, column=2, pady=10)
	report = tk.Button(frm, text="Report", command=lambda: reportabuse(lst),
		name="report", width=20, bg=btncolour, font=fnt,
		fg=txtcolour, activebackground=btnpcolour,
		activeforeground=txtcolour)
	report.grid(row=2, column=1, pady=10)
	frm.pack()

def main():
	setup_gui(window)
	window.mainloop()

if __name__ == '__main__':
	main()
