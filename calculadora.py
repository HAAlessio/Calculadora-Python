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

        self.digitos = {7:(2, 1), 8:(2, 2), 9:(2, 3), 4:(3, 1), 5:(3, 2), 6:(3, 3), 1:(4, 1), 2:(4, 2), 3:(4, 3), 0:(5, 2), '.':(5, 3)}

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
            self.janela.bind(key, lambda event, operador=key: self.junta_operador(operador))

    def cria_botoes_especiais(self):
        self.cria_botao_limpa()
        self.cria_botao_igual()
        self.cria_botao_potencia()
        self.cria_botao_raiz()
        self.cria_botao_negate()
        self.cria_botao_porcentagem()
        self.cria_botao_fracao()
        self.cria_botao_pi()

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
            botao = tk.Button(self.botoes_frame, text=str(digit), bg=CINZA_CLARO, fg=COR_DIGITO, font=FONTE_DIGITO,
                               borderwidth=0, command=lambda x=digit: self.adiciona_expressao(x))
            botao.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def junta_operador(self, operador):
        self.expressao_atual += operador
        self.expressao += self.expressao_atual
        self.expressao_atual = ''
        self.atualiza_label_geral()
        self.atualiza_label()

    def cria_botoes_operadores(self):
        i = 1
        for operador, symbol in self.operacoes.items():
            botao = tk.Button(self.botoes_frame, text=symbol, bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                               borderwidth=0, command=lambda x=operador: self.junta_operador(x))
            botao.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def limpa(self):
        self.expressao_atual = ''
        self.expressao = ''
        self.atualiza_label()
        self.atualiza_label_geral()

    def cria_botao_limpa(self):
        botao = tk.Button(self.botoes_frame, text='C', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.limpa)
        botao.grid(row=0, column=3, sticky=tk.NSEW, columnspan=2)

    def potencia(self):
        self.expressao_atual = str(eval(f'{self.expressao_atual}**2'))
        self.atualiza_label()

    def cria_botao_potencia(self):
        botao = tk.Button(self.botoes_frame, text='x\u00b2', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.potencia)
        botao.grid(row=1, column=2, sticky=tk.NSEW)

    def raiz(self):
        self.expressao_atual = str(eval(f'{self.expressao_atual}**0.5'))
        self.atualiza_label()

    def cria_botao_raiz(self):
        botao = tk.Button(self.botoes_frame, text='\u221ax', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.raiz)
        botao.grid(row=1, column=3, sticky=tk.NSEW)

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
        botao = tk.Button(self.botoes_frame, text='=', bg=LARANJA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.avalia)
        botao.grid(row=5, column=4, columnspan=1, sticky=tk.NSEW)

    def negate(self):
        if self.expressao_atual not in self.operacoes:
            self.expressao_atual = str(float(self.expressao_atual) * -1)
            self.atualiza_label()

    def cria_botao_negate(self):
        botao = tk.Button(self.botoes_frame, text='+/-', bg=CINZA_CLARO, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.negate)
        botao.grid(row=5, column=1, columnspan=1, sticky=tk.NSEW)

    def porcentagem(self):
        self.expressao_atual = str(float(self.expressao_atual) / 100)
        self.atualiza_label()

    def cria_botao_porcentagem(self):
        botao = tk.Button(self.botoes_frame, text='%', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.porcentagem)
        botao.grid(row=0, column=2, columnspan=1, sticky=tk.NSEW)

    def pi(self):
        pi = 3.1415926535897932384626433832795
        self.expressao_atual = "{:.2f}".format(pi)
        self.atualiza_label()

    def cria_botao_pi(self):
        botao = tk.Button(self.botoes_frame, text='π', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.pi)
        botao.grid(row=0, column=1, columnspan=1, sticky=tk.NSEW)

    def fracao(self):
        self.expressao_atual = str(1 / float(self.expressao_atual))
        self.atualiza_label()

    def cria_botao_fracao(self):
        botao = tk.Button(self.botoes_frame, text='1/x', bg=CINZA, fg=COR_DIGITO, font=FONTE_DEFAULT,
                           borderwidth=0, command=self.fracao)
        botao.grid(row=1, column=1, columnspan=1, sticky=tk.NSEW)

    def cria_botoes_frame(self):
        frame = tk.Frame(self.janela)
        frame.pack(expand=True, fill='both')
        return frame

    def atualiza_label_geral(self):
        expression = self.expressao
        for operador, symbol in self.operacoes.items():
            expression = expression.replace(operador, f' {symbol} ')
        self.label_geral.config(text=expression)

    def atualiza_label(self):
        self.label.config(text=self.expressao_atual[:11])

    def roda(self):
        self.janela.mainloop()


if __name__ == '__main__':
    calc = Calculadora()
    calc.roda()
