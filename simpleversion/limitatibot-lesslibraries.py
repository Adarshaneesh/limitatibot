# -*- coding: utf-8 -*-
#Programmato da Davide Leone in Python 3 - Per contatti: leonedavide[at]protonmail.com
#Distribuito sotto licenza GNU Affero GPL - Copyright 2018 Davide Leone
#Versione 1.1 Limitati Bot LessL 09/122/18 

""" Limitati Bot Less is a simple bot for telegram that allows limitate users to send you a message.
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
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

#-- CONFIG -- Assicurati di compilare tutti i campi prima di avviare il bot
token = '' #Token del bot ottenuto da t.me/botfather
amministratore = 0 #ID del proprietario del bot
antiflood_trigger = 6 #Numero massimo di messaggi mandabili nell'arco di 5 secondi
folder_position = '' #Posizione dei file all'interno del sistema; necessario per funzioni quali il crontab 
arcbanned = folder_position+'banned.save' #Nome del file che archivia gli utenti bannati
log_error = folder_position+'log.txt' #Nome del file in cui salvare il registro degli errori
repository = 'https://github.com/Davide-Leone/limitatibot' #Link al codice sorgente del programma.
#N.B.: Se si attuano modifiche, eccetto alle configurazioni, è necessario pubblicare un nuovo repository con il nuovo codice sorgente.

#Funzioni del bot
def filtro(msg): #Filtro contro flood ed utenti bannati
    global chat_id, banned
    if 'message' in list(msg.keys()): #Prende l'id dell'utente
        chat_id = msg['message']['chat']['id']
    else:
        chat_id = msg['chat']['id']
        
    try: #Scarica l'archivio degli utenti bannati
        file = open(arcbanned,'rb')
        banned = pickle.load(file)
        file.close()
    except:
        banned = []
        
    if msg['chat']['type'] == 'private': #Ignora canali e gruppi
        if chat_id not in antiflood: #Se l'utente non è nel registro antiflood, lo aggiungeee
            antiflood[chat_id] = 0
        if antiflood[chat_id] <= antiflood_trigger: #Filtro antiflood
            antiflood[chat_id] += 1 #Aggiorna il filtro antiflood
            if chat_id not in banned: #Utente non bannato
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
                        print('⚠ ERRORE '+str(e)) #Stampa l'errore a schermo
                        bot.sendMessage(amministratore,str(e)) #Invia l'errore all'amministratore del sistema.
                        file = open(log_error,'w')
                        file.write(str(e)+'\n') #Logging dell'errore su un file apposito
                        file.close()
            else: #Utente bannato
                bot.sendMessage(chat_id,"Mi spiace, ma è stato bannato dall'utilizzo di questo bot.")
                            
        elif antiflood[chat_id] == 6: #L'utente viene avvisato del filtro
            antiflood[chat_id] += 1 #Viene mandato un solo avviso
            bot.sendMessage(chat_id,"⚠ *FILTRO ANTIFLOOD*\nSta mandando *troppe richieste*. Attenda prima di mandarne di nuove.",'Markdown')
            
    
def gestisci(msg):
    
    if "message_id" in list(msg.keys()): #Raccoglie l'ID del messaggio
        mess_id = msg['message_id']
    else:
        mess_id = msg['message']['message_id']
        
    if "text" in list(msg.keys()): #Se il messaggio è testuale, ne raccoglie il testo
        command = msg['text'].lower()
    else:
        command = ''
        
    if 'reply_to_message' in list(msg.keys()): #Il messaggio è in risposta ad un altro messaggio, controlla di chi sia questo
        destinatario = msg['reply_to_message']['forward_from']['id']
    else:
        destinatario = 0

    if chat_id == amministratore: #Messaggio dall'amministratore del bot
        
        if command[:4] == "/ban": #Commando ban
            if destinatario != amministratore and destinatario != 0:
                banned.append(str(destinatario)) #Aggiunge l'utente alla lista dei bannati
                bot.sendMessage(chat_id,"Utente bannato correttamente.")
            elif destinatario == 0 and len(command) > 5:
                k = 5-len(command)
                banned.append(str(command[k:]))
                bot.sendMessage(chat_id,"Utente bannato correttamente.")
                    
        elif command[:6] == "/unban":
            if destinatario != 0 and destinatario != amministratore:
                if destinatario in banned:
                    banned.remove(destinatario)
                    bot.sendMessage(chat_id,"Utente sbannato correttamente.")
                else:
                    bot.sendMessage(chat_id,"L'utente non risulta essere stato bannato.")
            elif destinatario == 0 and len(command) > 7:
                k = 7-len(command)
                if command[k:]:
                    banned.remove(command[k:])
                    bot.sendMessage(chat_id,"Utente sbannato correttamente.")
                else:
                    bot.sendMessage(chat_id,"L'utente non risulta essere stato bannato.")
                
        elif destinatario != 0: #È in risposta ad un altro messaggio
                if 'caption' in list(msg.keys()):
                    did = msg['caption'] #Didascalia di foto, video, documenti.
                else:
                    did = None
                #Estrae il tipo di messaggio e agisce caso per caso
                chiavi = list(msg.keys())
                message = 'Messaggio inviato correttamente'
                if "text" in chiavi:
                    bot.sendMessage(destinatario,msg['text'])
                elif "sticker" in chiavi:
                    bot.sendSticker(destinatario,msg['sticker']['file_id'])
                elif "document" in chiavi:
                    bot.sendDocument(destinatario,msg['document']['file_id'],caption=did)
                elif "photo" in chiavi:
                    try:
                        bot.sendMediaGroup(destinatario,msg['media_group_id'])
                    except:
                        bot.sendPhoto(destinatario,msg['photo'][0]['file_id'],caption=did)
                elif "audio" in chiavi:
                    bot.sendAudio(destinatario,msg['audio']['file_id'],caption=did)
                elif "voice" in chiavi:
                    bot.sendVoice(destinatario,msg['voice']['file_id'])
                elif "video_note" in chiavi:
                    bot.sendVideoNote(destinatario,msg['video_note']['file_id'])
                elif "video" in chiavi:
                    bot.sendVideo(destinatario,msg['video']['file_id'],caption=did)
                elif "location" in chiavi:
                    bot.sendLocation(destinatario,msg['location']['latitude'],msg['location']['longitude'])
                elif "contact" in chiavi:
                    bot.sendContact(destinatario,msg['contact']['phone_number'],msg['contact']['first_name'])
                else:
                    message = "⚠️ IMPOSSIBILE RECAPITARE IL MESSAGGIO"
                bot.sendMessage(chat_id,message) #Viene confermato o meno che il messaggio è stato inviato

    else: #Messaggio da un utente
        if command == "/start": #Messaggio di benvenuto
            message = """Benvenuto nel mio bot limitati.\nManda un messaggio per iniziare la conversazione. Ti risponderò appena posso.\nPuoi usare /license per informazioni sulla licenza."""
            bot.sendMessage(chat_id,message)
        elif command == "/license": #Informazioni sulla licenza e su dove scaricare una copia del sorgente
            message = "Distribuito sotto licenza [Affero GPL](https://www.gnu.org/licenses/)."
            tastiera = InlineKeyboardMarkup(inline_keyboard=(
                [[InlineKeyboardButton(text='Source code',url=repository)]]))
            bot.sendMessage(chat_id,message,'Markdown',disable_web_page_preview=True,reply_markup=tastiera)
        try:
            bot.forwardMessage(amministratore,chat_id,msg['message_id']) #Inoltra il messaggio all'amministratore del bot
        except Exception as e:
            if str(e) == "'message_id'":
                None #È stata premuta una tastiera; non ha messaggi da inoltrare
                #Definire qui cosa succede quando viene premuta una tastiera, se si desidera aggiungerne
            else:
                raise #Errore sconosciuto. Viene gestito come previsto da filtro(msg)

    file = open(arcbanned,'wb') #Aggiorna la lista degli utenti bannati
    pickle.dump(banned,file) 
    file.close()

    
antiflood = {}
bot = telepot.Bot(token)
MessageLoop(bot,filtro).run_as_thread() #Riceve i messaggi
while 1:
    antiflood = {} #Resetta il filtro antiflood ogni 5 secondi
    time.sleep(5)
