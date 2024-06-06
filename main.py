from tkinter import filedialog, ttk
from tkinter.ttk import Treeview
import customtkinter
from customtkinter import CTkImage
from tkinter import *
from PIL import Image  # Importação correta do Pillow
from tkcalendar import Calendar, DateEntry
import mysql.connector
from datetime import datetime


conexao=mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='SempreCriança'
)

cursor = conexao.cursor()
# cursor.execute('''Create table Crianças(
# nome VARCHAR(50) NOT NULL,
# data_nascimento DATE NOT NULL,
# telefone VARCHAR(11) NOT NULL,
# cpf_responsavel VARCHAR(14) PRIMARY KEY NOT NULL,
# rg_resp VARCHAR(9) NOT NULL,
# nome_resp VARCHAR(50) NOT NULL,
# projeto VARCHAR(20) NOT NULL,
# declaracao_escolar VARCHAR(10),
# vacinacao VARCHAR(10),
# termo_imagem VARCHAR(10)
# )'''
# )



conexao.commit()



class App:
    def __init__(self, root):
        self.root = root
        self.tema()
        self.create_widgets()
        self.aparencia()
        self.consulta_criancas_tree = None  # Inicialização da Treeview para consulta de crianças
        self.cursor = conexao.cursor()

    def tema(self):
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")


    def create_widgets(self):
        self.root.geometry("700x500")
        self.root.title("Sempre criança")
        self.root.iconbitmap("logo.ico")
        self.root.resizable(False, False)


        img = CTkImage(Image.open("logo.png"), size=(310, 230))
        self.label_img = customtkinter.CTkLabel(master=self.root, image=img, text="")
        self.label_img.image = img
        self.label_img.place(x=5, y=100)

        # Frame na direita -------------
        cadastro_frame = customtkinter.CTkFrame(master=self.root, width=370, height=500, corner_radius=20, fg_color="#ffffdc")
        cadastro_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(master=cadastro_frame, text='Gerenciador - Sempre Criança', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        # BOTÕES DA JANELA PRINCIPAL -------
        cadastrar_criancas_button = customtkinter.CTkButton(master=cadastro_frame, text="Cadastrar crianças", width=140, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10, command=self.abrir_janela_cadastro_criancas)
        cadastrar_criancas_button.place(x=20, y=150)

        cadastrar_voluntarios_button = customtkinter.CTkButton(master=cadastro_frame, text="Cadastrar voluntários", width=100, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10, command=self.abrir_janela_cadastro_voluntarios)
        cadastrar_voluntarios_button.place(x=200, y=150)

        consultar_criancas_button = customtkinter.CTkButton(master=cadastro_frame, text="Consultar Crianças", width=140, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10, command=self.abrir_janela_consulta_crianca)
        consultar_criancas_button.place(x=20, y=250)

        consultar_voluntarios_button = customtkinter.CTkButton(master=cadastro_frame, text="Consultar Voluntários", width=140, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10)
        consultar_voluntarios_button.place(x=200, y=250)
         # FIM DOS BOTÕES -------------

    def aparencia(self):
        self.lb_apm = customtkinter.CTkLabel(self.root, text="", bg_color="transparent", text_color=['#000','#fff']).place(x=60, y=420)
        self.opt_apm = customtkinter.CTkOptionMenu(self.root, values=["Light","Dark","System"], command=self.change_apm).place(x=20, y=450)


    def change_apm(self, nova_aparencia):
        customtkinter.set_appearance_mode(nova_aparencia)

        # FIM DA JANELA PRINCIPAL -------------


# JANELA DE CADASTRO DE CRIANÇAS -------------------------------------
    def abrir_janela_cadastro_criancas(self):
        self.nova_janela = customtkinter.CTkToplevel(self.root)
        self.nova_janela.title("Cadastro de Crianças")
        self.nova_janela.iconbitmap("logo.ico")
        self.nova_janela.geometry("800x600")
        self.nova_janela.resizable(False, False)

        # Configurar grid
        self.nova_janela.grid_columnconfigure(0, weight=1)
        self.nova_janela.grid_columnconfigure(1, weight=3)

        # Frame na direita -------------
        crianca_frame = customtkinter.CTkFrame(self.nova_janela, width=470, height=600, corner_radius=20, fg_color="#ffffdc")
        crianca_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(crianca_frame, text='', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        img = CTkImage(Image.open("logo.png"), size=(310,230))
        self.label_img = customtkinter.CTkLabel(self.nova_janela, image=img, text="")
        self.label_img.image = img
        self.label_img.place(x=5, y=100)

        # Nome
        nome_label = customtkinter.CTkLabel(self.nova_janela, text="Nome:", bg_color="#ffffdc", text_color='black')
        nome_label.place(x=495, y=10)
        self.nome_entry = customtkinter.CTkEntry(self.nova_janela)
        self.nome_entry.place(x=560, y=10,)

        # Data de nascimento
        data_nascimento = customtkinter.CTkLabel(self.nova_janela, text="Data de\nNascimento:", bg_color="#ffffdc", text_color='black')
        data_nascimento.place(x=475, y=60)

        self.date_entry = DateEntry(self.nova_janela, width=12, background='#f2f28d', foreground='black', borderwidth=2, date_pattern="dd/MM/yyyy")
        self.date_entry.place(x=580, y=65)

        # self.data_nasc_entry = customtkinter.CTkEntry(self.nova_janela)
        # self.data_nasc_entry.place(x=80, y=50,)

        # Telefone --------------------
        telefone_label = customtkinter.CTkLabel(self.nova_janela, text="Telefone:", bg_color="#ffffdc", text_color='black')
        telefone_label.place(x=490, y=110)
        self.telefone_entry = customtkinter.CTkEntry(self.nova_janela)
        self.telefone_entry.place(x=560, y=110)

        #CPF -----------------------
        cpf_responsavel = customtkinter.CTkLabel(self.nova_janela, text="CPF do \nResponsável:" , bg_color="#ffffdc", text_color='black')
        cpf_responsavel.place(x=475, y=150)
        self.cpf_responsavel = customtkinter.CTkEntry(self.nova_janela)
        self.cpf_responsavel.place(x=560, y=150,)

        #RG ------------------
        rg_resp = customtkinter.CTkLabel(self.nova_janela, text="RG do \nResponsável:", bg_color="#ffffdc", text_color='black')
        rg_resp.place(x=475, y=190)
        self.rg_resp = customtkinter.CTkEntry(self.nova_janela)
        self.rg_resp.place(x=560, y=190,)

        #NOME DO RESPONSÁVEL ----------------------------
        nome_resp = customtkinter.CTkLabel(self.nova_janela, text="Nome do\nResponsável:", bg_color="#ffffdc", text_color='black')
        nome_resp.place(x=475, y=230)
        self.nome_resp = customtkinter.CTkEntry(self.nova_janela)
        self.nome_resp.place(x=560, y=230,)

        #ENDEREÇO ----------------------------
        endereco = customtkinter.CTkLabel(self.nova_janela, text="Endereço:", bg_color="#ffffdc", text_color='black')
        endereco.place(x=475, y=270)
        self.endereco = customtkinter.CTkEntry(self.nova_janela)
        self.endereco.place(x=560, y=270,)

        #PROJETO ----------------------------
        projeto= customtkinter.CTkLabel(self.nova_janela, text="Projeto:", bg_color="#ffffdc", text_color='black')
        projeto.place(x=475, y=310)
        self.projeto = customtkinter.CTkEntry(self.nova_janela)
        self.projeto.place(x=560, y=310,)


        #DECLARAÇÃO ESCOLAR -----------------
        self.declaracao_var = StringVar()  # Variável de controle

        declaracao_label = customtkinter.CTkLabel(self.nova_janela, text="Declaração\nescolar:", bg_color="#ffffdc",
                                             text_color='black')
        declaracao_label.place(x=475, y=360)
        declaracao_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.declaracao_var, value="Sim",
                                                 bg_color="#ffffdc", text_color='black')
        declaracao_sim.place(x=570, y=360)
        declaracao_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.declaracao_var, value="Não",
                                                 bg_color="#ffffdc", text_color='black')
        declaracao_nao.place(x=630, y=360)


        # VACINAÇÃO ------------------------
        self.vacina_var = StringVar()  # Variável de controle para os botões de opção

        vacina_label = customtkinter.CTkLabel(self.nova_janela, text="A vacinação está\nem dia?", bg_color="#ffffdc", text_color='black')
        vacina_label.place(x=460, y=400)
        vacina_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.vacina_var, value="Sim", bg_color="#ffffdc", text_color='black')
        vacina_sim.place(x=570, y=400)
        vacina_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.vacina_var, value="Não", bg_color="#ffffdc", text_color='black')
        vacina_nao.place(x=630, y=400)

        # TERMO -----------------------------
        self.termo_var = StringVar() #Variável de controle

        termo_label = customtkinter.CTkLabel(self.nova_janela, text="Termo de \nimagem assinado?", bg_color="#ffffdc", text_color='black')
        termo_label.place(x=450, y=440)
        termo_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.termo_var, value="Sim", bg_color="#ffffdc", text_color='black')
        termo_sim.place(x=570, y=440)
        termo_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.termo_var, value="Não", bg_color="#ffffdc", text_color='black')
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
        confirmar_button = customtkinter.CTkButton(self.nova_janela, text="CONFIRMAR", width=170, height=50, corner_radius=15,command=self.salvar_informacoes)
        confirmar_button.place(x=260, y=545)

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

    def salvar_informacoes(self):
        # Coleta os dados dos campos de entrada
        nome = self.nome_entry.get()
        data_nascimento = self.date_entry.get_date()
        telefone = self.telefone_entry.get()
        cpf = self.cpf_responsavel.get()
        rg = self.rg_resp.get()
        nome_resp = self.nome_resp.get()
        projeto = self.projeto.get()
        declaracao = self.declaracao_var.get()
        vacinacao = self.vacina_var.get()
        termo = self.termo_var.get()
        # certidao = self.certidao_var.get()


        # Inserir os dados no banco de dados
        self.cursor.execute('''
        INSERT INTO Crianças (nome, data_nascimento, telefone, cpf_responsavel, rg_resp, nome_resp, projeto, declaracao_escolar, vacinacao, termo_imagem)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        
        ''', (nome, data_nascimento, telefone, cpf, rg, nome_resp, projeto, declaracao, vacinacao, termo))
        conexao.commit()

        # Exibe os dados no console (apenas para verificação)
        print(f"Nome: {nome}")
        print(f"Data de Nascimento: {data_nascimento}")
        print(f"Telefone: {telefone}")
        print(f"CPF do Responsável: {cpf}")
        print(f"RG do Responsável: {rg}")
        print(f"Nome do Responsável: {nome_resp}")
        print(f"Projeto: {projeto}")
        print(f"Declaração Escolar: {declaracao}")
        print(f"Vacinação em dia: {vacinacao}")
        print(f"Termo de imagem assinado: {termo}")
        # print(f"Certidão de Nascimento: {certidao}")



