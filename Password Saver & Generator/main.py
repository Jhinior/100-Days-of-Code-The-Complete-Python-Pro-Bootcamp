from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_enter.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
      password_list.append(random.choice(letters))

    for char in range(nr_symbols):
      password_list += random.choice(symbols)

    for char in range(nr_numbers):
      password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
      password += char

    password_enter.insert(0,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    new_data = {website_enter.get() : {
        "email" : username_enter.get(),
        "password" : password_enter.get()
    }

    }
    if len(website_enter.get()) != 0 and len(username_enter.get()) != 0 and len(password_enter.get()) != 0:
        is_ok =messagebox.askokcancel(title=website_enter.get(),
                                      message=f"This the data you "
                                      f"entered: \nEmail: {username_enter.get()}\n"
                                      f"Password: {password_enter.get()} \nConfirm to save.")
        if is_ok:
            with open("data.json", "r") as file:
                try:
                    data = json.load(file)
                    data.update(new_data)
                except:
                    with open("data.json", "w") as file:
                        json.dump(new_data, file, indent=4)
                else:
                    with open("data.json", "w") as file:
                        json.dump(data, file, indent=4)
            website_enter.delete(0,END)
            password_enter.delete(0, END)

    else:
        messagebox.showinfo(title="Error", message="Messing information needs to fill")

def search():
    with open("data.json", "r") as file:
        data = json.load(file)
        try:
            pop_out = data[website_enter.get()]
        except KeyError:
            pop_out = f"Sorry, there is no saved data for {website_enter.get()}"
            messagebox.showinfo(title=website_enter.get(), message=f"{pop_out}")
        else:
            messagebox.showinfo(title=website_enter.get(),message=f"{pop_out}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50,pady= 50)
canvas = Canvas(width=200,height=200, highlightthickness= 0)
image = PhotoImage(file = "logo.png")
canvas.create_image(100,100, image = image)
canvas.grid(column= 1, row=0)
#UI Labels:
website = Label(text="Website:")
website.grid(column= 0, row=1)
username = Label(text="Email/Username:")
username.grid(column= 0, row=2)
password = Label(text="Password:")
password.grid(column= 0, row=3)
#UI Entery:
website_enter = Entry(width=32)
website_enter.grid(column= 1, row=1)
input = website_enter
website_enter.focus()
username_enter = Entry(width=50)
username_enter.insert(0,"mahmoud@gmail.com")
username_enter.grid(column= 1, row=2,columnspan = 2)
password_enter = Entry(width=32)
password_enter.grid(column= 1, row=3)

#Ui Buttons:
generate = Button(text= "Generate Password",width= 14,command= generate_password)
generate.grid(column= 2, row=3)
search = Button(text= "Search",width= 14,command=search)
search.grid(column= 2, row=1)
add = Button(text="Add",width= 43,command= save)
add.grid(column= 1, row=5,columnspan = 2)





window.mainloop()