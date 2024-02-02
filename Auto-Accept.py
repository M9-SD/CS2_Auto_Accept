
import pyautogui
import time
from threading import Thread

button_ACCEPT = 'accept_button.jpg'
button_ACCEPT_H = 'accept_button_h.jpg'
buttons_menuBar = 'MenuBar_buttons.jpg'

def spawn(fnc=None, params=None, independent=None):
    if fnc is None:
        return None
    if params is None:
        params=()
    if independent is None:
        independent=False
    thrd = Thread(
        target=fnc,
        args=params,
    )
    thrd.daemon = not independent
    return [thrd, thrd.start()]

def inMainMenu():
    location_MENUBAR = None
    try:
        location_MENUBAR = pyautogui.locateCenterOnScreen(buttons_menuBar, confidence=0.77)
    except:
        pass
    return (True if location_MENUBAR else False)

def startAutoAccept():
    global autoAccept
    autoAccept = True
    print('Starting auto-accept loop...')
    while autoAccept:
        # waitUntil {inMainMenu}
        print('Auto-accept waiting for main menu...')
        while ((not inMainMenu()) and autoAccept):
            time.sleep(0.1)
        if not autoAccept:
            print('Auto accept loop start canceled.')
            break
        # while {inMainMenu}
        print('Auto-accept found main menu, starting button search loop...')
        while inMainMenu() and autoAccept:
            # Look for button
            location_ACCEPT = None
            try:
                location_ACCEPT = pyautogui.locateCenterOnScreen(button_ACCEPT, confidence=0.77)
            except:
                pass
            if location_ACCEPT is None:
                try:
                    location_ACCEPT = pyautogui.locateCenterOnScreen(button_ACCEPT_H, confidence=0.77)
                except:
                    pass
            if location_ACCEPT is None:
                pass
            else:
                print(f"Auto-accept FOUND BUTTON @ {location_ACCEPT}")
                # Press the button
                ogMPos = pyautogui.position()
                pyautogui.moveTo(location_ACCEPT)
                pyautogui.doubleClick()
                pyautogui.moveTo(*ogMPos)
                print(f"Auto-accept CLICKED BUTTON @ {location_ACCEPT}")
                """
                global shutdown
                shutdown = True
                """
                # ^ Shutdown disabled to allow it to keep accepting new matches if not enough players accept.
            del location_ACCEPT
            time.sleep(0.1)
        if autoAccept:
            print('Auto-accept button search stopped because not inMainMenu().')
        else:
            print('Auto-accept button search stopped because autoAccept=False.')
    print('Auto-accept loop stopped.')

shutdown = False
autoAccept = False

def main():
    spawn(startAutoAccept)
    while not shutdown:
        time.sleep(0.1)
    print('Shutting down...')

if __name__ == '__main__':
    main()
