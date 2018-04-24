# -*- coding: utf-8 -*-
#Programmato da Davide Leone in Python 3 - Per contatti: leonedavide[at]protonmail.com
#Distribuito sotto licenza GNU Affero GPL - Copyright 2018 Davide Leone
#Versione 1.0 Limitati Bot LessL 24/04/18 

""" Limitati Bot LessL is a simple bot for telegram that allows limitate users to send you a message.
    Copyright (C) 2018  Davide Leone

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>."""

#Import delle librerie
import telepot
from telepot.loop import MessageLoop
import time
import pickle

#-- CONFIG -- Assicurati di compilare tutti i campi prima di avviare il bot
token = '' #Token del bot ottenuto da t.me/botfather
amministratore = 0 #ID del proprietario del bot
antiflood_trigger = 6 #Numero massimo di messaggi mandabili nell'arco di 5 secondi
folder_position = '' #Posizione dei file all'interno del sistema; necessario per funzioni quali il crontab 
arcbanned = folder_position+'' #Nome del file che archivia gli utenti bannati
error_logging = folder_position+'' #Nome del file in cui salvare il registro degli errori
repository = 'https://github.com/Davide-Leone/limitatibot' #Link al codice sorgente del programma.
#N.B.: Se si attuano modifiche, eccetto alle configurazioni, è necessario pubblicare un nuovo repository con il nuovo codice sorgente.

#Funzioni del bot
def filtro(msg): #Filtro contro flood ed utenti bannati
    global chat_id
    try: #Prende l'id dell'utente
        chat_id = msg['chat']['id']
    except:
        chat_id = msg['message']['chat']['id']
    try: #Scarica l'archivio degli utenti bannati
        file = open(arcbanned,'rb')
        banned = pickle.load(file)
        arcbanned.close()
    except:
        banned = []
    if chat_id not in banned and msg['chat']['type'] == 'private': #Controlla l'utente non sia stato bannato, filtro ulteriore per ignorare canali e gruppi
        try: 
            antiflood[chat_id] #Tenta di recuperare il valore antiflood. Se non è stato assegnato genera un errore
        except KeyError: #Valore non ancora assegnato; lo assegna
            antiflood[chat_id] = 0
        if antiflood[chat_id] <= antiflood_trigger: #Filtro antiflood
            antiflood[chat_id] += 1 #Aggiorna il filtro antiflood
            try:
                gestisci(msg) #Avvia il bot
            except telepot.exception.TooManyRequestsError: #Errore noto: filtr antiflood di Telegram
                bot.sendMessage(chat_id,"⚠ *ERRORE TELEGRAM 400:* avete mandato troppe richieste",'Markdown')
                antiflood[chat_id] = 7
            except Exception as e: #Gestione degli errori
                if str(e) == str(('Bad Request: message is not modified', 400, {'ok': False, 'error_code': 400, 'description': 'Bad Request: message is not modified'})):
                    None #Errore noto. Invia due richieste per modificare allo stesso modo uno stesso messaggio
                elif str(e) == str(('Forbidden: bot was blocked by the user', 403, {'ok': False, 'error_code': 403, 'description': 'Forbidden: bot was blocked by the user'})):
                    None #Errore noto. Il bot non riesce a contattare un utente da cui è stato bloccato
                else: #Errore non noto.
                    print('⚠ ERRORE'+str(e)) #Stampa l'errore a schermo
                    bot.sendMessage(amministratore,str(e)) #Invia l'errore all'amministratore del sistema. Eliminare le virgolette per attivarla
                    scrivi(error_logging,(str(e)+'\n')) #Logging dell'errore su un file apposito
                    
        elif antiflood[chat_id] == 6: #L'utente viene avvisato del filtro
            antiflood[chat_id] += 1 #Viene mandato un solo avviso
            bot.sendMessage(chat_id,"⚠ *FILTRO ANTIFLOOD*\nSta mandando *troppe richieste*. Attenda prima di mandarne di nuove.",'Markdown')

    
