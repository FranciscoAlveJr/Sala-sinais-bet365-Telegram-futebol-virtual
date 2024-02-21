
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

    def resolucao(self) -> tuple:
        s = pyautogui.size()
        size = s.width, s.height
        return size

    def posicao_mouse(self):
        p = pyautogui.position()
        position = p.x, p.y
        print(position)

    def login(self, usuario, senha):
        # Maximiza a tela
        # pyautogui.hotkey('win', 'up')

        # Fecha aviso, se tiver
        pyautogui.click(1352, 100)

        # Clicar em Login amarelo
        pyautogui.click(1302, 152)

        # Clica/limpa no campo do usuário
        pyautogui.click(846, 226)

        # Escreve no campo do usuário
        pyautogui.write(usuario)

        # Clica e limpa no campo da senha
        pyautogui.click(825, 287)
        pyautogui.hotkey('ctrl', 'backspace')

        # Escreve no campo da senha
        pyautogui.write(senha)

        # Clicar em login verde
        pyautogui.click(661, 353)

    def campeonatos(self, campeonato):
        copa = 447, 299
        euro = 574, 308
        super = 723, 307
        premier = 888, 304

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
        pyautogui.click(x=790, y=644)
        pyautogui.scroll(-900)

        # Clica para a aposta em "Sim" de "Ambos os Times"
        pyautogui.click(x=934, y=451)

        # Clica no campo para digitar o valor da aposta
        pyautogui.click(x=501, y=654)

        # Digita o valor da aposta
        pyautogui.write(aposta, interval=0.25)

        # Clica em Fazer aposta
        pyautogui.click(x=822, y=652)

        # Clica uma vez para sair da janela e uma segunda na aba Minhas Apostas
        pyautogui.click(x=784, y=152)
        pyautogui.click(x=784, y=152)

        # Em Minhas Apostas, clica na aba Todos
        pyautogui.click(x=400, y=222)

    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binario = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # edges = cv2.Canny(binario, 100, 200)

        return binario

    def rec_img(self):
        pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        region = 1129, 244, 188, 46

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
    # bet.delay(1.5)
    # sleep(2)
    r = bet.resolucao()
    print(r == (1920, 1080))
    # bet.posicao_mouse()
    # bet.abrir_browser()
    # sleep(10)
    # bet.login('patriciasv0901', 'patricia@0659123')
    # sleep(5)
    # bet.campeonatos('PREMIER')
    # a = 1
    # for i in range(4):
    #     bet.fazer_aposta(str(a))
        
    #     result = bet.rec_img()
    #     while result == None:
    #         result = bet.rec_img()
    #         print(result)
    #         sleep(1)
    #         continue

    #     if result == 'Ganho':
    #         print('Deu ganho!')
    #         break
    #     elif result == 'Perda':
    #         if i == 3:
    #             print('Deu perda.')
    #         else:
    #             print('Deu perda. Dobrando aposta.')
    #             a *= 2
    #             sleep(1)
    #         pyautogui.hotkey('alt', 'left')
    #         sleep(1)
    #         continue
    