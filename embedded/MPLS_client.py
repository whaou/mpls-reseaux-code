def on_button_pressed_a():
    global A_state, nb_tx
    if A_state == 1:
        A_state = 0
    else:
        A_state = 1
    radio.send_string("" + msg_header + "A" + ":" + convert_to_text(A_state))
    nb_tx += 1


input.on_button_pressed(Button.A, on_button_pressed_a)


def on_button_pressed_b():
    global B_state, nb_tx
    if B_state == 1:
        B_state = 0
    else:
        B_state = 1
    radio.send_string("" + msg_header + "B" + ":" + convert_to_text(B_state))
    nb_tx += 1


input.on_button_pressed(Button.B, on_button_pressed_b)

color = 0
nb_tx = 0
B_state = 0
A_state = 0
msg_header = ""
radio.set_group(1)
num_carte = "01"
msg_header = "C" + ":" + num_carte + ";"
A_state = 0
B_state = 0
basic.show_string("C n°" + num_carte)


def on_forever():
    basic.show_number(nb_tx)


basic.forever(on_forever)


def on_every_interval():
    global color
    radio.send_string(
        ""
        + msg_header
        + "R"
        + ":"
        + convert_to_text(color)
        + ","
        + convert_to_text(color)
        + ","
        + convert_to_text(color)
    )
    color += 1
    if color > 255:
        color = 0


loops.every_interval(100, on_every_interval)
