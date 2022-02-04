from pynput import keyboard
import time as t 
import paho.mqtt.client as mqtt
#globals
cutting = 1
stove = -1
position = 0
in_cooking = 0
spins = 0
chops = 0
key_prev = keyboard.Key.up
ideal_spin = 1
ideal_cut = 1
start = t.time()
end = t.time()
diff = end - start
total_stove = 0
total_cutting = 0
GOAL_STOVE = 1
GOAL_CUTTING = 1
flag_player = 0
flag_opponent = 0
flag_received = 0
score = 0
#globals


#mqtt interaction
def on_connect(client, userdata, flags, rc):
    global flag_player
    global flag_opponent
    print("Connection returned result: "+str(rc))
    
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
# client.subscribe("ece180d/test")
# The callback of the client when it disconnects.
    player = input("which player are you playing as, 1 or 2?")
    if str(player) == '1':
        flag_player = 1
        flag_opponent = 2
    elif str(player) == '2':
        flag_player = 2
        flag_opponent = 1
    client.subscribe(str(player)+'Team8', qos=1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print('Unexpected Disconnect')
    else:
        print('Expected Disconnect')

def on_message(client, userdata, message):
    global flag_received
    global in_cooking
    global score
    flag_received = message.payload
    #case that you are done with the game when you receive the message
    if in_cooking == 2:
        client.publish(str(flag_opponent)+'Team8', float(score), qos=1)
        if 1000-float(score) > 1000-float(flag_received):
            print('You are better than the other idiot sandwich. Congration.')
            print('Your score: '+str(float(score))+'\n'+"Your opponent's score: " + str(float(flag_received)))
        else:
            print('You lost. Try a little harder next time would ya?')
            print('Your score: '+str(float(score))+'\n'+"Your opponent's score: " + str(float(flag_received)))
        client.loop_stop()
        client.disconnect()
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
    global ideal_spin
    global ideal_cut
    
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
                elif diff < ideal_spin * 1.2 and diff > ideal_spin * 0.8:
                    spins = spins + 1
                    print("Okay job! Great Spin!")
                elif diff < ideal_spin * 2 and diff > ideal_spin * 0.5:
                    spins = spins + 0.2
                    print("That was not a great spin, try to equalize your pace!")
                else:
                    print("You're an idiot sandwich. Try again.")
                print(spins)
                return False
            else:
                print('wrong key')
                return False

    #given cooking = 1, cutting      
    elif position == cutting:
        if key == keyboard.Key.up:
            key_prev = keyboard.Key.up
            start = t.time()
            return False
        elif key == keyboard.Key.down:
            if key_prev == keyboard.Key.up:
                key_prev = keyboard.Key.down
                end = t.time()
                diff = end-start
                #timing of cut
                if diff < ideal_cut * 1.1 and diff > ideal_cut * 0.9:
                    chops = chops + 1.5
                    print("Good job! Perfect Cut!")
                elif diff < ideal_cut * 1.2 and diff > ideal_cut * 0.8:
                    chops = chops + 1
                    print("Okay job! Great Cut!")
                elif diff < ideal_cut * 2 and diff > ideal_cut * 0.5:
                    chops = chops + 0.2
                    print("That was not a great cut, try to equalize your pace!")
                else:
                    print("You're an idiot sandwich. Try again.")
                print(chops)
                return False
            else:
                print('wrong key')
                return False
        else:
            print('wrong key')
            return False
#
#
#GAME STARTS HERE
#
#
client = mqtt.Client()
# add additional client options (security, certifications, etc.)
# many default options should be good to start off.
# add callbacks to client.
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
# 2. connect to a broker using one of the connect*() functions.
client.connect_async("test.mosquitto.org")
# 3. call one of the loop*() functions to maintain network traffic flow with the broker.
client.loop_start()

#wait for player selection
while(flag_player==0):
    pass
t.sleep(1)
start_game = t.time()    
while(in_cooking != 2):
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
            total_stove = total_stove + 1
            print("Total stove times remaining: "+ str(GOAL_STOVE-total_stove))
    elif position == cutting:
        txt = input('Type knife to start chopping: ')
        if txt == 'knife':
            print('press up and down chef')
            while(chops<6):
                with keyboard.Listener(on_press=on_press)as listener:
                    listener.join()
            chops = 0
            total_cutting = total_cutting + 1
            print("Total cutting times remaining: "+ str(GOAL_CUTTING-total_cutting))
    in_cooking = 0
    if total_cutting >= GOAL_CUTTING and total_stove >= GOAL_STOVE:
        in_cooking = 2
end_game = t.time()
score = end_game-start_game
print('Your time was: ' + str(score))
client.publish(str(flag_opponent)+'Team8', float(score), qos=1)
print("waiting for opponent's time...")
while True:
    pass