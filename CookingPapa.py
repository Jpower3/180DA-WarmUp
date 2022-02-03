from pynput import keyboard
import time as t 
cutting = 1
stove = -1
position = 0
in_cooking = 0
spins = 0
chops = 0
key_prev = keyboard.Key.up
ideal_spin = 1
ideal_cut = 0.5
start = t.time()
end = t.time()
diff = end - start
def on_press(key):
    #global variables declared
    global position
    global stove
    global cutting
    global in_cooking
    global spins
    global key_prev
    global chops
    global start
    global end
    global diff
    
    #choose which board
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
 
    #given cooking = 1, stove
    elif position == stove:
        if key == keyboard.Key.up:
            key_prev = keyboard.Key.up
            start = t.time()
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
                end = t.time()
                diff = end-start
                #timing of spins
                if diff < ideal_spin * 1.1 and diff > ideal_spin * 0.9:
                    spins = spins + 1.5
                    print("Good job! Perfect Spin!")
                elif diff < ideal_spin *1.2 and diff > ideal_spin * 0.8:
                    spins = spins + 1
                    print("Okay job! Great Spin!")
                elif diff < ideal_spin * 2 and diff > ideal_spin *0.5:
                    spins = spins - 0.5
                    print("That was not a great spin, try to equalize your pace!")
                print(spins)
                return False
            else:
                print('wrong key')
                return False

    #given cooking = 1, cutting      
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

