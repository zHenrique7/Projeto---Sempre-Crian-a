from tkinter import filedialog, ttk, font, messagebox
from tkinter.ttk import Treeview
import customtkinter
from customtkinter import CTkImage
from tkinter import *
from PIL import Image, ImageTk  # Importação correta do Pillow
from tkcalendar import Calendar, DateEntry
import mysql.connector
import ctypes


conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='SempreCriança'
)

cursor = conexao.cursor()
# cursor.execute('CREATE DATABASE if not exists SempreCriança')
# cursor.execute('''Create table Crianças(
# id INT AUTO_INCREMENT PRIMARY KEY,
# nome VARCHAR(50) NOT NULL,
# data_nascimento DATE NOT NULL,
# telefone VARCHAR(11) NOT NULL,
# endereco VARCHAR(100) NOT NULL,
# cpf_responsavel VARCHAR(14) NOT NULL,
# rg_resp VARCHAR(12) NOT NULL,
# nome_resp VARCHAR(50) NOT NULL,
# projeto VARCHAR(100) NOT NULL,
# declaracao_escolar VARCHAR(10),
# vacinacao VARCHAR(10),
# termo_imagem VARCHAR(10),
# certidao VARCHAR(10),
# frequencia INT DEFAULT 0
# )'''
# )

# cursor.execute('DROP TABLE Crianças')


#
# cursor.execute('''CREATE TABLE Voluntarios(
# ID INT AUTO_INCREMENT PRIMARY KEY,
# nome VARCHAR(50) NOT NULL,
# telefone VARCHAR(11) NOT NULL,
# email VARCHAR(50) NOT NULL,
# profissao VARCHAR(50) NOT NULL,
# projeto VARCHAR(100) NOT NULL,
# participacao VARCHAR(10) NOT NULL,
# frequencia INT DEFAULT 0
# )'''
# )




# cursor.execute('''
#     ALTER TABLE Crianças
#     ADD COLUMN frequencia INT DEFAULT 0
# ''')


# cursor.execute('''
#     ALTER TABLE Voluntarios
#     ADD COLUMN profissao VARCHAR(50) NOT NULL
# ''')

conexao.commit()

