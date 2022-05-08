#!/usr/bin/env python
import asyncio
import websockets
import json
import serial
import serial.tools.list_ports as list_ports
import time
import socket


MSG_JSON = {
    "NAME": "",
    "TEXT": "",
    "VAL": 0,
    "TEMP": 0,
    "A": "",
    "B": "",
    "AB": "",
    "P0": "",
    "P1": "",
    "P2": "",
    "RGB": "000000000",
    "PITCH": 0,
    "ROLL": 0,
    "ACCX": 0,
    "ACCY": 0,
    "ACCZ": 0,
    "DIST": 0,
    "MVT": "",
    "LASTCMD": "",
}
#
#  Déatils du flux JSON pour chaque cartes MB
#  {
#    "C": "01", /* chiffre 2 digits */
#    "NAME": "", /* libre = nom de la "carte" mb à afficher */
#    "TEXT": "", /* texte libre */
#    "VAL": "", /* nombre entier ou float */
#    "TEMP": "", /* nombre entier ou float */
#    "A": "",  /* 0/1 */
#    "B": "", /* 0/1 */
#    "AB": "", /* 0/1 */
#    "P0": "", /* nombre int float ? */
#    "P1": "",
#    "P2": "",
#    "RGB": "", /* 255255255  ou 000000000  concatenatuion de R de 0 à 255 puis G, puis B  */
#    "PITCH": "", /* nombre entier ou float orientation pirch */
#    "ROLL": "", /* nombre entier ou float orientation roll */
#    "ACCX": "", /* nombre entier ou float accéléromètre axe X */
#    "ACCY": "", /* nombre entier ou float accéléromètre axe Y */
#    "ACCZ": "", /* nombre entier ou float accéléromètre axe Z */
#    "DIST": "", /* nombre entier ou float mesure distance, US ou IR */
#    "MVT": "", /* 0/1 capteur PIR présence/mouvement */
#    "LASTCMD": ""  /* dernière commande reçue */
#  }
#  CXXTEMPYYYYYYYY
#  XX => numéro de la carte 01 à 24
#  YYYYYYYY => témpérature -10.0  25

NUM_MSG = {"NBMSG": 0}

TAB_MB = []
NB_CARTEMB = 24  # nombre de cartes gérée dans le programme

DATA_JSON = {}


# TAB_MB.append({"C": "00", **MSG_JSON})
#
# initialise le tableau de cartes avec un MSG au format JSON pour chacune qui est mis à jour lors de chaque réception de data sur via la carte MB serveur
#
for i in range(0, NB_CARTEMB + 1):
    if i < 10:
        y = "0" + str(i)
    else:
        y = str(i)
    TAB_MB.append({"C": y, **MSG_JSON})

#
# Fonction find_comport permet de trouver la carte MB connectée en USB
#
# Detection automatique de la carte MB connectée en USB
PID_MICROBIT = 516
VID_MICROBIT = 3368
TIMEOUT = 0.1


def find_comport(pid, vid, baud):
    """return a serial port"""
    ser_port = serial.Serial(timeout=TIMEOUT)
    ser_port.baudrate = baud
    ports = list(list_ports.comports())
    print("scanning ports")
    for p in ports:
        print("port: {}".format(p))
        try:
            print("pid: {} vid: {}".format(p.pid, p.vid))
        except AttributeError:
            continue
        if (p.pid == pid) and (p.vid == vid):
            print(
                "found target device pid: {} vid: {} port: {}".format(
                    p.pid, p.vid, p.device
                )
            )
            ser_port.port = str(p.device)
            return ser_port
    return None


#
# Fonction MSG_to_JSON prend en paramètre le message brut et le découpe
# pour le stocker dans le tableau TAB_MB à la position correspondant au
# numéro de la carte MB ainsi met a jour les datas de la carte pour
# chaque message et retourne le message JSON complet pour la carte une
# fois traité avec un status "STATE" OK ou ERROR si pas traité
# correctement
#
def MSG_to_JSON(message):
    # convertir le message en JSON
    # MSG_JSON = {"C": "","NAME": "","TEXT": "","VAL": 0,"TEMP": 0,"A": "","B": "","AB": "","P0": "","P1": "","P2": "","RGB": "0","PITCH": "","ROLL": "","ACCX": "","ACCY": "","ACCZ": "","DIST": "","MVT": "","LASTCMD": ""}

    message = message.strip("\n")
    message = message.strip("\r")
    message = message.strip(" ")
    if message[0:2] == "C:":
        # Reception d'un ou plusieurs messages d'une carte MB
        # print("MESSAGE MSG_to_JSON --", message, "--")

        NUM_MSG["NBMSG"] += 1

        if message.find("C:", 2) > 0:
            # ici 2 messages imbriqués au moins...
            pos = message[4:].find("C:")
            MSG_to_JSON(message[4 + pos :])
            message = str(message[: 4 + pos])

        try:
            # Récupération du n° de la carte
            msg = message.split(";")
            print("recherche n° carte: ", msg)
            try:
                m = msg.pop(0).split(":")
                num_carte = int(m[1])
                print("->", num_carte)
                if num_carte > NB_CARTEMB:
                    print("Error numero carte --", num_carte, "-- message :", message)
                TAB_MB[num_carte]["CARTE"] = f"{num_carte:02d}"
            except:
                return json.dumps({"STATE": "ERROR", **NUM_MSG})

            # Récupération de la commande
            next_cmd = msg.pop(0).split(":")
            print("Commande suivante: ", next_cmd)

            # Si le champ est de type string
            if next_cmd[0] in ["NAME", "TEXT", "A", "B", "AB", "P0", "P1", "P2", "MVT"]:
                print("Commande texte: " + next_cmd[0])
                try:
                    TAB_MB[num_carte][next_cmd[0]] = next_cmd[1]
                except:
                    return json.dumps({"STATE": "ERROR", **NUM_MSG})

            # Si le champ est de type float
            elif next_cmd[0] in [
                "VAL",
                "TEMP",
                "PITCH",
                "ROLL",
                "ACCX",
                "ACCY",
                "ACCZ",
            ]:
                try:
                    TAB_MB[num_carte][next_cmd[0]] = float(next_cmd[1])
                except:
                    return json.dumps({"STATE": "ERROR", **NUM_MSG})

            # Si le champ est de type RGB
            elif next_cmd[0] == "R":
                try:
                    print("Commande RGB: ", next_cmd[1])
                    [r, g, b] = next_cmd[1].split(",")
                    [red, green, blue] = [int(r), int(g), int(b)]
                    print("-> ", f"{red:03d}" + f"{green:03d}" + f"{blue:03d}")
                    TAB_MB[num_carte]["RGB"] = (
                        f"{red:03d}" + f"{green:03d}" + f"{blue:03d}"
                    )
                    print("3")
                except:
                    return json.dumps({"STATE": "ERROR", **NUM_MSG})

            TAB_MB[num_carte]["LASTCMD"] = message

            return json.dumps({"STATE": "OK", **TAB_MB[num_carte], **NUM_MSG})
        except ValueError:
            return json.dumps({"STATE": "ERROR", **NUM_MSG})
    else:
        return json.dumps({"STATE": "ERROR"})


