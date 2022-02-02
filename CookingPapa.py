from pynput import keyboard
cutting = 1
stove = -1
position = 0
in_cooking = 0
spins = 0
chops = 0
key_prev = keyboard.Key.up
def on_press(key):
    global position
    global stove
    global cutting
    global in_cooking
    global spins
    global key_prev
    global chops
    if in_cooking == 0:
        if key == keyboard.Key.left:
            position = stove
            return False
        elif key == keyboard.Key.right:
            position = cutting
            return False
        else:
            position = 0
        print('press left to go to stove, right to go to chopping board')
    elif position == stove:
        if key == keyboard.Key.up:
            key_prev = keyboard.Key.up
            return False
        elif key == keyboard.Key.right:
            if key_prev == keyboard.Key.up:
                key_prev = keyboard.Key.right
                return False
            else:
                print('wrong key')
        elif key == keyboard.Key.down:
            if key_prev == keyboard.Key.right:
                key_prev = keyboard.Key.down
                return False
            else:
                print('wrong key')
        elif key == keyboard.Key.left:
            if key_prev == keyboard.Key.down:
                key_prev = keyboard.Key.left
                spins = spins + 1
                return False
            else:
                print('wrong key')
                return False      
    elif position == cutting:
        if key == keyboard.Key.up:
            key_prev = keyboard.Key.up
            return False
        elif key == keyboard.Key.down:
            if key_prev == keyboard.Key.up:
                key_prev = keyboard.Key.down
                chops = chops + 1
                return False
            else:
                print('wrong key')
                return False
        else:
            print('wrong key')
            return False
    
while(True):
    print('press left to go to stove, right to go to chopping board')
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    in_cooking = 1
    if position == stove:
        txt = input('Type spoon to start stirring: ')
        if txt == 'spoon':
            print('press up right down left chef')
            while(spins<4):
                with keyboard.Listener(on_press=on_press)as listener:
                    listener.join()
            spins = 0
    elif position == cutting:
        txt = input('Type knife to start chopping: ')
        if txt == 'knife':
            print('press up and down chef')
            while(chops<6):
                with keyboard.Listener(on_press=on_press)as listener:
                    listener.join()
            chops = 0
    in_cooking = 0

