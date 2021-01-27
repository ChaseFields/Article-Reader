from gtts import gTTS
import os
import getpass

# returns the path to the user's desktop
def handle_file_location():
    user = getpass.getuser()
    if user == 'Chase':
        path = "C:\\Users\\" + user + "\\OneDrive" + "\\Desktop\\"
    else:
        path = "C:\\Users\\" + user + "\\Desktop\\"
    return path

# creates the mp3 out of the text passed into it in scrape.py
def create_mp3(text_to_read, title):

    # Set english language as a constant
    LANGUAGE = 'en'

    # pass in the scraped content as a string to be read. 

    output = gTTS(text=text_to_read, lang=LANGUAGE)

    # creates the mp3 file and saves it to the user desktop folder
    file_name = create_mp3_title(title)
    path_to_desktop = handle_file_location()
    full_path = path_to_desktop + file_name
    output.save(full_path)

    # starts the file reading in the default OS mp3 player
    start_file_str = "start" + " " + full_path
    os.system(start_file_str)

def create_mp3_title(user_title):
    # print('\nProvide a name for the audio file of your article.')
    file_name = user_title + '.mp3'
    formatted_filename = file_name.replace(' ', '-')
    # print('\n** The audio version of your article is being prepared in your desktop folder. It will play shortly. **')
    return formatted_filename
