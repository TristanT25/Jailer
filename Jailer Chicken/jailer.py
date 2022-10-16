import json
import random
import string
import os
from tkinter import *
import tkinter.messagebox
from twilio.rest import Client
from PIL import Image, ImageTk
import encrypt
import decrypt

#Setting environment
account_sid = "ACe8de9117eb5ca33afb8f1d0772600797"
auth_token = "3537b5966881b74c7eaa9e0b5041dd6f"
client = Client(account_sid, auth_token)


dir = os.path.dirname(__file__)
data = os.path.join(dir, 'data.json')
win = Tk()

#-----------------GLOBAL FUNCTIONS
# Generate Password
def generatePass(length):
    element = string.ascii_letters + string.punctuation
    password = ''.join(random.choice(element) for i in range(length))

    return password

# Retrieve Password
def retrieve(app):
    temp = {}

    # Load JSON into temp
    with open(data, 'r') as json_file:
        temp = json.load(json_file)

    return temp[app]

# Update/Add Password
def updatePass(app, length):
    temp = {}

    # Load JSON into temp
    with open(data, 'r') as json_file:
        temp = json.load(json_file)

    # Generate password and add to dictionary
    temp[app] = generatePass(length)

    # Write temp to JSON
    with open(data, 'w') as fp:
        json.dump(temp, fp)

# Delete Password
def deletePass(app):
    temp = {}

    # Load JSON into temp
    with open(data, 'r') as json_file:
        temp = json.load(json_file)

    # Delete password
    temp.pop(app)

    # Write temp to JSON
    with open(data, 'w') as fp:
        json.dump(temp, fp)

# Print All
def printPass():
    temp = {}
    finalString = ''
    # Load JSON into temp
    with open(data, 'r') as json_file:
        temp = json.load(json_file)

    if len(temp) == 0:
        raise Exception('Empty')

    # Print all password
    for key, value in temp.items():
        finalString += f"{key}: {value}\n"
    return finalString
#-----------------GLOBAL FUNCTIONS

key = ''.join(random.choice(string.digits) for i in range(6))
print(key)
# Send through sms
message = client.messages.create(
  body=key,
  from_='+18649713941',
  to='+17852266513'
)

#-----------------UI COMPONENT
#-----------------MENU
def menu(e):
    # decrypt data.json
    decrypt.decrypt()

    # canvas reset
    for i in win.winfo_children():
        i.destroy()

    #-----------------FUNCTIONS
    def retrievePass(e):
        app = entry.get()
        try:
            data = retrieve(app)
            tkinter.messagebox.showinfo(title='Password', message=data)
            entry.delete(0, 'end')
        except:
            tkinter.messagebox.showinfo(title='Password', message='App not found')
            entry.delete(0, 'end')

    def updateP(e):
        app = entry.get()
        try:
            data = retrieve(app)
            updatePass(app, 25)
            tkinter.messagebox.showinfo(title='Password', message='Updated!\n' + 'new pass: ' + data)
            entry.delete(0, 'end')
        except:
            updatePass(app, 25)
            data = retrieve(app)
            tkinter.messagebox.showinfo(title='Password', message='New App Added!\n' + 'pass: ' + data)
            entry.delete(0, 'end')

    def deleteP(e):
        app = entry.get()
        try:
            deletePass(app)
            tkinter.messagebox.showinfo(title='Password', message=app + ' deleted!')
            entry.delete(0, 'end')
        except:
            tkinter.messagebox.showinfo(title='Password', message='App not found!')
            entry.delete(0, 'end')

    def printP(e):
        try:
            passwords = printPass()
            tkinter.messagebox.showinfo(title='Password', message=passwords)
            entry.delete(0, 'end')
        except:
            tkinter.messagebox.showinfo(title='Password', message='Password manager is empty!')
            entry.delete(0, 'end')
    #-----------------FUNCTIONS

    #-----------------CANVAS OBJECT
    canvas = Canvas(
        master=win,
        bg='black',
        borderwidth=0,
        highlightthickness=0
    )
    canvas.pack(fill='both', expand=True)
    canvas.create_image(
        0, 0,
        image=bgActiveImage,
        anchor='nw'
    )
    entry = Entry(
        master=canvas, 
        background='white', fg='black', selectbackground='black', selectforeground='white', 
        borderwidth=0, highlightthickness=0, 
        font='SegoeUIBlack 16',
        justify=CENTER
    )
    entryBox = canvas.create_window(
        43, 138,
        anchor='nw',
        window=entry,
        width=222,
        height=33,
    )
    retrieveButton = canvas.create_image(
        43, 192,
        image=retrieveImage,
        anchor='nw'
    )
    updateButton = canvas.create_image(
        156, 192,
        image=updateImage,
        anchor='nw'
    )
    deleteButton = canvas.create_image(
        43, 235,
        image=deleteImage,
        anchor='nw'
    )
    printButton = canvas.create_image(
        156, 235,
        image=printImage,
        anchor='nw'
    )
    #-----------------CANVAS OBJECT

    # binding
    canvas.tag_bind(retrieveButton, '<Button>', retrievePass)
    canvas.tag_bind(updateButton, '<Button>', updateP)
    canvas.tag_bind(deleteButton, '<Button>', deleteP)
    canvas.tag_bind(printButton, '<Button>', printP)
#-----------------MENU

#-----------------AUTH
def auth(e):
    # canvas reset
    for i in win.winfo_children():
        i.destroy()

    #-----------------FUNCTIONS
    def checkPass(e):
        global key
        if(entry.get() == key):
            menu('')
        else:
            entry.delete(0, 'end')
            tkinter.messagebox.showerror(title='ERROR', message='WRONG KEY')
    #-----------------FUNCTIONS
    
    #-----------------CANVAS OBJECT
    canvas = Canvas(
        master=win,
        bg='black',
        borderwidth=0,
        highlightthickness=0
    )
    canvas.pack(fill='both', expand=True)
    canvas.create_image(
        0, 0,
        image=bgImage,
        anchor='nw'
    )

    entry = Entry(
        master=canvas, 
        background='white', fg='black', selectbackground='black', selectforeground='white', 
        borderwidth=0, highlightthickness=0, 
        font='SegoeUIBlack 16',
        justify=CENTER
    )
    entryBox = canvas.create_window(
        43, 138,
        anchor='nw',
        window=entry,
        width=222,
        height=33,
    )

    enter = canvas.create_image(
        97, 192,
        image=enterImage,
        anchor='nw'
    )
    #-----------------CANVAS OBJECT

    # binding
    canvas.tag_bind(enter, '<Button>', checkPass)
#-----------------AUTH



#-----------------WINDOW
win.geometry('500x300')
win.resizable(False,False)
win.title('Jailer')
#-----------------WINDOW

#-----------------RESOURCES
#--AUTH RESOURCES--
bgImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/imageBg.png')))
enterImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/ImageEnter.png')))

#--MENU RESOURCES--
bgActiveImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/imageBgActive.png')))
retrieveImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/ImageRetrieve.png')))
updateImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/ImageUpdate.png')))
deleteImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/ImageDelete.png')))
printImage = ImageTk.PhotoImage(Image.open(os.path.join(dir, 'resource/ImagePrint.png')))
#-----------------RESOURCES

auth('')
win.mainloop()
encrypt.encrypt()
#-----------------UI COMPONENT

