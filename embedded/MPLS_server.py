def on_received_string(receivedString):
    global nb_rx
    nb_rx += 1
    serial.write_line(receivedString)


radio.on_received_string(on_received_string)

radio.set_group(1)
serial.redirect_to_usb()
nb_rx = 0
basic.show_string("MPLS Serveur")


def on_forever():
    basic.show_number(nb_rx)


basic.forever(on_forever)
