import keyboard
import pyautogui as pg
import time

print('Press (right) for ctrl + pageup or (left) for ctrl + pagedown')

while True:
    # print('Waiting for key press...')
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_DOWN:
        if event.name == 'left':
            keyboard.press_and_release('ctrl+pageup')
            print('Pressed ctrl + pageup')
        elif event.name == 'right':
            keyboard.press_and_release('ctrl+pagedown')
            print('Pressed ctrl + pagedown')
    
    time.sleep(0.5)