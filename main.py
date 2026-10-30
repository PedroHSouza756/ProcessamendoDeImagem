
# Importa o Tkinter para criar a janela principal.
import tkinter as tk

# Importa a classe responsável pela interface.
from view import AplicacaoView

# Importa a classe responsável pelo controle do programa.
from controller import AplicacaoController


# Função principal que inicia a aplicação.
def main():
    # Cria a janela principal do programa.
    janela = tk.Tk()

    # Cria a interface gráfica dentro da janela.
    view = AplicacaoView(janela)

    # Cria o Controller e conecta suas ações à View.
    controller = AplicacaoController(view)

    # Inicia o loop de eventos.
    # Mantém a janela aberta e permite interagir com os botões.
    janela.mainloop()


# Verifica se este arquivo foi executado diretamente.
# Se foi, inicia o programa pela função main().
if __name__ == "__main__":
    main()
