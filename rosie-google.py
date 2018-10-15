from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
from requests import get    #Módulo que pega a URL
from bs4 import BeautifulSoup
import webbrowser as browser
from paho.mqtt import publish   #Apenas publica


## CONFIGURAÇÕES ##
hotword = 'rose'   #Cria a credencial gcloud

with open('rosie-python-assistente-ee492a4b2e61.json') as credenciais_google: #abre o arquivo com credenciais Json
    credenciais_google = credenciais_google.read()  #crediais recebe o método de leitura

#####LISTAGEM DOS COMANDOS  #####
'''
NOTÍCIAS                        Últimas notícias
TOCA <NOME DO ÁLBUM>            Reproduz o álbum no spotify player web
TEMPO AGORA                     Informações sobre temperatura e condição climática
TEMPERATURA HOJE                Informações sobre mínima e máxima
LIGA/DESLIGA BUNKER             Controle iluminação do escritório
'''


##### FUNÇÕES PRINCIPAIS #####

def monitora_audio():
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        while True:         ####PEGA O TEXTO GRAVADO E TRANSFORMA EM TEXTO
            print("Aguardando o Comando: ")
            audio = microfone.listen (source)#Ativa o microfone
            try:    #Acesso as credenciais google, add o idioma
                trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
                trigger = trigger.lower()   #letras minúsculas para facilitar a comparação

                ##TESTA TRIGGER ###
                if hotword in trigger:
                    print('COMANDO: ', trigger)
                    responde('feedback')
                    executa_comandos(trigger)
                    break

            except sr.UnknownValueError:
                print("Google not understand audio")    #Exibe o erro
            except sr.RequestError as e:
                print("Could not request results from Google Cloud Speech service; {0}".format(e))  #Exibe o erro

    return trigger

##CAPTA O ÁUDIO DE VOZ E REALIZA A AÇÃO DE PLAYLIST SELECIONADA POR VOZ##
## Usa áudio gravado, fazendo a chamada do play no arquivo
def responde(arquivo):  #Chama a função + nome do arquivo
    playsound(['audios/' + arquivo + '.mp3'])

def cria_audio(mensagem):
    tts = gTTS(audio, lang='pt-br') #adiciona a frase e o idioma a ser interpretado
    tts.save('audios/mensagem.mp3') #referencia e salva o arquivo áudio
    print('ROSIE:', mensagem)
    playsound('audios/mensagem.mp3')   #Chamada no windows

#Função principal##
def executa_comandos(trigger):
    if 'noticias' in trigger:
        ultimas_noticias()
        ## Toca o álbum atrvés da trigger mencionada
    elif 'toca' in trigger and 'acoustic_rock' in trigger:
        playlists('acoustic_rock')

    elif 'toca' in trigger and 'rock_songs' in trigger:
        playlists('rock_songs')

    elif 'tempo agora' in trigger:
        previsao_tempo(tempo=True)

    elif 'temperatura hoje' in trigger:
        previsao_tempo(minmax=True)
    #Liga
    elif 'liga o bunker' in trigger:
        publica_mqtt('offic/iluminacao/status', '1')
    #Desliga
    elif 'desativa o bunker' in trigger:
        publica_mqtt('offic/iluminacao/status', '0')

    else:
        mensagem = trigger.strip(hotword)   # apaga o hotword e atribue a mensagem o que foi dito
        cria_audio(mensagem)   #Repete o que foi falado
        print('C.INVÁLIDO', mensagem)   #Exibe na console
        responde('Comando_invalido')

###FUNÇÕES DE COMANDOS

def ultimas_noticias():
    #Request dar um get na URL e abaixo trata o conteúdo
    site = get('https://news.google.com/news/rss?ned=pt_br&gl=BR&hl=pt')
    noticias = BeautifulSoup(site.text, 'html.parser')
    #Captura a tag item e sua quantidade de notícias
    for item in noticias.findAll('item')[:3]:
        mensagem = item.title.text
        cria_audio(mensagem)    #criando áudio mensagem por mensagem

def playlists(album):   ###PEGA A MÚSICA ATRÁVES DO BROWSER
    if album == 'rock_songs':     #Escolhe o álbum
        browser.open('https://open.spotify.com/track/6gzVeJipkECzTkc3uyX55N')   #link da música
    elif album == 'acoustic_rock':
        browser.open('https://open.spotify.com/track/5j0AI4tzNT4Hu1sbizGgve')

###INFORMAÇÕES DE UMA API CLIMA WEATHER####
def previsao_tempo(tempo=False, minmax=False):
    #API weather informa o clima do estado de Pernambuco
    site = get('http://api.openweathermap.org/data/2.5/weather?id=3468157&APPID=1755265331c2804457b5ebbb82e62a51&units'
                '=metric&lang=pt')
    clima = site.json()
    #print(json.dumps(clima, indent=4))#Mostra de forma mais estruturada
    temperatura = clima['main']['temp']
    minima = clima['main']['temp_min']
    maxima = clima['main']['temp_max']
    descricao = clima['weather'][0]['description']
    if tempo:
        mensagem = f'No momento fazem {temperatura} graus com: {descricao}'
    if minmax:
        mensagem = f'Mínima de {minima} e máxima de {maxima}'
    cria_audio(mensagem)

    ####CONEXAO VIA CLOUDMQTT(SERVER) PARA CONEXAO COM UMA LÂMPADA(lig/des)####
    #MQTT IOT#
def publica_mqtt(topic, payload):
    publish.single(topic, payload=payload, qos=1, retain=True, hostname="m15.cloudmqtt.com",
                   port=13761, client_id="rosie", auth={'username': 'iuxlfopr', 'password':'k0Upsz1C5FKJ'})
    if payload =='1':
        mensagem = 'Bunker Ligado!'
    elif payload =='0':
        cria_audio(mensagem)


##organiza o código##
def main():
    while True:
        monitora_audio()

main()
