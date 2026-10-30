
# Importa Image para abrir e converter as imagens.
from PIL import Image

# Importa o Model, onde estão as funções dos filtros.
import model


# Classe responsável pela lógica de controle (Controller).
class AplicacaoController:

    # Recebe a View que será controlada.
    def __init__(self, view):
        self.view = view

        # Guarda a imagem original sem filtros.
        self.imagem_original = None

        # Guarda o resultado do filtro aplicado.
        self.imagem_resultado = None

        # Registra os métodos que serão chamados pelos botões.
        self.view.definir_callbacks(
            abrir=self.abrir_imagem,
            aplicar=self.aplicar_filtro,
            voltar=self.voltar_original,
            salvar=self.salvar_imagem
        )

    # Abre uma imagem escolhida pelo usuário.
    def abrir_imagem(self):
        # Pede à View que abra a janela de seleção.
        caminho = self.view.escolher_imagem()

        # Se o usuário cancelar, não faz nada.
        if not caminho:
            return

        try:
            # Abre o arquivo e converte para RGB.
            # A imagem original fica independente do arquivo.
            with Image.open(caminho) as arquivo:
                self.imagem_original = arquivo.convert("RGB")

            # Limpa o resultado anterior.
            self.imagem_resultado = None

            # Mostra a imagem original na interface.
            self.view.mostrar_imagem(self.imagem_original)

        except Exception as erro:
            # Informa se ocorreu algum problema ao abrir.
            self.view.erro(
                "Erro",
                f"Não foi possível abrir a imagem:\n{erro}"
            )

    # Aplica o filtro selecionado pelo usuário.
    def aplicar_filtro(self, nome_filtro):
        # Verifica se alguma imagem foi carregada.
        if self.imagem_original is None:
            self.view.aviso(
                "Atenção",
                "Abra uma imagem primeiro."
            )
            return

        try:
            # Envia o nome do filtro e a imagem original ao Model.
            # Cada filtro sempre parte do original, evitando
            # acumular alterações de filtros anteriores.
            self.imagem_resultado = model.aplicar_filtro(
                nome_filtro,
                self.imagem_original
            )

            # Exibe o resultado devolvido pelo Model.
            self.view.mostrar_imagem(self.imagem_resultado)

        except Exception as erro:
            # Exibe qualquer erro ocorrido durante o processamento.
            self.view.erro(
                "Erro",
                f"Não foi possível aplicar o filtro:\n{erro}"
            )

    # Restaura a imagem que foi carregada inicialmente.
    def voltar_original(self):
        # Verifica se há uma imagem original.
        if self.imagem_original is None:
            self.view.aviso(
                "Atenção",
                "Abra uma imagem primeiro."
            )
            return

        # Descarta o resultado do filtro atual.
        self.imagem_resultado = None

        # Exibe novamente a imagem sem alterações.
        self.view.mostrar_imagem(self.imagem_original)

    # Salva o resultado do filtro aplicado.
    def salvar_imagem(self):
        # Impede salvar quando não existe resultado.
        if self.imagem_resultado is None:
            self.view.aviso(
                "Atenção",
                "Aplique um filtro antes de salvar."
            )
            return

        # Solicita à View o caminho do arquivo de destino.
        caminho = self.view.escolher_destino()

        # Se o usuário cancelar, encerra a operação.
        if not caminho:
            return

        try:
            # Obtém a imagem processada.
            imagem = self.imagem_resultado

            # JPG não suporta imagens em escala de cinza
            # como modo L? Pillow normalmente suporta L em JPEG,
            # mas RGB garante compatibilidade com esse formato.
            if caminho.lower().endswith((".jpg", ".jpeg")):
                imagem = imagem.convert("RGB")

            # Salva a imagem no local selecionado.
            imagem.save(caminho)

            # Informa que a operação foi concluída.
            self.view.sucesso(
                "Sucesso",
                "Imagem salva com sucesso!"
            )

        except Exception as erro:
            # Informa se ocorreu algum problema ao salvar.
            self.view.erro(
                "Erro",
                f"Não foi possível salvar a imagem:\n{erro}"
            )
