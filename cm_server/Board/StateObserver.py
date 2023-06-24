
import Board 
class StateObserver:
    def __init__(self, board_com):
        self.board_com = board_com
    def notify(self, state):
        # we want to lit up the leds on the board like before
        # create a led_state corresponding to the state
        # send the led_state to the board
        led_state = 0
        for i in range(0, 8):
            b = state >> i * 8 & 0xFF
            if i % 2 != 0:
                # reverse the bits
                b = int('{:08b}'.format(b)[::-1], 2)
            led_state |= b << i * 8

        command = Board.Commands.SET_LEDS_STATE_REQUEST
        command = command.to_bytes(1, "little")
        data_len = 8
        data_len = data_len.to_bytes(4, "little")
        data = led_state.to_bytes(8, "big")
        self.board_com.send(command + data_len + data)

                

                
        