def gestisci(msg):
    try: #Recupera le info base
        mess_id = msg['message_id']
    except:
        mess_id = msg['message']['message_id']
    try: 
        command = msg['text'].lower()
    except:
        command = ''
    try: #Il messaggio è in risposta ad un altro messaggio
        destinatario = msg['reply_to_message']['forward_from']['id']
    except:
        destinatario = 0

    if chat_id == amministratore:
        if command == "/ban": #Commando ban
            if destinatario != 0 and destinatario != amministratore:
                banned.apppend(destinatario) #Aggiunge l'utente alla lista dei bannati
        elif command == "/unban":
            if destinatario != 0 and destinatario != amministratore:
                banned.remove(destinatario)
        elif destinatario != 0: #È in risposta ad un altro messaggio
                try:
                    did = msg['caption'] #Didascalia di foto, video, documenti.
                except:
                    did = None
                #Estrae il tipo di messaggio e agisce caso per caso
                tipo = list(msg.keys())[-1] 
                message = 'Messaggio inviato correttamente'
                if tipo == 'text':
                    bot.sendMessage(destinatario,msg['text'])
                elif tipo == "sticker":
                    bot.sendSticker(destinatario,msg['sticker']['file_id'])
                elif tipo == "document":
                    bot.sendDocument(destinatario,msg['document']['file_id'],caption=did)
                elif tipo == "photo":
                    try:
                        bot.sendMediaGroup(destinatario,msg['media_group_id'])
                    except:
                        bot.sendPhoto(destinatario,msg['photo'][0]['file_id'],caption=did)
                elif tipo == "audio":
                    bot.sendAudio(destinatario,msg['audio']['file_id'],caption=did)
                elif tipo == "voice":
                    bot.sendVoice(destinatario,msg['voice']['file_id'])
                elif tipo == "video_note":
                    bot.sendVideoNote(destinatario,msg['video_note']['file_id'])
                elif tipo == "video":
                    bot.sendVideo(destinatario,msg['video']['file_id'],caption=did)
                elif tipo == "location":
                    bot.sendLocation(destinatario,msg['location']['latitude'],msg['location']['longitude'])
                elif tipo == "contact":
                    bot.sendContact(destinatario,msg['contact']['phone_number'],msg['contact']['first_name'])
                else:
                    message = "⚠️ IMPOSSIBILE RECAPITARE IL MESSAGGIO"
                bot.sendMessage(chat_id,message) #Viene confermato o meno che il messaggio è stato inviato

    else:
        if command == "/start": #Messaggio di benvenuto
            welcome = """Benvenuto nel bot limitati.
Manda un messaggio per iniziare la conversazione.
Puoi usare /license per informazioni sulla licenza"""
            bot.sendMessage(chat_id,welcome)
        elif command == "/license": #Informazioni sulla licenza e su dove scaricare una copia del sorgente
            message = "Distribuito sotto licenza [Affero GPL](https://www.gnu.org/licenses/). Puoi scaricare il file sorgente del bot a: "+repository
            bot.sendMessage(chat_id,message,'Markdown')
        try:
            bot.forwardMessage(amministratore,chat_id,msg['message_id']) #Inoltra il messaggio all'amministratore del bot
        except Exception as e:
            if str(e) == "'message_id'":
                None #È stata premuta una tastiera; non ha messaggi da inoltrare
                #Definire qui cosa succede quando viene premuta una tastiera, se si desidera aggiungerne
            else:
                raise #Errore sconosciuto. Viene gestito come previsto da filtro(msg)

    file = open(arcbanned,'rb') #Aggiorna la lista degli utenti bannati
    pickle.dump(banned,arcbanned) 
    file.close()
    
MessageLoop(telepot.Bot(token),filtro).run_as_thread() #Riceve i messaggi
while 1:
    antiflood = {} #Resetta il filtro antiflood ogni 5 secondi
    time.sleep(5)