# FIM DA JANELA DE CADASTRO DE CRIANÇAS --------------------------------


# JANELA DE CADASTRO DE VOLUNTARIOS -------------------------------------
    def abrir_janela_cadastro_voluntarios(self):
        self.janela_voluntario = customtkinter.CTkToplevel(self.root)
        self.janela_voluntario.title("Cadastro de Voluntários")
        self.janela_voluntario.iconbitmap("logo.ico")
        self.janela_voluntario.geometry("800x600")
        self.janela_voluntario.resizable(False, False)

        # Configurar grid
        self.janela_voluntario.grid_columnconfigure(0, weight=1)
        self.janela_voluntario.grid_columnconfigure(1, weight=3)

        # Frame na direita -------------
        crianca_frame = customtkinter.CTkFrame(self.janela_voluntario, width=470, height=600, corner_radius=20, fg_color="#ffffdc")
        crianca_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(crianca_frame, text='', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        img = CTkImage(Image.open("logo.png"), size=(310,230))
        self.label_img = customtkinter.CTkLabel(self.janela_voluntario, image=img, text="")
        self.label_img.image = img
        self.label_img.place(x=5, y=100)

        # Nome
        nome_label = customtkinter.CTkLabel(self.janela_voluntario, text="Nome:", bg_color="#ffffdc", text_color='black')
        nome_label.place(x=500, y=120)
        self.nome_entry = customtkinter.CTkEntry(self.janela_voluntario)
        self.nome_entry.place(x=560, y=120, )

        # Telefone --------------------
        telefone_label = customtkinter.CTkLabel(self.janela_voluntario, text="Telefone:", bg_color="#ffffdc", text_color='black')
        telefone_label.place(x=490, y=220)
        self.telefone_entry = customtkinter.CTkEntry(self.janela_voluntario)
        self.telefone_entry.place(x=560, y=220)

        # EMAIL --------------------
        email_label = customtkinter.CTkLabel(self.janela_voluntario, text="Email:", bg_color="#ffffdc", text_color='black')
        email_label.place(x=500, y=170)
        self.email_entry = customtkinter.CTkEntry(self.janela_voluntario)
        self.email_entry.place(x=560, y=170)

        # PROFISSÃO --------------------
        profissao_label = customtkinter.CTkLabel(self.janela_voluntario, text="Profissão:", bg_color="#ffffdc", text_color='black')
        profissao_label.place(x=490, y=270)
        self.profissao_entry = customtkinter.CTkEntry(self.janela_voluntario)
        self.profissao_entry.place(x=560, y=270)

        #PROJETO ----------------------------
        projeto= customtkinter.CTkLabel(self.janela_voluntario, text="Projeto:", bg_color="#ffffdc", text_color='black')
        projeto.place(x=500, y=320)
        self.projeto = customtkinter.CTkEntry(self.janela_voluntario)
        self.projeto.place(x=560, y=320,)

        # Já participou de algum projeto? -----------------------------
        self.participacao_var = StringVar() #Variável de controle

        participacao_label = customtkinter.CTkLabel(self.janela_voluntario, text="Já participou\n de algum projeto?", bg_color="#ffffdc", text_color='black')
        participacao_label.place(x=465, y=370)
        participacao_sim = customtkinter.CTkRadioButton(self.janela_voluntario, text="Sim", variable=self.participacao_var, value="Sim", bg_color="#ffffdc", text_color='black')
        participacao_sim.place(x=585, y=370)
        participacao_nao = customtkinter.CTkRadioButton(self.janela_voluntario, text="Não", variable=self.participacao_var, value="Não", bg_color="#ffffdc", text_color='black')
        participacao_nao.place(x=645, y=370)


        # Botão CONFIRMAR
        confirmar_button = customtkinter.CTkButton(self.janela_voluntario, text="CONFIRMAR", width=170, height=50, corner_radius=15,command=self.salvar_informacoes)
        confirmar_button.place(x=515, y=420)

        # JANELA DE CONSULTA DE CRIANÇAS -------------------------------------
    def abrir_janela_consulta_crianca(self):
        self.consulta_criancas = customtkinter.CTkToplevel(self.root)
        self.consulta_criancas.title("Consulta de crianças")
        self.consulta_criancas.iconbitmap("logo.ico")
        self.consulta_criancas.state('zoomed')
        self.consulta_criancas.resizable(False, False)

        # Configurar grid
        self.consulta_criancas.grid_columnconfigure(0, weight=1)
        self.consulta_criancas.grid_columnconfigure(1, weight=3)

        # Frame para Treeview e Scrollbars
        frame_tree = customtkinter.CTkFrame(self.consulta_criancas)
        frame_tree.pack(padx=1, pady=1, fill="both")

        # Criar a treeview para exibir os dados
        self.tree = ttk.Treeview(self.consulta_criancas, columns=(
        "Nome", "Data de Nascimento", "Telefone", "CPF responsável", "RG responsável", "Nome responsável",
        "Projeto", "Declaração escolar", "Vacinação", "Termo de imagem"), show="headings")

        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Data de Nascimento", text="Data de Nascimento")
        self.tree.heading("Telefone", text="Telefone")
        self.tree.heading("CPF responsável", text="CPF responsável")
        self.tree.heading("RG responsável", text="RG responsável")
        self.tree.heading("Nome responsável", text="Nome responsável")
        self.tree.heading("Projeto", text="Projeto")
        self.tree.heading("Declaração escolar", text="Declaração escolar")
        self.tree.heading("Vacinação", text="Vacinação")
        self.tree.heading("Termo de imagem", text="Termo de imagem")
        self.tree.pack(side="left", fill="both", expand=True)

        # Adicionar barras de rolagem
        scrollbar_vertical = ttk.Scrollbar(frame_tree, orient="vertical", command=self.tree.yview)
        scrollbar_vertical.pack(side="right", fill="y")
        self.tree.configure(yscroll=scrollbar_vertical.set)

        scrollbar_horizontal = ttk.Scrollbar(frame_tree, orient="horizontal", command=self.tree.xview)
        scrollbar_horizontal.pack(side="bottom", fill="x")
        self.tree.configure(xscroll=scrollbar_horizontal.set)

        # Buscar dados do banco de dados e adicionar ao Treeview
        self.cursor.execute('SELECT * FROM Crianças')
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)


# Criação da janela principal
janela = customtkinter.CTk()

# Instanciação da classe App
app = App(janela)

# Iniciar o loop principal da janela
janela.mainloop()