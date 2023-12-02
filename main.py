import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import validators
from pytube import YouTube
import os
from PIL import Image, ImageTk
import sys

class YouTubeVideoDownloader(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Video Downloader")
        self.geometry('400x200+100+100')
        self.resizable(False, False)
        if getattr(sys, 'frozen', False):
            ico = Image.open(os.path.join(sys._MEIPASS, "files/logo.png"))
        else:
            ico = Image.open("files/logo.png")
        photo = ImageTk.PhotoImage(ico)
        self.wm_iconphoto(False, photo)
        self.iconphoto(False, photo) 

        self.get_previous_destination()
        self.create_widgets()

    def set_frame(self):
        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()
        
    def create_widgets(self):
        self.set_frame()
        # Url Input definition
        self.url_input_label = ttk.Label(self.frame, text="Youtube URL").grid(column=0, row=0)
        self.url_input = ttk.Entry(self.frame)
        self.url_input.grid(column=1, row=0, columnspan=2, padx=5)

        # Error label definition
        self.error_label = ttk.Label(self.frame, foreground='red')
        self.error_label.grid(column=1, row=1, sticky=tk.W, padx=5)

        # File title input definition
        self.filename_input_label = ttk.Label(self.frame, text="Nome file").grid(column=0, row=2)
        self.filename_input = ttk.Entry(self.frame)
        self.filename_input.grid(column=1, row=2, columnspan=2, padx=5)

        # Destination Input definition
        ttk.Button(self.frame, text='Seleziona destinazione', command=self.select_destination_button_action).grid(column=0, row=3, pady=4)
        self.destination_path_input = ttk.Entry(self.frame)
        self.destination_path_input.grid(column=1, row=3)
        self.destination_path_input.insert(string=self.previous_destination, index=0)
        
        # Buttons definition
        ttk.Button(self.frame, text='Scarica Audio', command=self.download_button_action).grid(column=0, row=4, pady=4)
        ttk.Button(self.frame, text="Quit", command=self.destroy).grid(column=1, row=4)

        # Display process label
        self.download_label = ttk.Label(self.frame, foreground='green', justify="center")
        self.download_label.grid(row=5)

    def show_message(self, error='', color='black'):
        self.error_label['text'] = error
        self.url_input['foreground'] = color

    def validate_url(self, url):
        return bool(validators.url(url))
    
    def get_previous_destination(self):
        try:
            self.previous_destination = open("./previous_destination.txt", mode="r").read()
        except:
            self.previous_destination = ""

    def set_previous_destination(self, destination):
        open("./previous_destination.txt", mode="w").write(destination)
    
    def get_audio_stream_from_youtube_video(self):
        self.yt_video = YouTube(self.url)
        self.audio_stream = self.yt_video.streams.filter(only_audio=True).first()

    def save_audio(self):
        if self.previous_destination:
            self.destination = self.previous_destination
        elif not self.destination:
            self.destination = filedialog.askdirectory(title="Seleziona la cartella in cui salvare il file")
            self.set_previous_destination(self.destination)

        base, ext = os.path.splitext(self.destination)
        self.file_name = self.filename_input.get()
        if self.file_name:
            filename = f"{base}/{self.file_name}" if ".mp3" in self.file_name else f"{base}/{self.file_name}.mp3"
        else:
            filename = f"{base}/{self.yt_video.title}.mp3"
        
        out_file = self.audio_stream.download(output_path=self.destination)
        os.rename(out_file, filename)

    def download_button_action(self):
        self.download_label['text'] = ""
        self.url = self.url_input.get() 
        is_valid_url = self.validate_url(self.url)
        if not is_valid_url:
            self.show_message('Inserire un url valido', 'red')
            return
        self.show_message()
        self.get_audio_stream_from_youtube_video()
        self.save_audio()
        self.download_label['text'] = "Download terminato!"
        
    def select_destination_button_action(self):
        self.destination = filedialog.askdirectory(title="Seleziona la cartella in cui salvare il file")
        self.set_previous_destination(self.destination)
        self.destination_path_input.delete(0, tk.END)
        self.destination_path_input.insert(string=self.destination, index=0)


if __name__ == '__main__':
    app = YouTubeVideoDownloader()
    app.mainloop()