#
# fonction principale qui récupère les data "série/USB" et convertit en JSON en retour
#
async def producer():
    try:
        message = mb_serie.readline().decode("utf-8")
        DATA_JSON = ""
        if message:
            print("Message RECU de la MB serveur: --", message, "--")
            if message[0:2] != "C:":
                print("Erreur message : --", message, "--")
                return DATA_JSON
            # Reception d'un message d'une carte MB
            # print("CARTE ",  message[5:7], " message :", message[7:])

            # Traitement du message et conversion en JSON
            DATA_JSON = MSG_to_JSON(str(message))
            print(DATA_JSON)

            print(NUM_MSG["NBMSG"], " messages reçus et envoyé ...")

            # Accuse de reception, retourne a la MB serveur un ACK + numéro carte du message
            accuse = "ACK" + message[2:4]
            mb_serie.write(accuse.encode("utf-8"))
            # print(accuse)
        return DATA_JSON
    except ValueError:
        print("Erreur de recpetion message")
    except KeyboardInterrupt:
        print("Fin du PGM ...")
        quit()


#
# Fonction handler appelée a chaque connexion au WS gère les multiples cnx et double sens ...
#
# WS_connected est la liste des clients du WS qui sont connectés
WS_connected = set()


async def consumer(message):
    # print("< {}".format(message))
    # exemples :
    # < {"CARTE":"01","COMMAND":"btnA"}
    # < {"CARTE":"01","COMMAND":"40"}
    # < {"CARTE":"01","COMMAND":"btnB"}
    # Envoyer aux carte MB C:XX;CMD:YYYYYYY  => XX numéro de carte   YYYYY valeur de la commande envoyée btnA, btnB = appuye bouton A, B ou une "valeur"
    # TODO ici on peut envoyer un message depuis une page WS via le WS et piloter une carte MB
    json_send_msg = json.loads(message)
    send_msg = "C:" + json_send_msg["CARTE"] + ";CMD:" + json_send_msg["COMMAND"]
    mb_serie.write(send_msg.encode("utf-8"))
    print("Message envoye a la MB serveur = ", send_msg)


async def producer_handler(websocket, path):
    global DATA_JSON
    # if DATA_JSON:
    #    await websocket.send(DATA_JSON)
    pass


async def handler(websocket, path):
    global DATA_JSON
    WS_connected.add(websocket)
    print("WS connected ...", websocket)
    try:
        while True:
            listener_task = asyncio.ensure_future(websocket.recv())
            # producer_task = asyncio.ensure_future(producer())
            producer_task = asyncio.ensure_future(producer_handler(websocket, path))
            done, pending = await asyncio.wait(
                [listener_task, producer_task], return_when=asyncio.FIRST_COMPLETED
            )

            if listener_task in done:
                message = listener_task.result()
                await consumer(message)
            else:
                listener_task.cancel()

            DATA_JSON = await producer()

            if producer_task in done:
                if DATA_JSON:
                    # envoi le msg JSON a tous les WS connectés
                    for ws in WS_connected:
                        await ws.send(DATA_JSON)
            else:
                producer_task.cancel()
    finally:
        WS_connected.remove(websocket)
        print("WS remove ...", websocket)


#
# Programme principal
#
# Boucle d'attente MB
print("Detection microbit")
mb_serie = find_comport(PID_MICROBIT, VID_MICROBIT, 115200)
if not mb_serie:
    print("microbit absente")
    time.sleep(1000)
else:
    print("ouverture de la communication avec MB serveur")
    print("-----======== * ========-----")
    mb_serie.open()

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])

    # start_server = websockets.serve(handler, '192.168.1.59', 8000)
    start_server = websockets.serve(handler, s.getsockname()[0], 8000)

    asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        print("server crashed")