class App:
    def __init__(self, root):
        self.on_resize = None
        self.root = root
        self.tema()
        self.create_widgets()
        self.aparencia()
        self.consulta_criancas_tree = None  # Inicialização da Treeview para consulta de crianças
        self.cursor = conexao.cursor()
        self.tree = None  # Inicialize o atributo tree
        self.root.iconbitmap("icon.ico")

        # ICONE DO APLICATIVO --------
        myappid = 'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        root.iconbitmap('icon.ico')
    def tema(self):
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")

    def centralizar_janela(self, largura, altura, janela):
        # Obter as dimensões da tela
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        # Calcular as coordenadas para centralizar a janela
        x = (largura_tela - largura) // 2
        y = (altura_tela - altura) // 2

        # Definir as dimensões e coordenadas da janela
        janela.geometry('%dx%d+%d+%d' % (largura, altura, x, y))

    def create_widgets(self):
        self.root.geometry("700x500")
        self.root.title("Sempre criança")
        self.root.resizable(False, False)
        self.centralizar_janela(700, 500, self.root)

        img = CTkImage(Image.open("icon.ico"), size=(310, 230))
        self.label_img = customtkinter.CTkLabel(master=self.root, image=img, text="")
        self.label_img.image = img
        self.label_img.place(x=5, y=100)

        # Frame na direita -------------
        cadastro_frame = customtkinter.CTkFrame(master=self.root, width=370, height=500, corner_radius=20,
                                                fg_color="#ffffdc")
        cadastro_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(master=cadastro_frame, text='Gerenciador - Sempre Criança',
                                       font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        # BOTÕES DA JANELA PRINCIPAL -------
        cadastrar_criancas_button = customtkinter.CTkButton(master=cadastro_frame, text="Cadastrar crianças", width=140,
                                                            height=50, fg_color="#FFD700", text_color="#1e1e1e",
                                                            corner_radius=10,
                                                            command=self.abrir_janela_cadastro_criancas)
        cadastrar_criancas_button.place(x=20, y=150)

        cadastrar_voluntarios_button = customtkinter.CTkButton(master=cadastro_frame, text="Cadastrar voluntários",
                                                               width=100, height=50, fg_color="#FFD700",
                                                               text_color="#1e1e1e", corner_radius=10,
                                                               command=self.abrir_janela_cadastro_voluntarios)
        cadastrar_voluntarios_button.place(x=200, y=150)

        consultar_criancas_button = customtkinter.CTkButton(master=cadastro_frame, text="Consultar Crianças", width=140,
                                                            height=50, fg_color="#FFD700", text_color="#1e1e1e",
                                                            corner_radius=10,
                                                            command=self.abrir_janela_consulta_crianca)
        consultar_criancas_button.place(x=20, y=250)

        consultar_voluntarios_button = customtkinter.CTkButton(master=cadastro_frame, text="Consultar Voluntários",
                                                               width=140, height=50, fg_color="#FFD700",
                                                               text_color="#1e1e1e", corner_radius=10,
                                                               command=self.abrir_janela_consulta_voluntarios)
        consultar_voluntarios_button.place(x=200, y=250)
        # FIM DOS BOTÕES -------------

    def aparencia(self):
        self.lb_apm = customtkinter.CTkLabel(self.root, text="", bg_color="transparent",
                                             text_color=['#000', '#fff']).place(x=60, y=420)
        self.opt_apm = customtkinter.CTkOptionMenu(self.root, values=["Light", "Dark", "System"],
                                                   command=self.change_apm).place(x=20, y=450)

    def change_apm(self, nova_aparencia):
        customtkinter.set_appearance_mode(nova_aparencia)

        # FIM DA JANELA PRINCIPAL -------------

    # JANELA DE CADASTRO DE CRIANÇAS -------------------------------------
    def abrir_janela_cadastro_criancas(self):
        self.nova_janela = customtkinter.CTkToplevel(self.root)
        self.nova_janela.title("Cadastro de Crianças")
        self.nova_janela.iconbitmap("icon.ico")
        self.nova_janela.geometry("800x600")
        self.nova_janela.resizable(False, False)
        self.centralizar_janela(800, 600, self.nova_janela)
        self.root.iconify()
        # Definir a função a ser chamada quando a janela for fechada
        self.nova_janela.protocol("WM_DELETE_WINDOW", self.fechar_janela_cadastro)

        # Configurar grid
        self.nova_janela.grid_columnconfigure(0, weight=1)
        self.nova_janela.grid_columnconfigure(1, weight=3)

        # Frame na direita -------------
        crianca_frame = customtkinter.CTkFrame(self.nova_janela, width=470, height=600, corner_radius=20,
                                               fg_color="#ffffdc")
        crianca_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(crianca_frame, text='', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        img = CTkImage(Image.open("icone.png"), size=(310, 230))
        self.label_img = customtkinter.CTkLabel(self.nova_janela, image=img, text="")
        self.label_img.image = img
        self.label_img.place(x=5, y=100)

        # Nome
        nome_label = customtkinter.CTkLabel(self.nova_janela, text="Nome:", bg_color="#ffffdc", text_color='black')
        nome_label.place(x=495, y=10)
        self.nome_entry = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.nome_entry.place(x=560, y=10, )

        # Data de nascimento
        data_nascimento = customtkinter.CTkLabel(self.nova_janela, text="Data de\nNascimento:", bg_color="#ffffdc",
                                                 text_color='black')
        data_nascimento.place(x=475, y=60)

        self.date_entry = DateEntry(self.nova_janela, width=12, background='#f2f28d', foreground='black', borderwidth=2, date_pattern="dd/MM/yyyy")
        self.date_entry.place(x=580, y=65)


        # Telefone --------------------
        telefone_label = customtkinter.CTkLabel(self.nova_janela, text="Telefone:", bg_color="#ffffdc",
                                                text_color='black')
        telefone_label.place(x=490, y=110)
        self.telefone_entry = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.telefone_entry.place(x=560, y=110)

        # CPF -----------------------
        cpf_responsavel = customtkinter.CTkLabel(self.nova_janela, text="CPF do \nResponsável:", bg_color="#ffffdc",
                                                 text_color='black')
        cpf_responsavel.place(x=475, y=150)
        self.cpf_responsavel = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.cpf_responsavel.place(x=560, y=150, )

        # RG ------------------
        rg_resp = customtkinter.CTkLabel(self.nova_janela, text="RG do \nResponsável:", bg_color="#ffffdc",
                                         text_color='black')
        rg_resp.place(x=475, y=190)
        self.rg_resp = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.rg_resp.place(x=560, y=190, )

        # NOME DO RESPONSÁVEL ----------------------------
        nome_resp = customtkinter.CTkLabel(self.nova_janela, text="Nome do\nResponsável:", bg_color="#ffffdc",
                                           text_color='black')
        nome_resp.place(x=475, y=230)
        self.nome_resp = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.nome_resp.place(x=560, y=230, )

        # ENDEREÇO ----------------------------
        endereco = customtkinter.CTkLabel(self.nova_janela, text="Endereço:", bg_color="#ffffdc", text_color='black')
        endereco.place(x=475, y=270)
        self.endereco = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.endereco.place(x=560, y=270, )

        # PROJETO ----------------------------
        projeto = customtkinter.CTkLabel(self.nova_janela, text="Projeto:", bg_color="#ffffdc", text_color='black')
        projeto.place(x=475, y=310)
        self.projeto = customtkinter.CTkEntry(self.nova_janela, bg_color= '#ffffdc')
        self.projeto.place(x=560, y=310, )

        # DECLARAÇÃO ESCOLAR -----------------
        self.declaracao_var = StringVar()  # Variável de controle

        declaracao_label = customtkinter.CTkLabel(self.nova_janela, text="Declaração\nescolar:", bg_color="#ffffdc",
                                                  text_color='black')
        declaracao_label.place(x=475, y=360)
        declaracao_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.declaracao_var,
                                                      value="Sim",
                                                      bg_color="#ffffdc", text_color='black')
        declaracao_sim.place(x=570, y=360)
        declaracao_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.declaracao_var,
                                                      value="Não",
                                                      bg_color="#ffffdc", text_color='black')
        declaracao_nao.place(x=630, y=360)

        # VACINAÇÃO ------------------------
        self.vacina_var = StringVar()  # Variável de controle para os botões de opção

        vacina_label = customtkinter.CTkLabel(self.nova_janela, text="A vacinação está\nem dia?", bg_color="#ffffdc",
                                              text_color='black')
        vacina_label.place(x=460, y=400)
        vacina_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.vacina_var, value="Sim",
                                                  bg_color="#ffffdc", text_color='black')
        vacina_sim.place(x=570, y=400)
        vacina_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.vacina_var, value="Não",
                                                  bg_color="#ffffdc", text_color='black')
        vacina_nao.place(x=630, y=400)

        # Certidao ------------------------
        self.certidao_var = StringVar()  # Variável de controle para os botões de opção

        certidao_label = customtkinter.CTkLabel(self.nova_janela, text="Certidão de nascimento:", bg_color="#ffffdc",
                                              text_color='black')
        certidao_label.place(x=430, y=480)
        certidao_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.certidao_var, value="Sim",
                                                  bg_color="#ffffdc", text_color='black')
        certidao_sim.place(x=570, y=480)
        certidao_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.certidao_var, value="Não",
                                                  bg_color="#ffffdc", text_color='black')
        certidao_nao.place(x=630, y=480)


        # TERMO -----------------------------
        self.termo_var = StringVar()  # Variável de controle

        termo_label = customtkinter.CTkLabel(self.nova_janela, text="Termo de \nimagem assinado?", bg_color="#ffffdc",
                                             text_color='black')
        termo_label.place(x=450, y=440)
        termo_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.termo_var, value="Sim",
                                                 bg_color="#ffffdc", text_color='black')
        termo_sim.place(x=570, y=440)
        termo_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.termo_var, value="Não",
                                                 bg_color="#ffffdc", text_color='black')
        termo_nao.place(x=630, y=440)

        # Certidão de nascimento (PDF)
        # self.certidao_var = StringVar()  # Variável de controle para o caminho do arquivo PDF
        #
        # certidao_label = customtkinter.CTkLabel(self.nova_janela, text="Certidão de Nascimento (PDF):", bg_color="#ffffdc", text_color='black')
        # certidao_label.place(x=470, y=490)
        # certidao_button = customtkinter.CTkButton(self.nova_janela, text="Selecionar Arquivo", bg_color="#ffffdc",
        #                                           command=self.selecionar_certidao)
        # certidao_button.place(x=490, y=520)

        # Botão CONFIRMAR
        confirmar_button = customtkinter.CTkButton(self.nova_janela, text="CONFIRMAR", width=170, height=50,
                                                   corner_radius=15, bg_color= '#ffffdc', command=self.salvar_informacoes)
        confirmar_button.place(x=485, y=530)

    # def selecionar_certidao(self):
    #     # filepath = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo",
    #     #                                       filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
    #     # Exibe a janela de seleção de arquivo para salvar o PDF
    #     filepath = filedialog.asksaveasfilename(defaultextension=".pdf",
    #                                             filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
    #     if filepath:
    #         # Aqui você pode adicionar código para salvar o arquivo PDF usando o caminho 'filepath'
    #         customtkinter.messagebox.showinfo("Sucesso", f"Arquivo PDF salvo em:\n{filepath}")
    #     else:
    #         customtkinter.messagebox.showwarning("Cancelado", "Nenhum arquivo foi selecionado para salvar.")

    def valida_nome(self, nome):
        valida = True
        if nome == '':
            messagebox.showwarning('Campos vazios', 'Campo nome é obrigatório!')
            valida = False
        for i in nome:
            if (not (i.isalpha()) and not (i.isspace())):
                messagebox.showwarning('Campo inválido', 'Caracteres invalidos')
                valida = False
                break
        if (len(nome) > 50):
            messagebox.showwarning('Passou do total', 'Nome muito grande')
            valida = False
        return valida

    def valida_telefone(self, telefone):
        if len(telefone) != 11:
            messagebox.showwarning('Telefone inválido',
                                   'Digite um telefone válido com 11 dígitos no modelo 99999999999')
            return False
        for i in telefone:
            if (not (i.isdigit())):
                messagebox.showwarning('Telefone inválido', 'Só podem haver números no telefone')
                return False
        return True

    def valida_cpf(self, cpf):
        if len(cpf) != 14:
            messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
            return False
        for i in range(len(cpf)):
            if (i == 3 and cpf[i] != '.'):
                messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
                return False
            elif (i == 7 and cpf[i] != '.'):
                messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
                return False
            elif (i == 11 and cpf[i] != '-'):
                messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
                return False
            elif (i != 3 and i != 7 and i != 11 and not (cpf[i].isdigit())):
                messagebox.showwarning('CPF inválido', 'Digite um cpf no modelo 123.123.123-12')
                return False

        return True

    def valida_rg(self, rg):
        if len(rg) != 12:
            messagebox.showwarning('RG inválido', 'Digite um RG válido no modelo: 00.000.000-0')
            return False
        for i in range(len(rg)):
            if (i == 2 and rg[i] != '.'):
                messagebox.showwarning('RG inválido', 'Digite um RG válido no modelo: 00.000.000-0')
                return False
            elif (i == 6 and rg[i] != '.'):
                messagebox.showwarning('RG inválido', 'Digite um RG válido no modelo: 00.000.000-0')
                return False
            elif (i == 10 and rg[i] != '-'):
                messagebox.showwarning('RG inválido', 'Digite um RG válido no modelo: 00.000.000-0')
                return False
            elif (i != 2 and i != 6 and i != 10 and not (rg[i].isdigit())):
                messagebox.showwarning('RG inválido', 'Digite um RG válido no modelo: 00.000.000-0')
                return False
        return True

    def valida_projeto(self, projeto):
        if len(projeto) > 100:
            messagebox.showwarning('Passou do total', 'Máximo de 100 caracteres')
            return False
        elif projeto == '':
            messagebox.showwarning('Campo vazio', 'Campo projeto não pode ser vazio')
            return False
        return True

    def valida_radio_button(self, teste):
        if teste == '':
            messagebox.showwarning('Campo vazio', 'Escolha uma das opções')
            return False
        return True

    def salvar_informacoes(self):
        # Coleta os dados dos campos de entrada
        nome = self.nome_entry.get()
        if not self.valida_nome(nome):  # Chama a função de validação
            return  # Retorna se o nome não for válido
        data_nascimento = self.date_entry.get_date()
        telefone = self.telefone_entry.get()
        if not self.valida_telefone(telefone):
            return
        endereco = self.endereco.get()
        cpf = self.cpf_responsavel.get()
        if not self.valida_cpf(cpf):
            return
        rg = self.rg_resp.get()
        if not self.valida_rg(rg):
            return
        nome_resp = self.nome_resp.get()
        projeto = self.projeto.get()
        if not self.valida_projeto(projeto):
            return
        declaracao = self.declaracao_var.get()
        vacinacao = self.vacina_var.get()
        termo = self.termo_var.get()
        certidao = self.certidao_var.get()

        if not self.valida_radio_button(termo):
            return
        if not self.valida_radio_button(declaracao):
            return
        if not self.valida_radio_button(vacinacao):
            return
        if not self.valida_radio_button(certidao):
            return
        # certidao = self.certidao_var.get()

        # Inserir os dados no banco de dados

        self.cursor.execute('''
        INSERT INTO Crianças (nome, data_nascimento, telefone, endereco, cpf_responsavel, rg_resp, nome_resp, projeto, declaracao_escolar, vacinacao, termo_imagem, certidao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

        ''', (nome, data_nascimento, telefone, endereco, cpf, rg, nome_resp, projeto, declaracao, vacinacao, termo, certidao))
        conexao.commit()
        messagebox.showinfo("Dados Salvos", "Os dados foram salvos com sucesso.")

        # Exibe os dados no console (apenas para verificação)
        print(f"Nome: {nome}")
        print(f"Data de Nascimento: {data_nascimento}")
        print(f"Telefone: {telefone}")
        print(f"Telefone: {endereco}")
        print(f"CPF do Responsável: {cpf}")
        print(f"RG do Responsável: {rg}")
        print(f"Nome do Responsável: {nome_resp}")
        print(f"Projeto: {projeto}")
        print(f"Declaração Escolar: {declaracao}")
        print(f"Vacinação em dia: {vacinacao}")
        print(f"Termo de imagem assinado: {termo}")
        print(f"Certidão de Nascimento: {certidao}")
    def fechar_janela_cadastro(self):
        # Fechar a nova janela
        self.nova_janela.destroy()

        self.centralizar_janela(700, 500, self.root)

        # Abrir novamente a janela principal
        self.root.deiconify()

    # FIM DA JANELA DE CADASTRO DE CRIANÇAS --------------------------------

    # JANELA DE CADASTRO DE VOLUNTARIOS -------------------------------------
    def abrir_janela_cadastro_voluntarios(self):
        self.janela_voluntario = customtkinter.CTkToplevel(self.root)
        self.janela_voluntario.title("Cadastro de Voluntários")
        self.janela_voluntario.iconbitmap("icon.ico")
        self.janela_voluntario.geometry("800x600")
        self.janela_voluntario.resizable(False, False)
        self.centralizar_janela(800, 600, self.janela_voluntario)
        self.root.iconify()
        self.janela_voluntario.protocol("WM_DELETE_WINDOW", self.fechar_janela_voluntario)

        # Configurar grid
        self.janela_voluntario.grid_columnconfigure(0, weight=1)
        self.janela_voluntario.grid_columnconfigure(1, weight=3)

        # Frame na direita -------------
        crianca_frame = customtkinter.CTkFrame(self.janela_voluntario, width=470, height=600, corner_radius=20,
                                               fg_color="#ffffdc")
        crianca_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(crianca_frame, text='', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        img = CTkImage(Image.open("icone.png"), size=(310, 230))
        self.label_img = customtkinter.CTkLabel(self.janela_voluntario, image=img, text="")
        self.label_img.image = img
        self.label_img.place(x=5, y=100)

        # Nome
        nome_label = customtkinter.CTkLabel(self.janela_voluntario, text="Nome:", bg_color="#ffffdc",
                                            text_color='black')
        nome_label.place(x=500, y=120)
        self.nome_entry = customtkinter.CTkEntry(self.janela_voluntario, bg_color= '#ffffdc')
        self.nome_entry.place(x=560, y=120, )

        # Telefone --------------------
        telefone_label = customtkinter.CTkLabel(self.janela_voluntario, text="Telefone:", bg_color="#ffffdc",
                                                text_color='black')
        telefone_label.place(x=490, y=220)
        self.telefone_entry = customtkinter.CTkEntry(self.janela_voluntario, bg_color= '#ffffdc')
        self.telefone_entry.place(x=560, y=220)

        # EMAIL --------------------
        email_label = customtkinter.CTkLabel(self.janela_voluntario, text="Email:", bg_color="#ffffdc",
                                             text_color='black')
        email_label.place(x=500, y=170)
        self.email_entry = customtkinter.CTkEntry(self.janela_voluntario, bg_color= '#ffffdc')
        self.email_entry.place(x=560, y=170)

        # PROFISSÃO --------------------
        profissao_label = customtkinter.CTkLabel(self.janela_voluntario, text="Profissão:", bg_color="#ffffdc",
                                                 text_color='black')
        profissao_label.place(x=490, y=270)
        self.profissao_entry = customtkinter.CTkEntry(self.janela_voluntario, bg_color= '#ffffdc')
        self.profissao_entry.place(x=560, y=270)

        # PROJETO ----------------------------
        projeto = customtkinter.CTkLabel(self.janela_voluntario, text="Projeto:", bg_color="#ffffdc",
                                         text_color='black')
        projeto.place(x=500, y=320)
        self.projeto = customtkinter.CTkEntry(self.janela_voluntario, bg_color= '#ffffdc')
        self.projeto.place(x=560, y=320, )

        # Já participou de algum projeto? -----------------------------
        self.participacao_var = StringVar()  # Variável de controle

        participacao_label = customtkinter.CTkLabel(self.janela_voluntario, text="Já participou\n de algum projeto?",
                                                    bg_color="#ffffdc", text_color='black')
        participacao_label.place(x=465, y=370)
        participacao_sim = customtkinter.CTkRadioButton(self.janela_voluntario, text="Sim",
                                                        variable=self.participacao_var, value="Sim", bg_color="#ffffdc",
                                                        text_color='black')
        participacao_sim.place(x=585, y=370)
        participacao_nao = customtkinter.CTkRadioButton(self.janela_voluntario, text="Não",
                                                        variable=self.participacao_var, value="Não", bg_color="#ffffdc",
                                                        text_color='black')
        participacao_nao.place(x=645, y=370)

        # Botão CONFIRMAR
        confirmar_button = customtkinter.CTkButton(self.janela_voluntario, text="CONFIRMAR", width=170, height=50,
                                                   corner_radius=15, bg_color= '#ffffdc', command=self.salvar_informacoes_voluntarios)
        confirmar_button.place(x=515, y=420)

    def valida_email(self, email):
        if email == '':
            messagebox.showwarning('Campo vazio', 'O campo email não pode ser vazio')
            return False
        teste = email.find('@')
        if teste == -1:
            messagebox.showwarning('Email inválido', 'Digite um email válido no formato xxxxxxx@xxxxx.xxx')
            return False
        if len(email) > 50:
            messagebox.showwarning('Passou do total', 'Email muito grande')
            return False
        return True

    def salvar_informacoes_voluntarios(self):

        nome = self.nome_entry.get()
        if not self.valida_nome(nome):
            return

        telefone = self.telefone_entry.get()
        if not self.valida_telefone(telefone):
            return

        email = self.email_entry.get()
        if not self.valida_email(email):
            return
        profissao = self.profissao_entry.get()

        if not self.valida_nome(profissao):
            return

        projeto = self.projeto.get()
        if not self.valida_projeto(projeto):
            return

        participacao = self.participacao_var.get()
        if not self.valida_radio_button(participacao):
            return


# Inserir os dados no banco de dados
        self.cursor.execute('''
        INSERT INTO Voluntarios (nome, telefone, email, profissao, projeto, participacao)
        VALUES (%s, %s, %s, %s, %s, %s)

        ''', (nome,telefone, email, profissao, projeto, participacao))
        conexao.commit()
        messagebox.showinfo("Dados Salvos", "Os dados foram salvos com sucesso.")


    def fechar_janela_voluntario(self):
        # Fechar a nova janela
        self.janela_voluntario.destroy()

        self.centralizar_janela(700, 500, self.root)

        # Abrir novamente a janela principal
        self.root.deiconify()

        # JANELA DE CONSULTA DE CRIANÇAS -------------------------------------

    def abrir_janela_consulta_crianca(self):

        # Verificar se a janela de consulta já existe e fechar se for o caso
        if hasattr(self, 'consulta_criancas') and self.consulta_criancas.winfo_exists():
            self.consulta_criancas.destroy()

        self.consulta_criancas = customtkinter.CTkToplevel(self.root)
        self.consulta_criancas.title("Consulta de crianças")
        # self.consulta_criancas.iconbitmap("icon.ico")
        # self.consulta_criancas.state('zoomed')
        self.consulta_criancas.geometry("1000x600")
        self.consulta_criancas.resizable(False, False)
        self.centralizar_janela(1000, 600, self.consulta_criancas)
        self.root.iconify()
        self.consulta_criancas.protocol("WM_DELETE_WINDOW", self.fechar_janela_consulta_criancas)



        # Configurar grid
        self.consulta_criancas.grid_columnconfigure(0, weight=1)
        self.consulta_criancas.grid_columnconfigure(1, weight=3)


        # Frame na direita -------------
        consulta_frame = customtkinter.CTkFrame(self.consulta_criancas, width=1980, height=160,
                                                fg_color="#ffffdc")
        consulta_frame.pack(side=TOP, padx=0, pady=0)

        label = customtkinter.CTkLabel(consulta_frame, text='',
                                       font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=900, y=50)

        img = CTkImage(Image.open("icone.png"), size=(230, 150))
        self.label_img = customtkinter.CTkLabel(self.consulta_criancas, image=img, text="", bg_color="#ffffdc")
        self.label_img.image = img
        self.label_img.place(x=400, y=5)



        # Botão Atualizar
        atualizar_button = customtkinter.CTkButton(self.consulta_criancas, text="Atualizar", width=80, height=40,
                                                   corner_radius=15, bg_color= '#ffffdc', command=self.abrir_janela_editar_crianca)
        atualizar_button.place(x=50, y=85)

        # Botão Excluir
        excluir_button = customtkinter.CTkButton(self.consulta_criancas, text="Excluir", width=80, height=40,
                                                   corner_radius=15, bg_color= '#ffffdc', command=self.excluir_dados_selecionados)
        excluir_button.place(x=150, y=85)

        # Carregar e redimensionar a imagem usando PIL
        lupa_image = Image.open("lupa.png")
        lupa_image = lupa_image.resize((lupa_image.width // 2, lupa_image.height // 2))

        lupa = customtkinter.CTkImage(lupa_image)

        # Criar o botão de pesquisa com a imagem
        pesquisar_button = customtkinter.CTkButton(self.consulta_criancas, text="", width=10, height=10,
                                                   image=lupa, bg_color= '#ffffdc',
                                                   command=self.pesquisar_por_nome,
                                                   )
        pesquisar_button.place(x=810, y=88)

        # Campo de entrada para inserir o nome a ser pesquisado
        self.pesquisar_entry = customtkinter.CTkEntry(self.consulta_criancas, bg_color= '#ffffdc')
        self.pesquisar_entry.place(x=668, y=88)

        # Botão Voltar
        voltar_button = customtkinter.CTkButton(self.consulta_criancas, text="Voltar", width=100, height=40,
                                                   corner_radius=15, bg_color= '#ffffdc',command=self.voltar)
        voltar_button.place(x=870, y=81)

        # Botão de Frequência
        frequencia_button = customtkinter.CTkButton(self.consulta_criancas, text="Falta", width=80, height=40,
                                                   corner_radius=15,bg_color= '#ffffdc', command=self.salvar_frequencia)
        frequencia_button.place(x=250, y=85)



        # Frame para Treeview e Scrollbars
        frame_tree = customtkinter.CTkFrame(self.consulta_criancas)
        frame_tree.pack(side="bottom", pady=(0,0), fill="both", expand=True)

        # Criar um estilo personalizado
        style = ttk.Style()
        style.theme_use("default")  # Escolha de um tema moderno

        # Definir cores e fontes
        style.configure("Treeview",
                        background="white",
                        fieldbackground="#E1E1E1",
                        foreground="black",
                        font=("Helvetica", 10))
        style.map("Treeview", background=[('selected', '#0078D7')])


        # Criar a treeview para exibir os dados
        self.tree = ttk.Treeview(frame_tree, columns=(
            "ID","Nome", "Data de Nascimento", "Telefone", "Endereço", "CPF responsável", "RG responsável", "Nome responsável",
            "Projeto", "Declaração escolar", "Vacinação", "Termo de imagem", "Certidão de nascimento", "Faltas"), show="headings", style="Treeview")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data de Nascimento", text="Data de Nascimento")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("Endereço", text="Endereço")
        self.tree.heading("CPF responsável", text="CPF responsável")
        self.tree.heading("RG responsável", text="RG responsável")
        self.tree.heading("Nome responsável", text="Nome responsável")
        self.tree.heading("Projeto", text="Projeto")
        self.tree.heading("Declaração escolar", text="Declaração escolar")
        self.tree.heading("Vacinação", text="Vacinação")
        self.tree.heading("Termo de imagem", text="Termo de imagem")
        self.tree.heading("Certidão de nascimento", text="Certidão de nascimento")
        self.tree.heading("Faltas", text="Faltas")

        # Ajustar a largura das colunas automaticamente
        for col in self.tree['columns']:
            self.tree.column(col, width=175, anchor='center', stretch=customtkinter.YES)
            # Permitir que o usuário redimensione as colunas
            self.tree.bind('<Configure>', self.on_resize)

        # Adicionar barras de rolagem
        scrollbar_vertical = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)

        # Empacotar treeview e scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_vertical.grid(row=0, column=1, sticky='ns')
        scrollbar_horizontal.grid(row=1, column=0, sticky='ew')

        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)


        # Buscar dados do banco de dados e adicionar ao Treeview
        self.cursor.execute('SELECT * FROM Crianças')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def excluir_dados_selecionados(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione uma criança para deletar.",
                                   parent=self.consulta_criancas)
            return
        # Obter o ID da criança selecionada
        id_selecionado = self.tree.item(item_selecionado, "values")[0]
        # Confirmar a exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar esta criança?",
                                       parent=self.consulta_criancas)
        if resposta:
            # Deletar o registro do banco de dados
            self.cursor.execute("DELETE FROM Crianças WHERE id = %s", (id_selecionado,))
            conexao.commit()

            # Remover o item da Treeview
            self.tree.delete(item_selecionado)
            messagebox.showinfo("Sucesso", "A criança foi deletada com sucesso.")

    def abrir_janela_editar_crianca(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione uma criança para editar.",
                                   parent=self.consulta_criancas)
            return

        # Obter os dados da criança selecionada
        id_selecionado = self.tree.item(item_selecionado, "values")[0]
        self.cursor.execute("SELECT * FROM Crianças WHERE id = %s", (id_selecionado,))
        dados_crianca = self.cursor.fetchone()

        if not dados_crianca:
            messagebox.showerror("Erro", "Os dados da criança não foram encontrados.", parent=self.consulta_criancas)
            return

        # Abrir a janela de edição com abas
        self.janela_edicao = customtkinter.CTkToplevel(self.root)
        self.janela_edicao.title("Editar Criança")
        self.janela_edicao.iconbitmap("icon.ico")
        self.janela_edicao.geometry("800x600")
        self.janela_edicao.resizable(False, False)
        self.centralizar_janela(800, 600, self.janela_edicao)

        # Minimizar a janela principal
        self.root.iconify()

        # Nome
        nome_label = customtkinter.CTkLabel(self.janela_edicao, text="Nome:", bg_color="#ffffdc", text_color='black')
        nome_label.place(x=495, y=10)
        self.nome_entry = customtkinter.CTkEntry(self.janela_edicao)
        self.nome_entry.place(x=560, y=10, )

        # Botão SALVAR EDIÇÕES
        salvar_button = customtkinter.CTkButton(self.janela_edicao, text="SALVAR", width=170, height=50,
                                                corner_radius=15, command=self.salvar_edicao)
        salvar_button.place(x=315, y=200)

    def salvar_edicao(self):
        # Coleta os dados dos campos de entrada
        nome = self.nome_entry.get()

        # Obter o ID da criança selecionada
        item_selecionado = self.tree.selection()
        id_selecionado = self.tree.item(item_selecionado, "values")[0]

        # Atualizar os dados no banco de dados
        self.cursor.execute('''
               UPDATE Crianças
               SET nome = %s
               WHERE id = %s
               ''', (nome, id_selecionado))
        conexao.commit()
        messagebox.showinfo("Dados Salvos", "Os dados foram salvos com sucesso.")

        # Fechar a janela de edição
        self.janela_edicao.destroy()

        self.consulta_criancas.destroy()

        # Abrir a janela de edição novamente para reiniciar
        self.abrir_janela_consulta_crianca()

    def salvar_frequencia(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione uma criança para atualizar a frequência.",
                                   parent=self.consulta_criancas)
            return

        # Obter os dados da criança selecionada
        id_selecionado = self.tree.item(item_selecionado, "values")[0]
        self.cursor.execute("SELECT frequencia FROM Crianças WHERE id = %s", (id_selecionado,))
        frequencia_atual = self.cursor.fetchone()[0]

        # Caixa de diálogo de confirmação
        resposta = messagebox.askyesno("Confirmação", "Marcar falta para essa criança?",
                                       parent=self.consulta_criancas)

        if resposta:  # Se o usuário confirmou
            nova_frequencia = frequencia_atual + 1
        else:  # Se o usuário cancelou
            nova_frequencia = frequencia_atual

        # Atualizar a frequência no banco de dados
        self.cursor.execute("UPDATE Crianças SET frequencia = %s WHERE id = %s", (nova_frequencia, id_selecionado))
        conexao.commit()

        messagebox.showinfo("Frequência atualizada", "A frequência foi atualizada com sucesso.")

        #Fechar a janela de edição
        self.consulta_criancas.destroy()
        # Abrir a janela de edição novamente para reiniciar
        self.abrir_janela_consulta_crianca()

    def voltar(self):
        # Fechar a janela de consulta e restaurar a janela principal
        self.consulta_criancas.destroy()
        self.root.deiconify()

    def pesquisar_por_nome(self):
        # Obter o nome digitado pelo usuário na entrada de pesquisa
        nome_pesquisado = self.pesquisar_entry.get()
        projeto_pesquisado = self.pesquisar_entry.get()
        endereco_pesquisado = self.pesquisar_entry.get()

        # Limpar a treeview antes de exibir os resultados da pesquisa
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Consultar o banco de dados para obter crianças cujos nomes correspondem à pesquisa
        self.cursor.execute("SELECT * FROM Crianças WHERE nome LIKE %s OR projeto LIKE %s OR endereco LIKE %s", ('%' + nome_pesquisado + '%', '%' + projeto_pesquisado + '%', '%' + endereco_pesquisado + '%'))
        rows = self.cursor.fetchall()
        if not rows:
            messagebox.showinfo("Nenhum resultado", "Nenhuma criança encontrada com esse nome.")

        # Adicionar os resultados da pesquisa à treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def fechar_janela_consulta_criancas(self):
        # Fechar a nova janela
        self.consulta_criancas.destroy()

        self.centralizar_janela(700, 500, self.root)

        # Abrir novamente a janela principal
        self.root.deiconify()



