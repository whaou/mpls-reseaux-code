def on_button_pressed_a():
    global nb_tx
    radio.send_string("" + msg_header + "A" + "1")
    nb_tx += 1


input.on_button_pressed(Button.A, on_button_pressed_a)

msg_header = ""
radio.set_group(1)
num_carte = "01"
msg_header = "CARTE" + num_carte
nb_tx = 0
basic.show_string("MPLS client")


def on_forever():
    basic.show_number(nb_tx)


basic.forever(on_forever)
