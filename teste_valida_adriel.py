from tkinter import messagebox
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

def valida_nome(self,nome):
    valida=True
    if nome=='':
        messagebox.showwarning('Campos vazios','Campo nome é obrigatório!')
        valida=False
    for i in nome:
        if (not (i.isalpha()) and not (i.isspace())):
            messagebox.showwarning('Campo inválido','Caractere invalido')
            valida=False
            break
    if (len(nome)>50):
        messagebox.showwarning('Passou do total','Nome muito grande')
        valida=False
    return valida

def telefone(self,telefone):
    if len(telefone)!=11:
        messagebox.showwarning('Telefone inválido','Digite um telefone válido com 11 dígitos no modelo 99999999999')
        return False
    for i in telefone:
        if(not(i.isdigit())):
            messagebox.showwarning('Telefone inválido','Só podem haver números no telefone')
            return False