# JANELA DE CONSULTA DE VOLUNTARIOS ----------------------------------

    def abrir_janela_consulta_voluntarios(self):

        # Verificar se a janela de consulta já existe e fechar se for o caso
        if hasattr(self, 'consulta voluntarios') and self.consulta_voluntarios.winfo_exists():
            self.consulta_criancas.destroy()

        self.consulta_voluntarios = customtkinter.CTkToplevel(self.root)
        self.consulta_voluntarios.title("Consulta de voluntários")
        self.consulta_voluntarios.iconbitmap("icon.ico")
        # self.consulta_criancas.state('zoomed')
        self.consulta_voluntarios.geometry("1000x600")
        self.consulta_voluntarios.resizable(False, False)
        self.centralizar_janela(1000, 600, self.consulta_voluntarios)
        self.root.iconify()
        self.consulta_voluntarios.protocol("WM_DELETE_WINDOW", self.fechar_janela_consulta_voluntarios)



        # Configurar grid
        self.consulta_voluntarios.grid_columnconfigure(0, weight=1)
        self.consulta_voluntarios.grid_columnconfigure(1, weight=3)


        # Frame na direita -------------
        consulta_frame = customtkinter.CTkFrame(self.consulta_voluntarios, width=1980, height=160,
                                                fg_color="#ffffdc")
        consulta_frame.pack(side=TOP, padx=0, pady=0)

        label = customtkinter.CTkLabel(consulta_frame, text='',
                                       font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=900, y=50)

        img = CTkImage(Image.open("icone.png"), size=(230, 150))
        self.label_img = customtkinter.CTkLabel(self.consulta_voluntarios, image=img, text="", bg_color="#ffffdc")
        self.label_img.image = img
        self.label_img.place(x=400, y=5)

        # Botão Atualizar
        atualizar_button = customtkinter.CTkButton(self.consulta_voluntarios, text="Atualizar", width=80, height=40,
                                                   corner_radius=15, bg_color= '#ffffdc', command=self.abrir_janela_editar_voluntario)
        atualizar_button.place(x=50, y=85)

        # Botão Excluir
        excluir_button = customtkinter.CTkButton(self.consulta_voluntarios, text="Excluir", width=80, height=40,
                                                   corner_radius=15, bg_color= '#ffffdc', command=self.excluir_voluntario)
        excluir_button.place(x=150, y=85)

        # Carregar e redimensionar a imagem usando PIL
        lupa_image = Image.open("lupa.png")
        lupa_image = lupa_image.resize((lupa_image.width // 2, lupa_image.height // 2))

        lupa = customtkinter.CTkImage(lupa_image)

        # Criar o botão de pesquisa com a imagem
        pesquisar_button = customtkinter.CTkButton(self.consulta_voluntarios, text="", width=10, height=10,
                                                   image=lupa, bg_color= '#ffffdc',
                                                   command=self.pesquisar_por_nome_voluntarios
                                                   )
        pesquisar_button.place(x=810, y=88)

        # Campo de entrada para inserir o nome a ser pesquisado
        self.pesquisar_entry = customtkinter.CTkEntry(self.consulta_voluntarios, bg_color= '#ffffdc')
        self.pesquisar_entry.place(x=668, y=88)

        # Botão Voltar
        voltar_button = customtkinter.CTkButton(self.consulta_voluntarios, text="Voltar", width=100, height=40,
                                                   corner_radius=15, bg_color= '#ffffdc',command=self.voltar_voluntarios)
        voltar_button.place(x=870, y=81)

        # Botão de Frequência
        frequencia_button = customtkinter.CTkButton(self.consulta_voluntarios, text="Falta", width=80, height=40,
                                                   corner_radius=15,bg_color= '#ffffdc', command=self.salvar_frequencia_voluntario)
        frequencia_button.place(x=250, y=85)



        # Frame para Treeview e Scrollbars
        frame_tree = customtkinter.CTkFrame(self.consulta_voluntarios)
        frame_tree.pack(side="bottom", pady=(0,0), fill="both", expand=True)

        # Criar um estilo personalizado
        style = ttk.Style()
        style.theme_use("default")  # Escolha de um tema moderno

        # Definir cores e fontes
        style.configure("Treeview",
                        background="white",
                        fieldbackground="#E1E1E1",
                        foreground="black",
                        font=("Helvetica", 10))
        style.map("Treeview", background=[('selected', '#0078D7')])


        # Criar a treeview para exibir os dados
        self.tree = ttk.Treeview(frame_tree, columns=(
            "ID","Nome","Telefone","E-mail","Profissão",
             "Projeto","Participação","Faltas"), show="headings", style="Treeview")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("E-mail", text="E-mail")
        self.tree.heading("Profissão", text="Profissão")
        self.tree.heading("Projeto", text="Projeto")
        self.tree.heading("Participação", text="Participação")
        self.tree.heading("Faltas", text="Faltas")

        # Ajustar a largura das colunas automaticamente
        for col in self.tree['columns']:
            self.tree.column(col, width=175, anchor='center', stretch=customtkinter.YES)
            # Permitir que o usuário redimensione as colunas
            self.tree.bind('<Configure>', self.on_resize)

        # Adicionar barras de rolagem
        scrollbar_vertical = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscroll=scrollbar_vertical.set, xscroll=scrollbar_horizontal.set)

        # Empacotar treeview e scrollbars
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_vertical.grid(row=0, column=1, sticky='ns')
        scrollbar_horizontal.grid(row=1, column=0, sticky='ew')

        frame_tree.grid_rowconfigure(0, weight=1)
        frame_tree.grid_columnconfigure(0, weight=1)


        # Buscar dados do banco de dados e adicionar ao Treeview
        self.cursor.execute('SELECT * FROM Voluntarios')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def excluir_voluntario(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione um voluntário para deletar.",
                                   parent=self.consulta_voluntarios)
            return
        # Obter o ID da criança selecionada
        id_selecionado = self.tree.item(item_selecionado, "values")[0]
        # Confirmar a exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja deletar este voluntário?",
                                       parent=self.consulta_voluntarios)
        if resposta:
            # Deletar o registro do banco de dados
            self.cursor.execute("DELETE FROM Voluntarios WHERE id = %s", (id_selecionado,))
            conexao.commit()

            # Remover o item da Treeview
            self.tree.delete(item_selecionado)
            messagebox.showinfo("Sucesso", "O voluntário foi deletado com sucesso.")


    def abrir_janela_editar_voluntario(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione um voluntário para editar.",
                                       parent=self.consulta_voluntarios)
            return

        # Obter os dados da criança selecionada
        id_selecionado = self.tree.item(item_selecionado, "values")[0]
        self.cursor.execute("SELECT * FROM Voluntarios WHERE id = %s", (id_selecionado,))
        dados_voluntario = self.cursor.fetchone()

        if not dados_voluntario:
            messagebox.showerror("Erro", "Os dados do voluntário não foram encontrados.", parent=self.consulta_voluntarios)
            return

        # Abrir a janela de edição com abas
        self.janela_editar_voluntario = customtkinter.CTkToplevel(self.root)
        self.janela_editar_voluntario.title("Editar Voluntário")
        self.janela_editar_voluntario.iconbitmap("icon.ico")
        self.janela_editar_voluntario.geometry("800x600")
        self.janela_editar_voluntario.resizable(False, False)
        self.centralizar_janela(800, 600, self.janela_editar_voluntario)

        # Minimizar a janela principal
        self.root.iconify()

        # Nome
        nome_label = customtkinter.CTkLabel(self.janela_editar_voluntario, text="Nome:", bg_color="#ffffdc", text_color='black')
        nome_label.place(x=495, y=10)
        self.nome_entry = customtkinter.CTkEntry(self.janela_editar_voluntario)
        self.nome_entry.place(x=560, y=10, )

        # Botão SALVAR EDIÇÕES
        salvar_button = customtkinter.CTkButton(self.janela_editar_voluntario, text="SALVAR", width=170, height=50,
                                                    corner_radius=15, command=self.salvar_edicao)
        salvar_button.place(x=315, y=200)

    def salvar_edicao(self):
        # Coleta os dados dos campos de entrada
        nome = self.nome_entry.get()

        # Obter o ID da criança selecionada
        item_selecionado = self.tree.selection()
        id_selecionado = self.tree.item(item_selecionado, "values")[0]

        # Atualizar os dados no banco de dados
        self.cursor.execute('''
                UPDATE Voluntarios
                SET nome = %s
                WHERE id = %s
        ''', (nome, id_selecionado))
        conexao.commit()
        messagebox.showinfo("Dados Salvos", "Os dados foram salvos com sucesso.")

        # Fechar a janela de edição
        self.janela_editar_voluntario.destroy()

        self.consulta_voluntarios.destroy()

        # Abrir a janela de edição novamente para reiniciar
        self.abrir_janela_consulta_voluntarios()

    def salvar_frequencia_voluntario(self):
        # Obter o item selecionado na Treeview
        item_selecionado = self.tree.selection()
        if not item_selecionado:
            messagebox.showwarning("Nenhum item selecionado", "Por favor, selecione um voluntário para atualizar a frequência.",
                                   parent=self.consulta_voluntarios)
            return

        # Obter os dados da criança selecionada
        id_selecionado = self.tree.item(item_selecionado, "values")[0]
        self.cursor.execute("SELECT frequencia FROM Voluntarios WHERE id = %s", (id_selecionado,))
        frequencia_atual = self.cursor.fetchone()[0]

        # Caixa de diálogo de confirmação
        resposta = messagebox.askyesno("Confirmação", "Marcar presença para este voluntário?",
                                       parent=self.consulta_voluntarios)

        if resposta:  # Se o usuário confirmou
            nova_frequencia = frequencia_atual + 1
        else:  # Se o usuário cancelou
            nova_frequencia = frequencia_atual

        # Atualizar a frequência no banco de dados
        self.cursor.execute("UPDATE Voluntarios SET frequencia = %s WHERE id = %s", (nova_frequencia, id_selecionado))
        conexao.commit()

        messagebox.showinfo("Frequência atualizada", "A frequência foi atualizada com sucesso.")

        # Fechar a janela de edição
        self.consulta_voluntarios.destroy()
        # Abrir a janela de edição novamente para reiniciar
        self.abrir_janela_consulta_voluntarios()

    def voltar_voluntarios(self):
        # Fechar a janela de consulta e restaurar a janela principal
        self.consulta_voluntarios.destroy()
        self.root.deiconify()

    def pesquisar_por_nome_voluntarios(self):
        # Obter o nome digitado pelo usuário na entrada de pesquisa
        nome_pesquisado = self.pesquisar_entry.get()
        projeto_pesquisado = self.pesquisar_entry.get()

        # Limpar a treeview antes de exibir os resultados da pesquisa
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Consultar o banco de dados para obter crianças cujos nomes correspondem à pesquisa
        self.cursor.execute("SELECT * FROM Voluntarios WHERE nome LIKE %s OR projeto LIKE %s", ('%' + nome_pesquisado + '%', '%' + projeto_pesquisado + '%'))
        rows = self.cursor.fetchall()

        if not rows:
            messagebox.showinfo("Nenhum resultado", "Nenhum voluntário encontrado com esse nome.")

        # Adicionar os resultados da pesquisa à treeview
        for row in rows:
            self.tree.insert("", "end", values=row)

    def fechar_janela_consulta_voluntarios(self):
        # Fechar a nova janela
        self.consulta_voluntarios.destroy()

        self.centralizar_janela(700, 500, self.root)

        # Abrir novamente a janela principal
        self.root.deiconify()



# Criação da janela principal
janela = customtkinter.CTk()

# Instanciação da classe App
app = App(janela)

# Iniciar o loop principal da janela
janela.mainloop()
