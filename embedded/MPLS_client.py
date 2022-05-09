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

nb_tx = 0
B_state = 0
A_state = 0
msg_header = ""
radio.set_group(1)
num_carte = "92"
msg_header = "C" + ":" + num_carte + ";"
A_state = 0
B_state = 0
color_R = 0
color_V = 0
color_B = 0
basic.show_string("C n°" + num_carte)


def on_every_interval():
    radio.send_string(
        ""
        + msg_header
        + "PITCH"
        + ":"
        + convert_to_text(input.rotation(Rotation.PITCH))
    )
    radio.send_string(
        "" + msg_header + "ROLL" + ":" + convert_to_text(input.rotation(Rotation.ROLL))
    )


loops.every_interval(1000, on_every_interval)


def on_every_interval2():
    radio.send_string(
        "" + msg_header + "TEMP" + ":" + convert_to_text(input.temperature())
    )


loops.every_interval(10000, on_every_interval2)


def on_forever():
    basic.show_number(nb_tx)


basic.forever(on_forever)


def on_every_interval3():
    global color_R, color_V, color_B
    radio.send_string(
        ""
        + msg_header
        + "R"
        + ":"
        + convert_to_text(color_R)
        + ","
        + convert_to_text(color_V)
        + ","
        + convert_to_text(color_B)
    )
    color_R += 1
    color_V += 2
    color_B += 3
    if color_R > 255:
        color_R = 0
    if color_V > 255:
        color_V = 0
    if color_B > 255:
        color_B = 0


loops.every_interval(100, on_every_interval3)
