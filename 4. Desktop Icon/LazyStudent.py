from tkinter import *
from tkinter import filedialog
from moviepy import *
#from moviepy.editor import VideoFileClip
from pytube import YouTube
import shutil
import whisper
from transformers import *
from transformers import pipeline
import numpy as np
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# long test link https://www.youtube.com/watch?v=TsfLm5iiYb4
# short test link https://www.youtube.com/watch?v=yCCrS_jynbg 
list = []

#Functions
def select_path():
    #allows user to select a path from the explorer
    path = filedialog.askdirectory()
    path_label.config(text=path)

def download__transcribe_summarise_file():
    #get user path
    get_link = link_field.get()
    #get selected path
    user_path = path_label.cget("text")
    screen.title('Downloading...')
    #Download Video
    mp4_video = YouTube(get_link).streams.get_highest_resolution().download(filename = "downloaded_video")
    #vid_clip = VideoFileClip(mp4_video)
    #vid_clip.close()
    #move file to selected directory
    shutil.move(mp4_video, user_path) #download works
    #---------------------------------------------------
    # Transcriber
    try:
        screen.title('Download Complete! Transcribing...')
        model = whisper.load_model('base')
        model_text = model.transcribe(user_path + r'\downloaded_video', fp16=False)['text'] # works till this line. Gives transcription output
        text_file = open(user_path + r'\transcribed_text.txt', "w")
        text_file.write(model_text)
        text_file.close()
        shutil.move(text_file, user_path) # Transcriber works!
    except:
        pass
    #---------------------------------------------------
    # Summariser
    try:
        screen.title('Transcribing Complete! Summarising...')
        summarizer = pipeline('summarization')
        with open(user_path + r'\transcribed_text.txt') as file:
            lines = file.readlines()
        #summary_text=summarizer(lines[0])
        for i in np.arange(0, len(lines[0]), 500):
            x = summarizer(lines[0][i:i+500], max_length=130, min_length=30,do_sample=False)
            list.append(x[0]['summary_text'])
        text_file2 = open(user_path + r"\summary.txt", "wt")
        #text_file2.write(summary_text[0]['summary_text'])
        for i in range(len(list)):
            text_file2.write(list[i])
        text_file2.close()
        shutil.move(text_file2, user_path)
    except:
        pass

    screen.title('Summarising Complete!')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
screen = Tk()
title = screen.title('Lazy Student')
canvas = Canvas(screen, width=500, height=500)
canvas.pack()

#image logo
logo_img = PhotoImage(file='3. Lazy Student GUI\yt3.png')
#resize
logo_img = logo_img.subsample(2, 2)
canvas.create_image(250, 100, image=logo_img)

#link field
link_field = Entry(screen, width=40, font=('Arial', 15) )
link_label = Label(screen, text="Enter Download Link: ", font=('Arial', 15))

#Select Path for saving the file
path_label = Label(screen, text="Select Path For Download", font=('Arial', 15))
select_btn =  Button(screen, text="Select Path", bg='blue', padx='22', pady='5',font=('Arial', 15), fg='#fff', command=select_path)
#Add to window
canvas.create_window(250, 280, window=path_label)
canvas.create_window(250, 330, window=select_btn)

#Add widgets to window 
canvas.create_window(250, 170, window=link_label)
canvas.create_window(250, 220, window=link_field)

#Download btns
download_btn = Button(screen, text="Download File",bg='blue', padx='22', pady='5',font=('Arial', 15), fg='#fff', command=download__transcribe_summarise_file)
#add to canvas
canvas.create_window(250, 390, window=download_btn)

screen.mainloop()
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Source: https://github.com/Maclinz/yt_downloader/blob/master/download.py
# source: https://www.youtube.com/watch?v=TEATfq6hPIg
# test link https://www.youtube.com/watch?v=yCCrS_jynbg 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
