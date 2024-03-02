import pyautogui
import webbrowser
import subprocess
from time import sleep
import cv2
from pytesseract import pytesseract
import numpy as np


class Bet365:
    
    def abrir_browser(self):
        chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        url = "https://www.bet365.com/#/AVR/B146/R^1/"

        subprocess.Popen([chrome_path, "--new-window", "--start-maximized", url])
        # webbrowser.open(url)

    def delay(self, t):
        pyautogui.PAUSE = t

    def resolucao(self):
        s = pyautogui.size()
        size = s.width, s.height
        print(size)

    def posicao_mouse(self):
        p = pyautogui.position()
        position = p.x, p.y
        print(position)

    def login(self, usuario, senha):
        # Maximiza a tela
        # pyautogui.hotkey('win', 'up')

        # Fecha aviso, se tiver
        pyautogui.click(x=1898, y=116)

        # Clicar em Login amarelo
        pyautogui.click(x=1655, y=160)

        # Clica/limpa no campo do usuário
        pyautogui.click(x=1125, y=237)

        # Escreve no campo do usuário
        pyautogui.write(usuario)

        # Clica e limpa no campo da senha
        pyautogui.click(x=1087, y=305)
        pyautogui.hotkey('ctrl', 'backspace')

        # Escreve no campo da senha
        pyautogui.write(senha)

        # Clicar em login verde
        pyautogui.click(x=947, y=378)

    def campeonatos(self, campeonato):
        copa = 652, 310
        euro = 818, 319
        super = 977, 309
        premier = 1125, 315

        # Clicar nas ligas
        if campeonato == 'PREMIER':
            pyautogui.click(x=premier[0], y=premier[1])
        elif campeonato == 'SUPER':
            pyautogui.click(x=super[0], y=super[1])
        elif campeonato == 'EURO':
            pyautogui.click(x=euro[0], y=euro[1])
        elif campeonato == 'COPA':
            pyautogui.click(x=copa[0], y=copa[1])

    def fazer_aposta(self, aposta: str):
        # Move para a tela de odds e rola a página
        pyautogui.click(x=1055, y=633)
        pyautogui.scroll(-300)

        # Clica para a aposta em "Sim" de "Ambos os Times"
        pyautogui.click(x=1235, y=946)

        # Clica no campo para digitar o valor da aposta
        pyautogui.click(x=824, y=965)

        # Digita o valor da aposta
        pyautogui.write(aposta, interval=0.25)

        # Clica em Fazer aposta
        pyautogui.click(x=1067, y=965)

        # Clica uma vez para sair da janela e uma segunda na aba Minhas Apostas
        pyautogui.click(x=1078, y=160)
        pyautogui.click(x=1078, y=160)

        # Em Minhas Apostas, clica na aba Todos
        pyautogui.click(x=643, y=215)

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binario = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # edges = cv2.Canny(binario, 100, 200)

        return binario

    def rec_img(self):
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        region = 1447, 242, 190, 48

        tela = pyautogui.screenshot(region=region)
        tela.save('data\screenshot.png')

        screen = cv2.imread('data\screenshot.png')

        text = pytesseract.image_to_string(screen)
        print(text)

        if 'Obtido' in text.split():
            return'Ganho'
        elif 'Perdida' in text.split():
            return 'Perda'


if __name__=='__main__':
    bet = Bet365()
    # print(bet.rec_img())
    bet.delay(1.5)
    sleep(2)
    bet.resolucao()
