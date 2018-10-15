# Teste IBM
import speech_recognition as sr   #módulo que possui suporte para bibliotecas de reconhecimento de voz offline e online.
import pyaudio

def monitora_microfone():   #Função que capta a voz via microfone

    microfone = sr.Recognizer()  # Obtém áudio do microfone
    with sr.Microphone() as source:
        print("Aguardando o comando!")
        audio = microfone.listen(source)

        # recognize speech using IBM Speech to Text
        IBM_USERNAME = "••••••••••••••••••••••••••••••••••••"  # IBM Speech to Text usernames are strings of the form XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
        IBM_PASSWORD = "••••••••••••"  # IBM Speech to Text passwords are mixed-case alphanumeric strings
        try:
            # Acessa o user, pass na conta da ibm para acessar o pacote speech_recognition
            print(microfone.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD, language='pt-BR'))
        except sr.UnknownValueError:
            print("IBM Speech to Text could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from IBM Speech to Text service; {0}".format(e))
        # Para teste, uso apenas a chave de API padrão
        # para usar outra chave de API, use `r.recognize_google(audio, key =" GOOGLE_SPEECH_RECOGNITION_API_KEY ")
        # instead of `r.recognize_google(audio)`
        try:
            print(microfone.recognize_google(audio, language='pt-BR'))  # reproduz o áudio na linguagem selecionada!
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")  # Exibe a frase se houver um erro
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service;"  # Exibe a frase se houver um erro
                  " {0}".format(e))

monitora_microfone()