import convert
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from bs4 import BeautifulSoup

def check_for_errors(URL, title):
    if URL == '' or title == '':
        messagebox.showerror("Warning", "You must enter a complete URL and a file title.")
        return False
    else:
        return True

        
def scrape(URL, title):

    # run check for errors function and assign to error_free
    error_free = check_for_errors(URL, title)

    if error_free:
        try:
            soup = get_response_object(URL)

            # call this function to let the user know the audio file is being created. 
            creating_file_message()

            # list to hold all elements to be read
            contents_to_read = ["The headline reads: "]

            # get the parent element whose children you want to scrape
            main_parent_element = get_desired_parent(soup, "body")
    
            # get the article headline
            headline = main_parent_element.h1.text

            # get the article P tags
            main_text = get_multiple_elements(soup, "p")
            
            # append all above elements to contents_to_read list
            contents_to_read.append(headline)
            contents_to_read.append('. ')
            contents_to_read.append(main_text)

            # make the contents_to_read list into a string
            read_this_string = ''.join(contents_to_read)

        except:
            messagebox.showinfo("URL Error", "There was a problem retrieving your URL. Please check for accuracy.")
            return

        # call the convert to mp3 function from convert import
        convert.create_mp3(read_this_string, title)

        

# create the beautiful soup object out of the user URL
def get_response_object(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    return soup

# function for returning one particular elements
def get_one_element(soup_object, element):
    return soup_object.find(element)


# function for returning a list of elements
def get_multiple_elements(soup_object, elements):
    text_of_elements_list = []
    element_list = soup_object.find_all(elements)
    for element in element_list:
        text_of_elements_list.append(element.text)
    text_of_elements_list_to_str = ' '.join(text_of_elements_list)
    return text_of_elements_list_to_str

# a function to grab the correct parent. For example, deciding which header contains the article headline
def get_desired_parent(soup_object, element):
    list_of_matches = soup_object.find_all(element)
    if len(list_of_matches) == 1:
        return list_of_matches[0]
    else:
        return list_of_matches[1]


def creating_file_message():
    background_label.config(compound=tk.CENTER, text="Your audio file is being created. It will play shortly....", font=('Helvitica', 30), fg='white')
    canvas.update()
    

# function for deleting the entries on the button click
def delete_data():
    article_name_entry.delete(0, 'end')
    url_entry.delete(0, 'end')

# the code from here to the end of the file creates the gui. 

# main window
root = tk.Tk()
root.geometry("1200x1200")

# canvas to serve as main parent
canvas = tk.Canvas(root, bg="#2e4073")
canvas.place(relwidth=1, relheight=1)

# Creates the background image inside a label on the canvas
background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(canvas, image = background_image)
background_label.place(relwidth=1, relheight=1)

# Label widgt for Title
title_label = tk.Label(canvas, text="Article Reader", bg="#304682", fg="white", font=("Helvitica", 40))
title_label.place(relx=.37, rely=.05)

# frame in which to place the URL entry widget
url_frame = tk.Frame(canvas, bg='#2e4073', bd=5)
url_frame.place(relx=.5, rely=.2, relheight=.1, relwidth=.95, anchor='n' )

# label indicating URL placement
url_label = tk.Label(url_frame, text="Enter Full URL:", bg='#2e4073', fg='white', font=('Helvitica', 14))
url_label.place(anchor='w', rely=.5)

# entry widget for URL
url_entry = tk.Entry(url_frame, font=('Helvitica', 15))
url_entry.place(relx=.13, rely=.25, relheight=.5, relwidth=.85)

# frame for article name
article_name_frame = tk.Frame(canvas, bg='#2e4073')
article_name_frame.place(relx=.25, rely=.34, relheight=.1, relwidth=.5)

# Label for article name frame
article_name_label = tk.Label(article_name_frame, text="Provide an Article Title:", bg='#2e4073', fg='white', font=('Helvitica', 14))
article_name_label.place(relx=.01, rely=.28)

# Entry for article name
article_name_entry = tk.Entry(article_name_frame, font=('Helvitica', 15))
article_name_entry.place(relx=.35, rely=.24, relheight=.5, relwidth=.5)

# button for creating audio file. Excecutes the scrape code object on click. 
button = tk.Button(canvas, text="Create Audio", bg='#5b735f', fg='white', font=('Helivitca', 18), relief="raised", command= lambda : [scrape(url_entry.get(), article_name_entry.get()), delete_data(), background_label.config(text='')])
button.place(relx=.4, rely=.6, relheight=.07, relwidth= .15)



root.mainloop()




