from tkinter import filedialog

import customtkinter
from customtkinter import CTkImage
from tkinter import *
from PIL import Image  # Importação correta do Pillow
from tkcalendar import Calendar, DateEntry


class App:
    def __init__(self, root):
        self.root = root
        self.tema()
        self.create_widgets()
        self.aparencia()

    def tema(self):
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("dark-blue")


    def create_widgets(self):
        self.root.geometry("700x500")
        self.root.title("Sempre criança")
        self.root.iconbitmap("icone.ico")
        self.root.resizable(False, False)


        # Usando CTkImage ao invés de PhotoImage
        img = CTkImage(Image.open("icon.png"), size=(310, 230))
        self.label_img = customtkinter.CTkLabel(master=self.root, image=img, text="")
        self.label_img.image = img  # Mantenha a referência à imagem
        self.label_img.place(x=5, y=100)  # Ajuste o posicionamento da imagem conforme necessário

        # Frame na direita -------------
        cadastro_frame = customtkinter.CTkFrame(master=self.root, width=370, height=500, corner_radius=20, fg_color="#ffffdc")
        cadastro_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(master=cadastro_frame, text='Gerenciador - Sempre Criança', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        # BOTÕES DA JANELA PRINCIPAL -------
        cadastrar_criancas_button = customtkinter.CTkButton(master=cadastro_frame, text="Cadastrar crianças", width=140, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10, command=self.abrir_janela_cadastro_criancas)
        cadastrar_criancas_button.place(x=20, y=150)

        cadastrar_voluntarios_button = customtkinter.CTkButton(master=cadastro_frame, text="Cadastrar voluntários", width=100, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10)
        cadastrar_voluntarios_button.place(x=200, y=150)

        consultar_criancas_button = customtkinter.CTkButton(master=cadastro_frame, text="Consultar Crianças", width=140, height=50, fg_color="#FFD700", text_color="#1e1e1e", corner_radius=10)
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
        self.nova_janela.iconbitmap("icone.ico")
        self.nova_janela.geometry("700x500")
        self.nova_janela.resizable(False, False)

        # Configurar grid
        self.nova_janela.grid_columnconfigure(0, weight=1)
        self.nova_janela.grid_columnconfigure(1, weight=3)

        # Frame na direita -------------
        crianca_frame = customtkinter.CTkFrame(self.nova_janela, width=370, height=500, corner_radius=20, fg_color="#ffffdc")
        crianca_frame.pack(side=RIGHT, padx=0, pady=0)

        label = customtkinter.CTkLabel(crianca_frame, text='', font=('Roboto', 20, 'bold'), text_color='black')
        label.place(x=35, y=50)

        img = CTkImage(Image.open("icon.png"), size=(310,230))
        self.label_img = customtkinter.CTkLabel(self.nova_janela, image=img, text="")
        self.label_img.image = img  # Mantenha a referência à imagem
        self.label_img.place(x=5, y=100)  # Ajuste o posicionamento da imagem conforme necessário

        # Nome
        nome_label = customtkinter.CTkLabel(self.nova_janela, text="Nome:", bg_color="#ffffdc", text_color='black')
        nome_label.place(x=430, y=10)
        self.nome_entry = customtkinter.CTkEntry(self.nova_janela)
        self.nome_entry.place(x=490, y=10,)

        # Data de nascimento
        dt_nasc = customtkinter.CTkLabel(self.nova_janela, text="Data de\nNascimento:", bg_color="#ffffdc", text_color='black')
        dt_nasc.place(x=415, y=50)

        self.date_entry = DateEntry(self.nova_janela, width=12, background='#f2f28d', foreground='black', borderwidth=2, date_pattern="dd/MM/yyyy")
        self.date_entry.place(x=500, y=55)  # Ajuste a posição conforme necessário

        # self.data_nasc_entry = customtkinter.CTkEntry(self.nova_janela)
        # self.data_nasc_entry.place(x=80, y=50,)

        # Telefone --------------------
        telefone_label = customtkinter.CTkLabel(self.nova_janela, text="Telefone:", bg_color="#ffffdc", text_color='black')
        telefone_label.place(x=420, y=90)
        self.telefone_entry = customtkinter.CTkEntry(self.nova_janela)
        self.telefone_entry.place(x=490, y=90,)

        #CPF -----------------------
        cpf_responsavel = customtkinter.CTkLabel(self.nova_janela, text="CPF do \nResponsável:" , bg_color="#ffffdc", text_color='black')
        cpf_responsavel.place(x=410, y=130)
        self.cpf_responsavel = customtkinter.CTkEntry(self.nova_janela)
        self.cpf_responsavel.place(x=490, y=135,)

        #RG ------------------
        rg_resp = customtkinter.CTkLabel(self.nova_janela, text="RG do \nResponsável:", bg_color="#ffffdc", text_color='black')
        rg_resp.place(x=410, y=175)
        self.rg_resp = customtkinter.CTkEntry(self.nova_janela)
        self.rg_resp.place(x=490, y=180,)

        # VACINAÇÃO ------------------------
        self.vacina_var = StringVar()  # Variável de controle para os botões de opção

        vacina_label = customtkinter.CTkLabel(self.nova_janela, text="A vacinação está\nem dia?:", bg_color="#ffffdc", text_color='black')
        vacina_label.place(x=400, y=230)
        vacina_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.vacina_var, value="Sim", bg_color="#ffffdc", text_color='black')
        vacina_sim.place(x=530, y=220)
        vacina_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.vacina_var, value="Não", bg_color="#ffffdc", text_color='black')
        vacina_nao.place(x=530, y=250)

        # TERMO -----------------------------
        self.termo_var = StringVar() #Variável de controle

        termo_label = customtkinter.CTkLabel(self.nova_janela, text="O termo está\nassinado?:", bg_color="#ffffdc", text_color='black')
        termo_label.place(x=410, y=300)
        termo_sim = customtkinter.CTkRadioButton(self.nova_janela, text="Sim", variable=self.termo_var, value="Sim", bg_color="#ffffdc", text_color='black')
        termo_sim.place(x=530, y=290)
        termo_nao = customtkinter.CTkRadioButton(self.nova_janela, text="Não", variable=self.termo_var, value="Não", bg_color="#ffffdc", text_color='black')
        termo_nao.place(x=530, y=320)

        # Certidão de nascimento (PDF)
        self.certidao_var = StringVar()  # Variável de controle para o caminho do arquivo PDF

        certidao_label = customtkinter.CTkLabel(self.nova_janela, text="Certidão de Nascimento (PDF):", bg_color="#ffffdc", text_color='black')
        certidao_label.place(x=410, y=360)
        certidao_button = customtkinter.CTkButton(self.nova_janela, text="Selecionar Arquivo", bg_color="#ffffdc",
                                                  command=self.selecionar_certidao)
        certidao_button.place(x=430, y=390)

        # Botão CONFIRMAR
        confirmar_button = customtkinter.CTkButton(self.nova_janela, text="CONFIRMAR", width=170, height=50, corner_radius=15,command=self.salvar_informacoes)
        confirmar_button.place(x=250, y=440)

    def selecionar_certidao(self):
        # filepath = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo",
        #                                       filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
        # Exibe a janela de seleção de arquivo para salvar o PDF
        filepath = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                filetypes=(("Arquivos PDF", "*.pdf"), ("Todos os arquivos", "*.*")))
        if filepath:
            # Aqui você pode adicionar código para salvar o arquivo PDF usando o caminho 'filepath'
            customtkinter.messagebox.showinfo("Sucesso", f"Arquivo PDF salvo em:\n{filepath}")
        else:
            customtkinter.messagebox.showwarning("Cancelado", "Nenhum arquivo foi selecionado para salvar.")


    def salvar_informacoes(self):
        # Coleta os dados dos campos de entrada
        nome = self.nome_entry.get()
        data_nasc = self.date_entry.get()
        telefone = self.telefone_entry.get()
        cpf = self.cpf_responsavel.get()
        rg = self.rg_resp.get()
        vacinacao = self.vacina_var.get()
        termo = self.termo_var.get()
        certidao = self.certidao_var.get()

        # Adicione aqui o código para salvar os dados
        # Pode ser em um banco de dados, arquivo, etc.
        # Por exemplo:
        print(f"Nome: {nome}")
        print(f"Data de Nascimento: {data_nasc}")
        print(f"Telefone: {telefone}")
        print(f"CPF do Responsável: {cpf}")
        print(f"RG do Responsável: {rg}")
        print(f"Vacinação em dia: {vacinacao}")
        print(f"Termo assinado: {termo}")
        print(f"Certidão de Nascimento: {certidao}")


# FIM DA JANELA DE CADASTRO DE CRIANÇAS --------------------------------




# Criação da janela principal
janela = customtkinter.CTk()

# Instanciação da classe App
app = App(janela)

# Iniciar o loop principal da janela
janela.mainloop()