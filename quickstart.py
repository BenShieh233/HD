from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import time

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

upload_file = 'HD_products.csv'
gfile = drive.CreateFile({'parents':[{'id':'1tiu74hnlyNGhVOBYQN8SNdnmbKXBr_th'}]})
gfile.SetContentFile(upload_file)
gfile.Upload()