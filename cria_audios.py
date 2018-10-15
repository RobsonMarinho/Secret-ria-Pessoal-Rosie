#gTTS(Google Test to Speech) Escreve texto e converte para voz!
from gtts import gTTS   #Importando o gTTS
from playsound import playsound

def cria_audio(audio):
    tts = gTTS(audio, lang='pt-br') #adiciona a frase e o idioma a ser interpretado
    tts.save('audios/comando_invalido.mp3') #referencia e salva o arquivo áudio

playsound('audios/comando_invalido.mp3')   #Chamada no windows

cria_audio('Eu não sou paga para isso!')

