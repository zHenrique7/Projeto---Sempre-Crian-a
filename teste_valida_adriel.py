from tkinter import messagebox as mb
from tkinter import filedialog, ttk, font, messagebox
from tkinter.ttk import Treeview
import customtkinter
from customtkinter import CTkImage
from tkinter import *
from PIL import Image, ImageTk  # Importação correta do Pillow
from tkcalendar import Calendar, DateEntry
import mysql.connector
import ctypes
from datetime import datetime

def valida_nome(nome):
    valida=True
    if nome=='':
        mb.showwarning('Campos vazios','Campo nome é obrigatório!')
        valida=False
    for i in nome:
        if (not i.isalpha() or not i.isspace()):
            mb.showwarning('Campo inválido','Caractere invalido')
            valida=False
            break
    if (len(nome)>50):
        mb.showwarning('Passou do total','Nome muito grande')
        valida=False
    return valida