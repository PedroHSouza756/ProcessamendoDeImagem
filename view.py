
# Importa o Tkinter para criar a interface gráfica.
import tkinter as tk

# Importa caixas de diálogo para selecionar arquivos
# e exibir mensagens ao usuário.
from tkinter import filedialog, messagebox

# Importa ImageTk para exibir imagens do Pillow no Tkinter.
from PIL import ImageTk


# Classe responsável pela interface gráfica (View).
class AplicacaoView:

    # Inicializa a janela e seus componentes.
    def __init__(self, janela):
        # Guarda a janela principal.
        self.janela = janela

        # Define o título da janela.
        self.janela.title("Estudo de Manipulação de Imagens")

        # Define o tamanho inicial da janela.
        self.janela.geometry("800x700")

        # Define os tamanhos mínimos permitidos.
        self.janela.minsize(600, 500)

        # Mantém uma referência à imagem exibida.
        # Isso impede que ela seja removida da memória.
        self.foto = None

        # Guarda uma cópia da imagem que será mostrada.
        self.imagem_exibida = None

        # Estas variáveis receberão as funções do Controller.
        # Inicialmente, nenhuma ação está conectada.
        self.on_abrir = None
        self.on_aplicar = None
        self.on_voltar = None
        self.on_salvar = None

        # Cria o título apresentado na janela.
        tk.Label(
            janela,
            text="Manipulação de Imagens - Filtros",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        # Botão que inicia a seleção de uma imagem.
        tk.Button(
            janela,
            text="Abrir imagem JPG",
            command=self.abrir_imagem
        ).pack(pady=4)

        # Guarda o nome do filtro selecionado.
        self.selecao = tk.StringVar(
            value="Escala de cinza"
        )

        # Lista dos filtros disponíveis.
        filtros = [
            "Escala de cinza",
            "Blur",
            "Sobel",
            "Unsharp",
            "Sharpening"
        ]

        # Apresenta a instrução acima do menu.
        tk.Label(
            janela,
            text="Escolha um filtro:"
        ).pack(pady=3)

        # Cria o menu suspenso para escolher o filtro.
        tk.OptionMenu(
            janela,
            self.selecao,
            *filtros
        ).pack(pady=3)

        # Botão para aplicar o filtro selecionado.
        tk.Button(
            janela,
            text="Aplicar filtro",
            command=self.aplicar_filtro
        ).pack(pady=4)

        # Botão para restaurar a imagem original.
        tk.Button(
            janela,
            text="Voltar ao original",
            command=self.voltar_original
        ).pack(pady=4)

        # Botão para salvar a imagem processada.
        tk.Button(
            janela,
            text="Salvar resultado",
            command=self.salvar_imagem
        ).pack(pady=4)

        # Cria a área onde a imagem será exibida.
        self.area_imagem = tk.Label(
            janela,
            text="Abra uma imagem para começar."
        )

        # Faz a área ocupar o espaço disponível da janela.
        self.area_imagem.pack(
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # Detecta mudanças no tamanho da área de imagem.
        # Assim, a prévia pode ser redimensionada.
        self.area_imagem.bind(
            "<Configure>",
            self.redimensionar_imagem
        )

    # Recebe as funções do Controller e conecta os eventos.
    def definir_callbacks(
        self, abrir, aplicar, voltar, salvar
    ):
        self.on_abrir = abrir
        self.on_aplicar = aplicar
        self.on_voltar = voltar
        self.on_salvar = salvar

    # Encaminha o clique em Abrir para o Controller.
    def abrir_imagem(self):
        if self.on_abrir:
            self.on_abrir()

    # Encaminha o filtro selecionado para o Controller.
    def aplicar_filtro(self):
        if self.on_aplicar:
            self.on_aplicar(self.selecao.get())

    # Solicita ao Controller que restaure o original.
    def voltar_original(self):
        if self.on_voltar:
            self.on_voltar()

    # Solicita ao Controller que salve o resultado.
    def salvar_imagem(self):
        if self.on_salvar:
            self.on_salvar()

    # Abre a janela de seleção de imagem.
    def escolher_imagem(self):
        return filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[
                ("Imagens JPG", "*.jpg *.jpeg"),
                ("Todas as imagens", "*.jpg *.jpeg *.png")
            ]
        )

    # Abre a janela para escolher onde salvar o resultado.
    def escolher_destino(self):
        return filedialog.asksaveasfilename(
            title="Salvar resultado",
            defaultextension=".jpg",
            filetypes=[
                ("Imagem JPG", "*.jpg"),
                ("Imagem PNG", "*.png")
            ]
        )

    # Recebe uma imagem e solicita sua exibição.
    def mostrar_imagem(self, imagem):
        # Guarda uma cópia independente da imagem recebida.
        self.imagem_exibida = imagem.copy()

        # Atualiza a prévia na interface.
        self._atualizar_previa()

    # Chamado quando o tamanho da área de imagem muda.
    def redimensionar_imagem(self, evento=None):
        # Só atualiza se houver uma imagem carregada.
        if self.imagem_exibida is not None:
            self._atualizar_previa()

    # Ajusta a imagem para caber na área de visualização.
    def _atualizar_previa(self):
        # Cria uma cópia para não alterar a imagem original.
        previa = self.imagem_exibida.copy()

        # Calcula a largura disponível na interface.
        largura = max(
            100,
            min(740, self.area_imagem.winfo_width() - 20)
        )

        # Calcula a altura disponível na interface.
        altura = max(
            100,
            min(380, self.area_imagem.winfo_height() - 20)
        )

        # Redimensiona a prévia mantendo as proporções.
        previa.thumbnail((largura, altura))

        # Converte a imagem para um formato compatível com Tkinter.
        self.foto = ImageTk.PhotoImage(previa)

        # Atualiza a imagem exibida na tela.
        self.area_imagem.configure(
            image=self.foto,
            text=""
        )

    # Exibe um aviso ao usuário.
    def aviso(self, titulo, mensagem):
        messagebox.showwarning(titulo, mensagem)

    # Exibe uma mensagem de erro.
    def erro(self, titulo, mensagem):
        messagebox.showerror(titulo, mensagem)

    # Exibe uma mensagem de sucesso.
    def sucesso(self, titulo, mensagem):
        messagebox.showinfo(titulo, mensagem)
