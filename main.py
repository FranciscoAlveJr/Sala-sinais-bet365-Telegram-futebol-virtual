from telbot import pegar_sinais
from time import sleep
from datetime import datetime
import pyautogui
import pytz
from dotenv import set_key, dotenv_values, load_dotenv
import os
import logging

from tkinter import *
from tkinter import messagebox

def minuto_atual():
    """
    Retorna o minuto atual.
    """
    agora = datetime.now()
    
    return agora.minute

def hora_atual():
    """
    Retorna a hora atual de GMT.
    """
    agora = datetime.now()
    gmt = pytz.timezone('GMT')
    agora_gmt = agora.astimezone(gmt)

    return str(agora_gmt.hour)

def current_time():
    agora = datetime.now()
    time_f = agora.strftime('%H:%M')
    time = time_f.split(':')

    return time

def load_env():
    env_values = dict(dotenv_values('data\.env'))
    usuario = env_values['usuario']
    senha = env_values['senha']

    return {'usuario': usuario, 'senha': senha}


class Sinais:
    def main(self):
        # Usuário, senha e valor da aposta
        load_dotenv('data\.env')
        user = os.getenv('usuario')
        senha = os.getenv('senha')

        if user == '' or senha == '':
            messagebox.showerror('ERRO', 'Não existe usuário ou senha cadastrada.')
            return None

        self.janela.destroy()
        
        print('Valor da aposta:')
        valor = int(input())
        print()

        # Verifica a resolução da tela
        s = pyautogui.size()
        size = s.width, s.height
        if size == (1920, 1080):
            from auto_bet365_1080 import Bet365
        elif size == (1366, 768):
            from auto_bet365_768p import Bet365

        # Abre o navegador no bet365
        bet = Bet365()
        bet.delay(1)
        bet.abrir_browser()
        sleep(10)
        bet.login(user, senha)
        sleep(5)

        t = 1
        time = current_time()
        h = int(time[0])

        while True:
            target_hour = f'{h+t}:00'
            sleep(1)

            time = current_time()
            time_f = f'{time[0]}:{time[1]}'

            if time_f != target_hour:
                continue
                
            while True:
                # Pega os sinais do Telegram
                print('Pegando novos sinais do Telegram...')
                logging.info('Pegando novos sinais do Telegram...')
                print()
                sinais = pegar_sinais()

                if sinais == None:
                    continue

                sleep(1)

                campeonato = sinais['campeonato']
                minutos = sinais['minutos']
                hora_sinal = sinais['hora']
                msg_time = sinais['msg_time']
                msg_hour = msg_time.hour

                hora_gmt_atual = hora_atual()

                # Verifica se a hora da mensagem é igual a hora atual(GMT)
                if str(msg_hour) != hora_gmt_atual:
                    continue

                # Verica se a hora do sinal é a mesma da hora atual(GMT)
                if hora_gmt_atual != hora_sinal:
                    continue

                qtd_minutos = len(minutos)

                # Clica no campeonato certo
                bet.campeonatos(campeonato)

                min_atual = minuto_atual()

                minuto_sinal = int(minutos[0])

                # Verifica se o atual é menor que o minuto do sinal
                if min_atual >= minuto_sinal:
                    continue

                # Espera até o minuto antes de encerrar as apostas
                while min_atual < minuto_sinal - 1:
                    min_atual = minuto_atual()
                    continue

                break

            # Aposta no Bet365
            for i, inicio_partida in enumerate(minutos):
                bet.fazer_aposta(str(valor))

                result = bet.rec_img()
                while result == None:
                    result = bet.rec_img()
                    sleep(2)
                    min_atual = minuto_atual()
                    if min_atual == int(inicio_partida) + 3:
                        print('GANHO!')
                        break
                    continue

                if result == 'Ganho':
                    print('GANHO!')
                    pyautogui.hotkey('alt', 'left')
                    break
                elif result == 'Perda':
                    if i == 3:
                        print('Deu perda.')
                    else:
                        print('Deu perda. Dobrando aposta.')
                        valor *= 2
                        sleep(1)
                    pyautogui.hotkey('alt', 'left')
                    sleep(1)
                    continue

            t += 1

    def interface(self):
        self.janela = Tk()
        self.janela.title('Sinais Telegram')
        self.janela.resizable(False, False)

        def cadastrar_login():
            janela2 = Toplevel(self.janela)
            janela2.title('Cadastrar Login')
            janela2.focus_force()

            load_dotenv('data\.env')
            usuario = os.getenv('usuario')        

            frame2 = LabelFrame(janela2, text=' Informe os dados de login ')
            frame2.pack(fill=BOTH, expand=False, padx=10, pady=10, ipadx=10, ipady=10)

            Label(frame2, text='Login registrado: ').grid(pady=10, padx=10, row=0)
            luser = Label(frame2, text=f'Login registrado: {usuario}')
            luser.place(x=10, y=10)

            Label(frame2, text='Usuário: ').grid(row=1, column=0)
            vusuario = Entry(frame2, bg='white', borderwidth=2, width=50)
            vusuario.grid(row=1, column=1, padx=10, pady=10)

            Label(frame2, text='Senha: ').grid(row=2, column=0)
            vsenha = Entry(frame2, bg='white', borderwidth=2, width=50)
            vsenha.grid(row=2, column=1, padx=10, pady=10)

            sucesso = Label(frame2, text='', fg='green')
            sucesso.place(x=130, y=120)

            def set_env():
                usuario = vusuario.get().strip()
                senha = vsenha.get().strip()

                if usuario == '' or senha == '':
                    sucesso.config(text='USUÁRIO E SENHA DEVEM SER INSERIDOS', fg='red')
                    janela2.update()
        
                else:
                    set_key('data\.env', 'usuario', usuario)
                    set_key('data\.env', 'senha', senha)

                    load_dotenv()
                    usuario = os.getenv('usuario')    

                    luser.config(text=f'Usuário registrado: {usuario}')

                    sucesso.config(text='USUÁRIO REGISTRADO COM SUCESSO!', fg='green')

                    vusuario.delete(0, END)
                    vsenha.delete(0, END)

                    janela2.update()

            btn_confirmar = Button(frame2, text='Confirmar', width=15, command=set_env)
            btn_confirmar.grid(row=3, columnspan=2, pady=20)

        frame = LabelFrame(self.janela, text=' O que deseja fazer primeiro? ')
        frame.pack(fill=BOTH, expand=False, padx=10, pady=10, ipadx=10, ipady=10)

        btn_iniciar = Button(frame, text='Iniciar bot', width=30, command=self.main)
        btn_iniciar.pack(padx=20, pady=20)

        btn_cadastrar = Button(frame, text='Cadastrar login', width=30, command=cadastrar_login)
        btn_cadastrar.pack(padx=20, pady=20)

        self.janela.mainloop()

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s', filename='log.log')

    try:
        sinais = Sinais()
        sinais.interface()
    except Exception as erro:
        logging.exception(erro)