import ftplib
import pwinput as pw
import tkinter as tk
from tkinter import filedialog

ftp = ftplib.FTP_TLS("ftp.box.com")
username = input("Enter your Box email: ")
password = pw.pwinput(prompt='Enter your password: ', mask='*') # Change the prompt.

ftp.login(username, password)
ftp.prot_p()
root = tk.Tk()
root.withdraw()
file = open(filedialog.askopenfilename(), "rb")
ftp.storbinary("STOR testVideo.mp4", file)
file.close()
ftp.close()