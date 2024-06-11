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

def valida_telefone(self,telefone):
    if len(telefone)!=11:
        messagebox.showwarning('Telefone inválido','Digite um telefone válido com 11 dígitos no modelo 99999999999')
        return False
    for i in telefone:
        if(not(i.isdigit())):
            messagebox.showwarning('Telefone inválido','Só podem haver números no telefone')
            return False
    return True

def valida_cpf(self,cpf):
    if len(cpf)!=14:
        messagebox.showwarning('CPF inválido','Digite um cpf no modelo 123.123.123-12')
        return False
    for i in range(len(cpf)):
        if(i==3 and cpf[i]!='.'):
            messagebox.showwarning('CPF inválido','Digite um cpf no modelo 123.123.123-12')
            return False
        elif(i==7 and cpf[i]!='.'):
            messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
            return False
        elif(i==11 and cpf[i]!='-'):
            messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
            return False
        elif(i!=3 and i!=7 and i!=11 and not(cpf[i].isdigit())):
            messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
            return False
    return True

def valida_rg(self,rg):
    if len(rg)!=12:
        messagebox.showwarning('RG inválido','Digite um RG válido no modelo: 00.000.000-0')
        return False
    for i in range(len(rg)):
        if(i==2 and rg[i]!='.'):
            messagebox.showwarning('RG inválido','Digite um RG válido no modelo: 00.000.000-0')
            return False
        elif(i==6 and rg[i]!='.'):
            messagebox.showwarning('RG inválido','Digite um RG válido no modelo: 00.000.000-0')
            return False
        elif(i==10 and rg[i]!='-'):
            messagebox.showwarning('RG inválido','Digite um RG válido no modelo: 00.000.000-0')
            return False
        elif(i!=2 and i!=6 and i!=10 and not(rg[i].isdigit())):
            messagebox.showwarning('RG inválido','Digite um RG válido no modelo: 00.000.000-0')
            return False
    return True

def valida_projeto(self,projeto):
    if len(projeto)>100:
        messagebox.showwarning('Passou do total','Máximo de 100 caracteres')
        return False
    elif projeto=='':
        messagebox.showwarning('Campo vazio','Campo projeto não pode ser vazio')
        return False
    return True
