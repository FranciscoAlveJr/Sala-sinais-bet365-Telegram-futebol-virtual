from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
import re
import emoji
import asyncio
from time import sleep
import os
from dotenv import load_dotenv


def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # símbolos & pictogramas
                               u"\U0001F680-\U0001F6FF"  # transporte & símbolos mapas
                               u"\U0001F1E0-\U0001F1FF"  # bandeiras (iOS)
                               u"\U00002500-\U00002BEF"  # chineses, japoneses, coreanos unificados
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u200d"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\u3030"
                               u"\ufe0f"
                               "Não se atrase! ⏰"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

load_dotenv('my_auth/.env')

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('NUMBER')

# Nome do grupo que você quer monitorar
group_name = '[VIP] - ARENA | AMBAS MARCAM'

async def main():
    async with TelegramClient('anon', api_id, api_hash) as client:
        try:
            await client.start()
        except SessionPasswordNeededError:
            await client.start(phone_number)

        # Encontrar o ID do grupo pelo nome
        async for dialog in client.iter_dialogs():
            if dialog.name == group_name:
                group_id = dialog.id
                break

        # Monitorar as mensagens do grupo
        message = await client.get_messages(group_id, limit=1)
        msg_date = message[0].date
        msg_id = message[0].id
        msg = message[0].text
        print(msg)
        print()
        msg = remove_emojis(msg)
        msg = msg.split()

        if len(msg[1]) > 5:
            return None
        
        if len(msg) == 7:
            campeonato = msg[0]
            hora = msg[1].replace('[', '').replace(']', '')
        else:
            c = msg[0]
            campeonato = c[c.find('[')+1:c.find(']')]
            hora = msg[1].removeprefix('H:').strip()

        minutos = msg[2]
        minutos = [minutos[i:i+2] for i in range(0, len(minutos), 2)]

        return {'campeonato': campeonato, 'minutos': minutos, 'id': msg_id, 'hora': hora, 'msg_time': msg_date}
    
def pegar_sinais():
        # with open('data/ultimo_id.txt') as file:
        #     ult_id = int(file.read())

        while True:
            sinais = asyncio.run(main())
            if sinais == None:
                sleep(1)
                continue
            # if sinais['id'] > ult_id:
            #     ult_id = sinais['id']
            #     with open('data/ultimo_id.txt', 'w') as file:
            #         file.write(str(ult_id))

            return sinais

if __name__ == '__main__':
    sinais = pegar_sinais()
    time = sinais['msg_time']
