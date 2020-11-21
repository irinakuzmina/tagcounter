
from tkinter import *
import requests
from lxml import html
from collections import Counter
import pickle as cPickle
import sqlite3
import datetime
import logging
import click


#def main():
#    print("I'm a beautiful CLI ✨")

############################

@click.command()
@click.argument('url')
@click.option('--get', is_flag=True,  help='Get tags')
@click.option('--view', is_flag=True,  help='View tags')
def geturl(get,view, url):

    if view:
     text.delete(1.0, END)
     conn = sqlite3.connect('example.db')
     t = conn.cursor()
     t.execute("SELECT url, date, tagscount from tags")
     print  (t.fetchall())

    if get:
     page = requests.get(url)
     tree = html.fromstring(page.content)

     all_elms = tree.cssselect('*')
     all_tags = [x.tag for x in all_elms]

     c = Counter(all_tags)
     print('all:', len(all_elms), 'span:', c['span'])

     for e in c:
      print('{}: {}'.format(e, c[e]))


     from tld import get_fld
     pdata = cPickle.dumps(c, cPickle.HIGHEST_PROTOCOL)

     conn = sqlite3.connect('example.db')

     now = datetime.datetime.now()

     t = conn.cursor()
     t.execute('''CREATE TABLE if not exists tags
             (sitename text, url text, date text, tagsdata blob, tagscount text)''')
     t.execute("INSERT INTO tags VALUES(?, ?, ?, ?, ?)", (get_fld(url), url, now.strftime("%d-%m-%Y %H:%M:%S"), sqlite3.Binary(pdata), str(c)))

     conn.commit()
     conn.close()

     logging.basicConfig(filename='HTML tags counter.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
     logging.info(get_fld(url))

############################




window = Tk()
window.title("HTML tags counter")
window.geometry("700x400")
def get_text():
     s = entry.get()
     url=s
     page = requests.get(url)
     tree = html.fromstring(page.content)

     all_elms = tree.cssselect('*')
     all_tags = [x.tag for x in all_elms]

     c = Counter(all_tags)
     print('all:', len(all_elms), 'span:', c['span'])

     for e in c:
      print('{}: {}'.format(e, c[e]))

     from tld import get_fld
     pdata = cPickle.dumps(c, cPickle.HIGHEST_PROTOCOL)

     conn = sqlite3.connect('example.db')

     now = datetime.datetime.now()

     t = conn.cursor()
     t.execute('''CREATE TABLE if not exists tags
             (sitename text, url text, date text, tagsdata blob, tagscount text)''')
     t.execute("INSERT INTO tags VALUES(?, ?, ?, ?, ?)", (get_fld(url), url, now.strftime("%d-%m-%Y %H:%M:%S"), sqlite3.Binary(pdata), str(c)))
  # t.execute("Drop table tags")

     conn.commit()
     conn.close()

     logging.basicConfig(filename='HTML tags counter.log', filemode='a', format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)
     logging.info(get_fld(url))

def show_fromdb():
    text.delete(1.0, END)
    conn = sqlite3.connect('example.db')
    t = conn.cursor()
    t.execute("SELECT url, date, tagscount from tags")
    text.insert(1.0, t.fetchall())

'''
    for row in t:
     data = cPickle.loads(int(row['tagsdata']))
    print(data)
    conn.close()
'''

# Deserialize the BLOB to a Python object - # pickle.loads() needs a
# bytestring.
#point = pickle.loads(str(serialized_point))
#print "got point back from database", point

statusvar = StringVar()
statusvar.set("Ready")

l1 = Label(text="Insert site URL here:", font="Arial 10")
entry = Entry(width=90)
button1 = Button(window, text='Upload', command=get_text)
button2 = Button(window, text='Show from DB', command=show_fromdb)
text = Text(height=15, width=90, wrap=WORD)
statusbar = Label(window, textvariable=statusvar, relief=SUNKEN, anchor="w")


l1.pack()
entry.pack()
button1.pack()
button2.pack()
text.pack()
statusbar.pack(side=BOTTOM, fill=X)



window.mainloop()


############################
#if __name__ == "__main__":
 #   geturl()
############################

