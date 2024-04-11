import tkinter as tk

FONTE_G = ('Arial', 40, 'bold')
FONTE_P = ('Arial', 16)
FONTE_DIGITO = ('Arial', 24, 'bold')
FONTE_DEFAULT = ('Arial', 20)

CINZA = '#303431'
CINZA_CLARO = '#3A3C3A'
LARANJA = '#FF7F27'
CINZA_ESCURO = '#1E211F'
COR_DIGITO = 'white'


class Calculadora:
    def __init__(self):
        self.janela = tk.Tk()
        self.janela.geometry('320x500')
        self.janela.resizable(0, 0)
        self.janela.title('Calculadora')
        self.janela.iconbitmap('C://Users/hurie/OneDrive/Documentos/Python/Calculadora/icone.ico')

        self.expressao = ''
        self.expressao_atual = ''
        self.display_frame = self.cria_display()

        self.label_geral, self.label = self.cria_display_label()

        self.digitos = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 3)
        }
        self.operacoes = {'/': '\u00F7', '*': '\u00D7', '-': '-', '+': '+'}
        self.botoes_frame = self.cria_botoes_frame()

        self.botoes_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.botoes_frame.rowconfigure(x, weight=1)
            self.botoes_frame.columnconfigure(x, weight=1)
        self.cria_botoes_digitos()
        self.cria_botoes_operadores()
        self.cria_botoes_especiais()
        self.bind_keys()

    def bind_keys(self):
        self.janela.bind('<Return>', lambda event: self.avalia())
        for key in self.digitos:
            self.janela.bind(str(key), lambda event, digit=key: self.adiciona_expressao(digit))

        for key in self.operacoes:
            self.janela.bind(key, lambda event, operator=key: self.junta_operador(operator))

    def cria_botoes_especiais(self):
        self.cria_botao_limpa()
        self.cria_botao_igual()
        self.cria_botao_potencia()
        self.cria_botão_raiz()
        self.cria_botão_negate()

    def cria_display_label(self):
        label_geral = tk.Label(self.display_frame, text=self.expressao, anchor=tk.E, bg=CINZA_ESCURO,
                               fg=COR_DIGITO, padx=24, font=FONTE_P)
        label_geral.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.expressao_atual, anchor=tk.E, bg=CINZA_ESCURO,
                         fg=COR_DIGITO, padx=24, font=FONTE_G)
        label.pack(expand=True, fill='both')

        return label_geral, label

    def cria_display(self):
        frame = tk.Frame(self.janela, height=221, bg=CINZA_ESCURO)
        frame.pack(expand=True, fill='both')
        return frame

    def adiciona_expressao(self, value):
        self.expressao_atual += str(value)
        self.atualiza_label()

    def cria_botoes_digitos(self):
        for digit, grid_value in self.digitos.items():
            button = tk.Button(self.botoes_frame, text=str(digit), bg=CINZA_CLARO, fg=COR_DIGITO, font=FONTE_DIGITO,
                               borderwidth=0, command=lambda x=digit: self.adiciona_expressao(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def junta_operador(self, operator):
        self.expressao_atual += operator
        self.expressao += self.expressao_atual
        self.expressao_atual = ''
        self.atualiza_label_geral()
        self.atualiza_label()

    def cria_botoes_operadores(self):
        i = 0
        for operator, symbol in self.operacoes.items():
            button = tk.Button(self.botoes_frame, text=symbol, bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                               borderwidth=0, command=lambda x=operator: self.junta_operador(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def limpa(self):
        self.expressao_atual = ''
        self.expressao = ''
        self.atualiza_label()
        self.atualiza_label_geral()

    def cria_botao_limpa(self):
        button = tk.Button(self.botoes_frame, text='C', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.limpa)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def potencia(self):
        self.expressao_atual = str(eval(f'{self.expressao_atual}**2'))
        self.atualiza_label()

    def cria_botao_potencia(self):
        button = tk.Button(self.botoes_frame, text='x\u00b2', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.potencia)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def raiz(self):
        self.expressao_atual = str(eval(f'{self.expressao_atual}**0.5'))
        self.atualiza_label()

    def cria_botão_raiz(self):
        button = tk.Button(self.botoes_frame, text='\u221ax', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.raiz)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def avalia(self):
        self.expressao += self.expressao_atual
        self.atualiza_label_geral()
        try:
            self.expressao_atual = str(eval(self.expressao))

            self.expressao = ''
        except Exception as e:
            self.expressao_atual = 'Error'
        finally:
            self.atualiza_label()

    def cria_botao_igual(self):
        button = tk.Button(self.botoes_frame, text='=', bg=LARANJA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.avalia)
        button.grid(row=4, column=4, columnspan=1, sticky=tk.NSEW)

    def negate(self):
        self.expressao_atual = self.expressao_atual * -1
        self.atualiza_label

    def cria_botão_negate(self):
        button = tk.Button(self.botoes_frame, text='+/-', bg=CINZA_CLARO, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.negate)
        button.grid(row=4, column=1, columnspan=1, sticky=tk.NSEW)

    def cria_botoes_frame(self):
        frame = tk.Frame(self.janela)
        frame.pack(expand=True, fill='both')
        return frame

    def atualiza_label_geral(self):
        expression = self.expressao
        for operator, symbol in self.operacoes.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.label_geral.config(text=expression)

    def atualiza_label(self):
        self.label.config(text=self.expressao_atual[:11])

    def roda(self):
        self.janela.mainloop()


if __name__ == '__main__':
    calc = Calculadora()
    calc.roda()
