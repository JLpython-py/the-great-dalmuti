#! python3
# client.py

import string
import time
import pickle
import pyperclip
import random
import socket
import sys

import pygame

SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LOCAL_HOSTNAME = socket.gethostname()
LOCAL_FQDN = socket.getfqdn()
IP_ADDRESS = socket.gethostbyname(LOCAL_HOSTNAME)
PORT = 2020
SERVER = (IP_ADDRESS, PORT)

pygame.init()

SCALE = 35
WIDTH = 32 * SCALE
HEIGHT = 20 * SCALE

pygame.display.set_caption('The Great Dalmuti')
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

BACKGROUND = pygame.image.load('.\docs\background.png').convert()
LOGO = pygame.image.load('.\docs\logo.png').convert_alpha()

class GameData:
    ''' Basic game data for "The Great Dalmuti"
'''
    def __init__(self):
        self.card_images = (
            '1_1.jpg',
            '2_1.jpg', '2_2.jpg',
            '3_1.jpg', '3_2.jpg', '3_3.jpg',
            '4_1.jpg', '4_2.jpg', '4_3.jpg', '4_4.jpg',
            '5_1.jpg', '5_2.jpg', '5_3.jpg', '5_4.jpg', '5_5.jpg',
            '6_1.jpg', '6_2.jpg', '6_3.jpg', '6_4.jpg', '6_5.jpg',
            '6_6.jpg',
            '7_1.jpg', '7_2.jpg', '7_3.jpg', '7_4.jpg', '7_5.jpg',
            '7_6.jpg', '7_7.jpg',
            '8_1.jpg', '8_2.jpg', '8_3.jpg', '8_4.jpg', '8_5.jpg',
            '8_6.jpg', '8_7.jpg', '8_8.jpg',
            '9_1.jpg', '9_2.jpg', '9_3.jpg', '9_4.jpg', '9_5.jpg',
            '9_6.jpg', '9_7.jpg', '9_8.jpg', '9_9.jpg',
            '10_1.jpg', '10_2.jpg', '10_3.jpg', '10_4.jpg', '10_5.jpg',
            '10_6.jpg', '10_7.jpg', '10_8.jpg', '10_9.jpg', '10_10.jpg',
            '11_1.jpg', '11_2.jpg', '11_3.jpg', '11_4.jpg', '11_5.jpg',
            '11_6.jpg', '11_7.jpg', '11_8.jpg', '11_9.jpg', '11_10.jpg',
            '11_11.jpg',
            '12_1.jpg', '12_2.jpg', '12_3.jpg', '12_4.jpg', '12_5.jpg',
            '12_6.jpg', '12_7.jpg', '12_8.jpg', '12_9.jpg', '12_10.jpg',
            '12_11.jpg', '12_12.jpg',
            'J_1.jpg', 'J_2.jpg')
        self.card_rear = 'x_x.jpg'
        self.settings = {
            4: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Lesser Peon', 'Greater Peon'),
            5: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A',
                   'Lesser Peon', 'Greater Peon'),
            6: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A', 'Merchant B',
                   'Lesser Peon', 'Greater Peon'),
            7: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A', 'Merchant B', 'Merchant C',
                   'Lesser Peon', 'Greater Peon'),
            8: ('Great Dalmuti', 'Lesser Dalmuti',
                   'Merchant A', 'Merchant B', 'Merchant C', 'Merchant D',
                   'Lesser Peon', 'Greater Peon')}
        self.ranks = {
            'Jester': (
                'J_1.jpg', 'J_2.jpg'),
            'Great Dalmuti': (
                '1_1.jpg',),
            'Archbishop': (
                '2_1.jpg', '2_2.jpg'),
            'Earl Marshal': (
                '3_1.jpg', '3_2.jpg', '3_3.jpg'),
            'Baroness': (
                '4_1.jpg', '4_2.jpg', '4_3.jpg', '4_4.jpg'),
            'Abbess': (
                '5_1.jpg', '5_2.jpg', '5_3.jpg', '5_4.jpg', '5_5.jpg'),
            'Knight': (
                '6_1.jpg', '6_2.jpg', '6_3.jpg', '6_4.jpg', '6_5.jpg',
                '6_6.jpg'),
            'Seamstress': (
                '7_1.jpg', '7_2.jpg', '7_3.jpg', '7_4.jpg', '7_5.jpg',
                '7_6.jpg', '7_7.jpg'),
            'Mason': (
                '8_1.jpg', '8_2.jpg', '8_3.jpg', '8_4.jpg', '8_5.jpg',
                '8_6.jpg', '8_7.jpg', '8_8.jpg'),
            'Cook': (
                '8_1.jpg', '8_2.jpg', '8_3.jpg', '8_4.jpg', '8_5.jpg',
                '8_6.jpg', '8_7.jpg', '8_8.jpg'),
            'Shepherdress': (
                '10_1.jpg', '10_2.jpg', '10_3.jpg', '10_4.jpg', '10_5.jpg',
                '10_6.jpg', '10_7.jpg', '10_8.jpg', '10_9.jpg', '10_10.jpg'),
            'Stonecutter': (
                '11_1.jpg', '11_2.jpg', '11_3.jpg', '11_4.jpg', '11_5.jpg',
                '11_6.jpg', '11_7.jpg', '11_8.jpg', '11_9.jpg', '11_10.jpg',
                '11_11.jpg'),
            'Peasant': (
                '12_1.jpg', '12_2.jpg', '12_3.jpg', '12_4.jpg', '12_5.jpg',
                '12_6.jpg', '12_7.jpg', '12_8.jpg', '12_9.jpg', '12_10.jpg',
                '12_11.jpg', '12_12.jpg')}

class Game:
    ''' Data sets to track game data as each game progresses
'''
    history = []

class Player:
    ''' Data sets to track player data as each game progresses
'''
    name = ''
    code = ''
    
    rank = ''
    cards = []

class Fonts:
    ''' Font data
'''
    name = 'freesansbold.ttf'
    small = pygame.font.Font(name, int(SCALE*0.5))
    main = pygame.font.Font(name, SCALE)
    large = pygame.font.Font(name, SCALE*3)

class HomeScreen:
    ''' Screen 1: Home Screen
        *Request name
        *Request game code or start new game
        *Connect to server
'''
    def __init__(self):
        self.background = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
        self.logo = pygame.transform.scale(LOGO, (16*SCALE, 10*SCALE))
        self.name = HomeScreen.Name()
        self.code = HomeScreen.Code()
        self.newgame = HomeScreen.NewGame()
        self.joingame = HomeScreen.JoinGame()

        #Active Attributes
        self.active = {
            'Name': False,
            'Code': False,
            'Screen': True}

        while self.active['Screen']:
            self.update_screen()

            #Check Current Events
            for event in pygame.event.get():
                check_for_quit(event)

                #Mouse Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Collides with Input Name Box
                    if self.name.box.collidepoint(event.pos):
                        self.active['Name'] = True
                        self.name.text_color = self.name.active
                    else:
                        self.active['Name'] = False
                        self.name.text_color = self.name.inactive

                    #Collides with Game Code Box
                    if self.code.box.collidepoint(event.pos):
                        self.active['Code'] = True
                        self.code.text_color = self.code.active
                    else:
                        self.active['Code'] = False
                        self.code.text_color = self.code.inactive

                    #Collides with Join Box
                    if self.joingame.button.collidepoint(event.pos):
                        if len(self.code.text) != 10:
                            Invalid('Code')
                            self.code.text = self.code.default_text
                            continue
                        if not all(
                            [char in list(
                                string.printable
                                ) for char in self.code.text]):
                            Invalid('Code')
                            self.code.text = self.code.default_text
                            continue

                        if not self.name.text:
                            Invalid('Name')
                            self.name.text = self.name.default_text
                            continue
                        if not all(
                            [char in list(
                                string.printable
                                ) for char in self.name.text]):
                            Invalid('Name')
                            self.name.text = self.name.default_text
                            continue

                        Player.name = self.name.text
                        SOCK.connect(SERVER)
                        print('Connecting to Server')
                        SOCK.send(Player.name.encode('utf-8'))
                        print('Sending Name')
                        self.active['Screen'] = False

                    #Collides with New Game Box
                    if self.newgame.button.collidepoint(event.pos):
                        if not self.name.text:
                            Invalid('Name')
                            self.name.text = self.name.default_text
                            continue
                        if not all(
                            [char in list(
                                string.printable
                                ) for char in self.name.text]):
                            Invalid('Name')
                            self.name.text = self.name.default_text
                            continue
                        Player.name = self.name.text
                        Player.code = ''.join(random.sample(
                            string.ascii_letters, 10))
                        SOCK.connect(SERVER)
                        print('Connecting to Server')
                        SOCK.send(Player.name.encode('utf-8'))
                        print('Sending Name')
                        self.active['Screen'] = False

                #Keyboard Typing is Active
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.active['Name'] = False
                        self.active['Code'] = False
                        self.name.text_color = self.name.inactive
                        self.code.text_color = self.code.inactive

                    #Input for Name is Active
                    if self.active['Name']:
                        if self.name.text == self.name.default_text:
                            self.name.text = ''
                        if event.key == pygame.K_BACKSPACE:
                            self.name.text = self.name.text[:-1]
                        elif event.key == pygame.K_DELETE:
                            self.name.text = ''
                        else:
                            self.name.text += event.unicode

                    #Input for Code is Active
                    if self.active['Code']:
                        if self.code.text == self.code.default_text:
                            self.code.text = ''
                        if event.key == pygame.K_BACKSPACE:
                            self.code.text = self.code.text[:-1]
                        elif event.key == pygame.K_DELETE:
                            self.code.text = ''
                        else:
                            self.code.text += event.unicode

    def update_screen(self):
        ''' *Add 'Background' image to Surface
            *Add 'Logo' image to Surface
            *Add framerate to Surface
            *Call all class update functions
            *Update display
            *Pass time between frames
'''
        SURFACE.blit(self.background, (0, 0))
        SURFACE.blit(self.logo, (8*SCALE, SCALE))
        display_fps()

        self.name.update(self.active['Name'])
        self.code.update(self.active['Code'])
        self.newgame.update()
        self.joingame.update()

        pygame.display.update()
        CLOCK.tick(30)

    class Name:
        ''' Input box to enter name
'''
        def __init__(self):
            ''' Set Name default attributes
'''
            self.default_text = 'Enter name...'
            self.active = pygame.Color('dodgerblue4')
            self.inactive = pygame.Color('white')

            self.box = pygame.Rect(SCALE*4, SCALE*12, SCALE*24, SCALE*2)
            self.width = 4
            self.text = self.default_text
            self.text_color = self.inactive
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self, active):
            ''' Update Name 'text' to match input text
                Update Name 'text_surf'
                Add Name 'box' and Name 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.text_color, self.box, self.width)

            if not self.text and not active:
                self.text = self.default_text
            self.surf = Fonts.main.render(self.text, True, self.text_color)
            if self.surf.get_width()>self.box.width:
                self.text = self.text[:-1]
            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.box.width,
                self.box.height)
            SURFACE.blit(self.surf, (self.box.x+10, self.box.y+mars[1]))

    class Code:
        ''' Input box to enter game code
'''
        def __init__(self):
            ''' Set Game Code default attributes
'''
            self.default_text = "Ent'r thy game code..."
            self.active = pygame.Color('dodgerblue4')
            self.inactive = pygame.Color('white')

            self.box = pygame.Rect(SCALE*11, SCALE*15, SCALE*12, SCALE*2)
            self.width = 4
            self.text = self.default_text
            self.text_color = self.inactive
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self, active):
            ''' Update Game Code 'text' to match input text
                Update Game Code 'text_surf'
                Add Game Code 'box' and Game Code 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.text_color, self.box, self.width)

            if not self.text and not active:
                self.text = self.default_text
            self.surf = Fonts.main.render(self.text, True, self.text_color)
            if (self.text != self.default_text
                and len(self.text) > 10)\
               or (self.surf.get_width() > self.box.width):
                self.text = self.text[:-1]
            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.box.width,
                self.box.height)
            SURFACE.blit(self.surf, (self.box.x+10, self.box.y+mars[1]))

    class NewGame:
        ''' Button to start new game
'''
        def __init__(self):
            ''' Set New Game attributes
'''
            self.button = pygame.Rect(SCALE*4, SCALE*15, SCALE*6, SCALE*2)
            self.width = 4
            self.text = 'New Game'
            self.color = pygame.Color('mediumseagreen')
            self.border = pygame.Color('dimgray')
            self.text_color = pygame.Color('white')
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self):
            ''' Add New Game 'button' and New Game 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.button)
            pygame.draw.rect(SURFACE, self.border, self.button, self.width)

            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.button.width,
                self.button.height)
            SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

    class JoinGame:
        ''' Button to join existing game
'''
        def __init__(self):
            ''' Set Join Game attributes
'''
            self.button = pygame.Rect(SCALE*24, SCALE*15, SCALE*4, SCALE*2)
            self.width = 4
            self.text = 'Joineth'
            self.color = pygame.Color('navy')
            self.border = pygame.Color('dimgray')
            self.text_color = pygame.Color('white')
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self):
            ''' Add Join Game 'button' and Join Game 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.button)
            pygame.draw.rect(SURFACE, self.border, self.button, self.width)

            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.button.width,
                self.button.height)
            SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

class Invalid:
    ''' Notice for invalid Name 'text' or Game Code 'text'
'''
    def __init__(self, reason):
        self.fill = pygame.Color('dimgray')
        self.width = 4
        self.box = Invalid.Box(reason)
        self.button = Invalid.Button()

        #Active Attributes
        active = True

        while active:
            self.update_screen()
            #Check Current Events
            for event in pygame.event.get():
                check_for_quit(event)
                #Mouse Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Collides with Clickout Button
                    if self.button.button.collidepoint(event.pos):
                        active = False

    def update_screen(self):
        ''' *Fill area where the Invalid box will be
            *Call box 'update' function
            *Fill box
            *Call button 'update' function
            *Display framerate
            *Update display
            *Pass time between frames
'''
        SURFACE.fill(self.fill, self.box.box)
        self.box.update()

        SURFACE.fill(self.fill, self.button.button)
        self.button.update()
        display_fps()

        pygame.display.update()
        CLOCK.tick(30)

    class Box:
        ''' Invalid notice box
'''
        def __init__(self, reason):
            ''' Set Invalid box attributes
'''
            self.box = pygame.Rect(SCALE*10, SCALE*8, SCALE*12, SCALE*4)
            self.width = 4
            self.text = 'Invalid {}'.format(reason)
            self.color = pygame.Color('red2')
            self.surf = Fonts.main.render(self.text, True, self.color)

        def update(self):
            ''' Add box 'box' and box 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.box, self.width)

            self.surf = Fonts.main.render(self.text, True, self.color)
            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.box.width,
                self.box.height)
            SURFACE.blit(self.surf, (self.box.x+mars[0], self.box.y+int(SCALE*0.5)))        

    class Button:
        ''' Invalid button to click out of notice
'''
        def __init__(self):
            ''' Set Invalid button attributes
'''
            self.button = pygame.Rect(SCALE*12, SCALE*10, SCALE*8, SCALE*1)
            self.width = 4
            self.text = 'Continue'
            self.color = pygame.Color('red2')
            self.text_color = pygame.Color('black')
            self.surf = Fonts.small.render(self.text, True, self.text_color)

        def update(self):
            ''' Add button 'button' and button 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.button)

            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.button.width,
                self.button.height)
            SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

class WaitingRoom:
    ''' Screen 2: Waiting Room
        *Wait for other users to join
        *Request status from users
        *Communicate data with server:
            Receive game history updates
            Receive game status
            Send player status
'''
    def __init__(self):
        self.background = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))
        self.code = WaitingRoom.Code()
        self.copycode = WaitingRoom.CopyCode()
        self.status = WaitingRoom.Status()
        self.history = WaitingRoom.History()
        self.cards = WaitingRoom.Cards()

        #Active Attributes
        self.active = {
            'Screen': True,
            'Status': False}

        interval = 0

        while self.active['Screen']:
            #Send player status
            SOCK.send(pickle.dumps(self.active['Status']))
            print('Sending Player Status({}) [{}]'.format(
                self.active['Status'],
                sys.getsizeof(self.active['Status'])))

            update = pickle.loads(SOCK.recv(2048))
            print('Receiving Game Update [{}]'.format(
                sys.getsizeof(update)))
            if not Game.history or update != Game.history[-1]:
                Game.history.append(update)

            self.active['Screen'] = pickle.loads(SOCK.recv(2048))
            print('Receiving Game Status({}) [{}]'.format(
                self.active['Screen'], sys.getsizeof(self.active['Screen'])))


            self.update_screen()
            if interval % 8 == 0:
                random.shuffle(self.cards.cards)
            interval += 1

            #Check Current Events
            for event in pygame.event.get():
                check_for_quit(event)
                #Mouse Click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #Collides with Start Button
                    if self.status.button.collidepoint(event.pos):
                        self.active['Status'] = not self.active['Status']
                        self.status.text = self.status.active\
                                           if self.active['Status']\
                                           else self.status.inactive
                    #Collides with Copy Button
                    if self.copycode.button.collidepoint(event.pos):
                        pyperclip.copy(Player.code)

    def update_screen(self):
        ''' Add Background image to Surface
            Display framerate
            Call each function 'update' function
            Update display
            Pass time between frames
'''

        SURFACE.blit(self.background, (0, 0))

        display_fps()

        self.code.update()
        self.copycode.update()
        self.status.update()
        self.history.update()
        self.cards.update()

        pygame.display.update()
        CLOCK.tick(30)

    class Code:
        ''' Display game code
'''
        def __init__(self, code=PORT):
            ''' Set Code attributes
'''
            self.box = pygame.Rect(SCALE*1, SCALE*1, SCALE*10, SCALE*2)
            self.text = 'Game Code: {}'.format(code)
            self.color = pygame.Color('dimgray')
            self.text_color = pygame.Color('white')
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self):
            ''' Add Code 'box' and Code 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.box)

            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.box.width,
                self.box.height)
            SURFACE.blit(self.surf, (self.box.x+10, self.box.y+mars[1]))            

    class CopyCode:
        ''' Copy Code to Clipboard
'''
        def __init__(self):
            ''' Set Copy Code attributes
'''
            self.button = pygame.Rect(SCALE*12, SCALE*1, SCALE*6, SCALE*2)
            self.text = 'Copy Code'
            self.color = pygame.Color('dodgerblue4')
            self.text_color = pygame.Color('white')
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self):
            ''' Add Copy Code 'button' and Copy Code 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.button)

            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.button.width,
                self.button.height)
            SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

    class Status:
        ''' Button to change player status
'''
        def __init__(self):
            ''' Set status attributes
'''
            self.active = 'Cancel'
            self.inactive = 'Ready'

            self.button = pygame.Rect(SCALE*19, SCALE*1, SCALE*12, SCALE*2)
            self.width = 4
            self.text = self.inactive
            self.color = pygame.Color('mediumseagreen')
            self.border = pygame.Color('ghostwhite')
            self.text_color = pygame.Color('white')
            self.surf = Fonts.main.render(self.text, True, self.text_color)

        def update(self):
            ''' Update Status 'text' to match status
                Update Status 'text_surf'
                Add Status 'button' and Status 'text_surf' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.button)
            pygame.draw.rect(SURFACE, self.border, self.button, self.width)

            self.surf = Fonts.main.render(self.text, True, self.text_color)
            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.button.width,
                self.button.height)
            SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

    class History:
        ''' Display game history
'''
        def __init__(self):
            ''' Set History attributes
'''
            self.box = pygame.Rect(SCALE*19, SCALE*4, SCALE*12, SCALE*12)
            self.width = 4
            self.color = pygame.Color('black')
            self.border = pygame.Color('ghostwhite')
            self.text_color = pygame.Color('white')
            self.surfs = []
            for event in Game.history:
                surf = Fonts.small.render(event, True, self.text_color)
                self.surfs.append(surf)
            self.gap = SCALE*0.25

        def update(self):
            ''' Update History 'text_surfs' to match Game 'History'
                Add History 'box' and History 'text_sufs' to Surface
'''
            pygame.draw.rect(SURFACE, self.color, self.box)
            pygame.draw.rect(SURFACE, self.border, self.box, self.width)

            height = SCALE*(len(Game.history)-1)\
                     +Fonts.small.size(Game.history[0])[1]
            if height > self.box.height:
                del Game.history[0]
            self.surfs = [Fonts.small.render(event, True, self.text_color)\
                          for event in Game.history]
            for i, surf in enumerate(self.surfs):
                SURFACE.blit(
                    surf, (
                        self.box.x+int(self.gap),
                        self.box.y+int(SCALE*i+self.gap))
                    )

    class Cards:
        ''' Simple animation which switches through cards randomly
'''
        def __init__(self):
            ''' Set Cards attributes
'''
            self.boxes = []
            for i in range(8):
                col = i%4
                row = i//4
                x_coord, y_coord = SCALE*(4*col+1), SCALE*(6*row+4)
                self.boxes.append(
                    pygame.Rect(x_coord, y_coord, int(SCALE*3.5), int(SCALE*5.5)))
            self.imgs = [pygame.image.load(f".\docs\{img}").convert()\
                         for img in GameData().card_images if '_1.' in img]
            self.cards = []
            for card in self.imgs:
                self.cards.append(
                    pygame.transform.scale(
                        card, (self.boxes[0].width, self.boxes[0].height)))
            self.color = pygame.Color('purple')

        def update(self):
            ''' Add each card 'box' and Card 'card_images' to Surface
'''
            for i, box in enumerate(self.boxes):
                pygame.draw.rect(SURFACE, self.color, box)
                SURFACE.blit(self.cards[i], (box.left, box.top))

class game_screen:
    ''' Screen 3: Game Screen
        *Allow players to virtually play the game
'''
    background = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))

    border_color = pygame.Color('white')
    border_width = 1
    box_width = 4

    class history:
        def __init__(self):
            self.box = pygame.Rect(SCALE*1, SCALE*1, SCALE*15, SCALE*8)
            self.width = 4
            self.color = pygame.Color('dimgray')
            self.border = pygame.Color('white')
            self.text_color = pygame.Color('white')
            self.surfs = []
            for event in Game.history:
                surf = Fonts.small.render(event, True, self.text_color)
                self.text_surfs.append(surf)
            self.gap = SCALE*0.25
        def update(self):
            pygame.draw.rect(SURFACE, self.color, self.box)
            pygame.draw.rect(SURFACE, sef.border, self.box, self.width)

            height = SCALE*(len(Game.history)-1)\
                     +Fonts.small.size(Game.history[0])[1]           
            if height > self.box.height:
                del Game.history[0]
            for event in Game.history:
                self.surfs.append(
                    Fonts.small.render(event, True, self.text_color))

            for i, surf in enumerate(self.surfs):
                SURFACE.blit(surf, (
                    self.box.x+int(self.gap),
                    self.box.y+int(SCALE*i+self.gap)))

    class turn:
        def __init__(self):
            self.color = pygame.Color('navy')
            self.text_color = pygame.Color('white')
        def update(self, turn):
            self.text = 'Turn: {}'.format(turn)
            self.surf = Fonts.small.render(self.text, True, self.text_color)
            SURFACE.blit(self.surf, (self.box.left, self.box.bottom+10))

    class rankings:
        def __init__(self):
            self.l_box = pygame.Rect(SCALE*17, SCALE*1, SCALE*11, SCALE*8)
            self.r_box = pygame.Rect(SCALE*28, SCALE*1, SCALE*3, SCALE*8)
            self.width = 4
            self.text_color = pygame.Color('dimgray')
            self.l_text = 'Name (Rank)'
            self.r_text = 'Cards Left'
            self.l_surf = Fonts.small.render(l_text, True, self.text_color)
            self.r_surf = Fonts.small.render(r_text, True, self.text_color)
        def update(self, order, cat, reverse):
            pygame.draw.rect(SURFACE, self.color, self.l_box, self.width)
            pygame.draw.rect(SURFACE, self.color, self.r_box, self.width)

            SURFACE.blit(self.l_surf, (self.l_box.x+10, self.l_box.y+int(SCALE*0.25)))
            SURFACE.blit(self.r_surf, (self.r_box.x+10, self.r_box.y+int(SCALE*0.25)))
            texts = order.get(cat)[::-1] if reverse else order.get(cat)
            for i, text in enumerate(texts, 1):
                l_surf = Fonts.small.render(text[0], True, self.text_color)
                r_surf = Fonts.small.render(text[1], True, self.text_color)
                SURFACE.blit(l_surf, (self.l_box.x+10, self.l_box.y+int(SCALE*(i+0.25))))
                SURFACE.blit(r_surf, (self.r_box.x+10, self.r_box.y+int(SCALE*(i+0.25))))

    class order:
        def __init__(self):
            self.text = 'Order:'
            self.text_color = pygame.Color('white')
            self.surf = fonts.small.render(self.text, True, self.text_color)
        def update(self):
            mars = center_text(
                self.surf.get_width(),
                self.surf.get_height(),
                self.surf.get_width(),
                SCALE*1)
            SURFACE.blit(self.text_surf, (SCALE*17, mars[1]))

        class rank:
            def __init__(self):
                self.button = pygame.Rect(SCALE*19, 0, SCALE*2, SCALE*1)
                self.width = 1
                self.color = pygame.Color('dodgerblue1')
                self.border = pygame.Color('white')
                self.active = pygame.Color('red')
                self.inactive = pygame.Color('white')
                self.text = 'Rank'
                self.text_color = self.active
                self.surf = fonts.main.render(self.text, True, self.text_color)
            def update(self):
                pygame.draw.rect(SURFACE, self.color, self.button)
                pygame.draw.rect(SURFACE, self.border, self.button, self.width)

                self.surf = fonts.small.render(self.text, True, self.text_color)
                mars = center_text(
                    self.surf.get_width(),
                    self.surf.get_height(),
                    self.button.width,
                    self.button.height)
                SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

        class cards:
            def __init__(self):
                self.button = pygame.Rect(SCALE*21, 0, SCALE*3, SCALE*1)
                self.width = 1
                self.text = 'Cards Left'
                self.color = pygame.Color('dodgerblue1')
                self.border = pygame.Color('white')
                self.active = pygame.Color('red')
                self.inactive = pygame.Color('white')
                self.text_color = self.inactive
                self.surf = fonts.main.render(self.text, True, self.text_color)
            def update(self):
                pygame.draw.rect(SURFACE, self.color, self.button)
                pygame.draw.rect(SURFACE, self.border, self.button, self.width)

                self.surf = fonts.small.render(self.text, True, self.text_color)
                mars = center_text(
                    self.surf.get_width(),
                    self.surf.get_height(),
                    self.button.width,
                    self.button.height)
                SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))

        class reverse:
            def __init__(self):
                self.button = pygame.Rect(SCALE*28, 0, SCALE*2, SCALE*1)
                self.width = 1
                self.text = 'Reverse'
                self.color = pygame.Color('dodgerblue1')
                self.border = pygame.Color('white')
                self.active = pygame.Color('red')
                self.inactive = pygame.Color('white')
                self.text_color = selfinactive
                self.surf = fonts.main.render(self.text, True, self.text_color)
            def update(self):
                pygame.draw.rect(SURFACE, self.color, self.button)
                pygame.draw.rect(SURFACE, self.border, self.button, self.width)

                self.surf = fonts.small.render(self.text, True, self.text_color)
                mars = center_text(
                    self.surf.get_width(),
                    self.surf.get_height(),
                    self.button.width,
                    self.button.height)
                SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))                

    class cards:
        class hand:
            def __init__(self):
                self.box = pygame.Rect(SCALE*8, SCALE*10, SCALE*23, int(SCALE*5.5))
                self.width = 4
                self.color = pygame.Color('purple')
                self.border = pygame.Color('ghostwhite')
                self.images = []
                self.cards = []
                self.rects = []
                self.card_info = {}

                for i, img in enumerate(Player.cards):
                    image = pygame.image.load(f".\docs\{img}")
                    card = pygame.transform.scale(
                        image, (int(SCALE*3.5), int(SCALE*5.5)))
                    rect = pygame.Rect(
                        self.box.x+SCALE*i,
                        self.box.y,
                        int(SCALE*3.5),
                        int(SCALE*5.5))
                    self.images.append(pygame.image.load(f".\docs\{img}"))
                    self.cards.append(pygame.transform.scale(
                        image, (int(SCALE*3.5), int(SCALE*5.5))))
                    self.rects.append(
                        pygame.Rect(
                            self.box.x+SCALE*i,
                            self.box.y,
                            int(SCALE*3.5),
                            int(SCALE*5.5)))
                    self.card_info.setdefault(
                        card,
                        {'Name': img,
                         'Converted Image': image,
                         'Rect': rect})
            def update(self, active):
                pygame.draw.rect(SURFACE, self.color, self.box, self.width)

                self.rects = [
                    pygame.Rect(
                        self.box.x+SCALE*i,
                        self.box.y,
                        int(SCALE*3.5),
                        int(SCALE*5.5))\
                    for i in range(len(self.cards))]

                self.cards = sorted(
                    self.cards,
                    key=lambda x:get_card(x).get('Value'))
                for i, rect in enumerate(self.rects):
                    pygame.draw.rect(SURFACE, self.border, rect, self.width)
                    SURFACE.blit(self.cards[i], (self.box.x+SCALE*i, self.box.y))

                if active['Card'] and active['Surf']:
                    pygame.draw.rect(SURFACE, self.border, active['Surf'], self.width)
                    SURFACE.blit(active['Card'], (
                        self.box.x+SCALE*self.cards.index(active['Card']),
                        self.box.y))
            def clicked(self, clicked):
                p_card = clicked['Card']
                p_rect = clicked['Rect']
                p_value = get_card(p_card).get('Value')

                if game_screen.cards.queue.cards:
                    q_card = game_screen.cards.queue.cards[-1]
                    q_value = get_card(prev_card).get('Value')

                if (self.cards and not p_value)\
                   or (not game_screen.cards.queue.cards and p_value)\
                   or (game_screen.cards.queue.cards\
                       and p_value == q_value):
                    game_screen.cards.queue.cards.append(p_value)
                    self.cards.remove(p_value)

                    game_screen.cards.queue.card_rects.append(p_rect)
                    self.card_rects.remove(p_rect)

        class queue:
            def __init__(self):
                self.box = pygame.Rect(int(SCALE*4.5), SCALE*10, int(SCALE*3.5), int(SCALE*5.5))
                self.width = 4
                self.color = pygame.Color('purple')
                self.text_color = pygame.Color('white')
                self.cards = []
                self.card_rects = []
            def update(self):
                pygame.draw.rect(SURFACE, self.color, self.box, self.width)

                for card_image in self.cards:
                    SURFACE.blit(card_image, (self.box.x, self.box.y))

                if self.cards:
                    num_cards = str(len(self.cards))
                    self.surf = fonts.large.render(num_cards, True, self.text_color)

                    mars = center_text(
                        self.surf.get_width(),
                        self.surf.get_height(),
                        self.box.width,
                        self.box.height)

                    SURFACE.blit(self.surf, (self.box.x+mars[0], self.box.y+mars[1]))

        class buttons:
            class clear:
                def __init__(self):
                    self.button = pygame.Rect(SCALE*1, SCALE*10, int(SCALE*3), int(SCALE*1.5))
                    self.text = 'Clear'
                    self.color = pygame.Color('red')
                    self.border = pygame.Color('white')
                    self.text_color = pygame.Color('white')
                    self.surf = fonts.small.render(self.text, True, self.text_color)
                def update(self):
                    pygame.draw.rect(SURFACE, self.color, self.button)
                    pygame.draw.rect(SURFACE, self.border, self.button, self.width)

                    mars = center_text(
                        self.surf.get_width(),
                        self.surf.get_height(),
                        self.button.width,
                        self.button.height)
                    SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))
                def clicked():
                    if game_screen.cards.queue.cards:
                        game_screen.cards.hand.cards += game_screen.cards.queue.cards
                        game_screen.cards.queue.cards = []
                        game_screen.cards.hand.card_rects += game_screen.cards.queue.card_rects
                        game_screen.cards.queue.card_rects = []

            class undo:
                def __init__(self):
                    self.button = pygame.Rect(SCALE*1, SCALE*12, int(SCALE*3), int(SCALE*1.5))
                    self.width = 4
                    self.text = 'Undo'
                    self.color = pygame.Color('red')
                    self.border = pygame.Color('white')
                    self.text_color = pygame.Color('white')
                    self.surf = fonts.small.render(self.text, True, self.text_color)
                def update(self):
                    pygame.draw.rect(SURFACE, self.color, self.button)
                    pygame.draw.rect(SURFACE, self.border, self.button, self.width)

                    mars = center_text(
                        self.surf.get_width(),
                        self.surf.get_height(),
                        self.button.width,
                        self.button.height)
                    SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))
                def clicked():
                    if game_screen.cards.queue.cards:
                        game_screen.cards.hand.cards.append(
                            game_screen.cards.queue.cards[-1])
                        game_screen.cards.queue.cards.remove(
                            game_screen.cards.queue.cards[-1])
                        game_screen.cards.hand.card_rects.append(
                            game_screen.cards.queue.card_rects[-1])
                        game_screen.cards.queue.card_rects.remove(
                            game_screen.cards.queue.card_rects[-1])
            class play:
                def __init__(self):
                    self.button = pygame.Rect(SCALE*1, SCALE*14, int(SCALE*3), int(SCALE*1.5))
                    self.width = 4
                    self.text = 'Play'
                    self.color = pygame.Color('red')
                    self.border = pygame.Color('white')
                    self.text_color = pygame.Color('white')
                    self.surf = fonts.small.render(self.text, True, self.text_color)
                def update(self):
                    pygame.draw.rect(SURFACE, self.color, self.button)
                    pygame.draw.rect(SURFACE, self.color, self.button, self.width)

                    mars = center_text(
                        self.surf.get_width(),
                        self.surf.get_height(),
                        self.button.width,
                        self.button.height)
                    SURFACE.blit(self.surf, (self.button.x+mars[0], self.button.y+mars[1]))
                def clicked():
                    if not game_screen.cards.queue.cards:
                        pass_turn = game_screen.cards.buttons.warning()
                        if not pass_turn:
                            return []

                    played_card = game_screen.cards.get_card(
                        game_screen.cards.queue.cards[0])
                    num_jesters = 0
                    for card in game_screen.cards.queue.cards:
                        test_card = game_screen.cards.get_card(card)
                        if test_card.get('Type') == 'Jester':
                            num_jesters += 1

                    played_cards = game_screen.cards.queue.cards
                    game_screen.cards.queue.cards = []
                    game_screen.cards.queue.card_rects = []
                    return played_cards

    def update_screen(classes, active, rankings):
        SURFACE.blit(game_screen.background, (0, 0))
        display_fps()

        funcs['History'].update()
        funcs['Turn'].update()
        if active['Order']['Rank']:
            category = 'Rank'
        elif active['Order']['Cards']:
            category = 'Cards'
        funcs['Rankings'].update(rankings, category, active['Order']['Reverse'])
        funcs['Order'].update()
        funcs['_Rank'].update()
        funcs['_Cards'].update()
        funcs['_Reverse'].update()
        funcs['Hand Cards'].update()
        funcs['Queue Cards'].update()
        funcs['_Clear'].update()
        funcs['_Undo'].update()
        funcs['_Play'].update()

        pygame.display.update()
        CLOCK.tick(30)

    def game_screen():
        classes = {
            'History': game_screen.history,
            'Turn': game_screen.turn,
            'Rankings': game_screen.rankings,
            'Order': game_screen.order,
            '_Rank': game_screen.order.rank,
            '_Cards': game_screen.order.cards,
            '_Reverse': game_screen.order.reverse,
            'Hand Cards': game_screen.cards.hand,
            'Queue Cards': game_screen.cards.queue,
            '_Clear': game_screen.cards.buttons.clear,
            '_Undo': game_screen.cards.buttons.undo,
            '_Play': game_screen.cards.buttons.play}
        funcs = {
            'History': game_screen.history(),
            'Turn': game_screen.turn(),
            'Rankings': game_screen.rankings(),
            'Order': game_screen.order(),
            '_Rank': game_screen.order.rank(),
            '_Cards': game_screen.order.cards(),
            '_Reverse': game_screen.order.reverse(),
            'Hand Cards': game_screen.cards.hand(),
            'Queue Cards': game_screen.cards.queue(),
            '_Clear': game_screen.cards.buttons.clear(),
            '_Button': game_screen.cards.buttons.undo(),
            '_Play': game_screen.cards.buttons.play()}

        #Active Attributes
        active = {
            'Order': {
                'Rank': True,
                'Cards': False,
                'Reverse': False},
            'Card': funcs['Hand Cards'].cards[-1],
            'Rect': funcs['Hand Cards'].rects[-1],
            'Screen': True,
            'Status': True,
            'Turn': False}
        turn = {
            'Quantity': 0,
            'Value': 0}

        while active['Screen']:
            SOCK.send(pickle.dumps(active['Status']))
            print('Sending Player Status({}) [{}]'.format(
                active['Status'], sys.getsizeof(active['Status'])))

            active['Turn'] = pickle.loads(SOCK.recv(2048))
            print('Reciving Turn({}) [{}]'.format(
                active['Turn'], sys.getsizeof(active['Turn'])))

            new_event = pickle.loads(SOCK.recv(2048))
            print('Receiving Game Update [{}]'.format(
                sys.getsizeof(new_event)))
            if not Game.history or new_event != Game.history[-1]:
                Game.history.append(new_event)

            rankings = pickle.loads(SOCK.recv(2048))
            print('Reciving Rankings [{}]'.format(
                sys.getsizeof(rankings)))
            game_screen.update_screen(classes, active, rankings)

            if active['Turn']:
                SOCK.sendall(pickle.dumps(played_cards))
                print('Sending Cards [{}]'.format(
                    sys.getsizeof(played_cards)))
                played_cards = []
                active['Turn'] = False
                if not len(funcs['_Hand'].cards):
                    active['Status'] = False

            #Check Current Events
            for event in pygame.event.get():
                check_for_quit(event)

                num_cards = len(funcs['Hand Cards'].rects)

                if event.type == pygame.MOUSEMOTION:
                    for i in range(num_cards-1, -1, -1):
                        test = funcs['Hand Cards'].rects[i]
                        if test.collidepoint(event.pos):
                            actives['Card'] = funcs['Hand Cards'].cards[i]
                            actives['Rect'] = funcs['Hand Cards'].rects[i]
                            break

                if event.type == pygame.MOUSEBUTTONDOWN and active['Turn']:
                    for i in range(num_cards-1, -1, -1):
                        test = funcs['Hand Cards'].card_rects[i]
                        if test.collidepoint(event.pos):
                            funcs['Hand Cards'].clicked(
                                funcs['Hand Cards'].cards[i],
                                funcs['Hand Cards'].rects[i])
                            break

                    if funcs['_Clear'].button.collidepoint(event.pos):
                        classes['_Clear'].clicked()

                    if funcs['_Undo'].button.collidepoint(event.pos):
                        classes['_Undo'].clicked()

                    if funcs['_Play'].button.collidepoint(event.pos):
                        played_cards = funcs['_Play'].clicked()

                    active['Card'] = False
                    active['Rect'] = False

                    if funcs['_Rank'].button.collidepoint(event.pos)\
                       or funcs['_Cards'].button.collidepoint(event.pos):
                        active['Order']['Rank'] = not active['Order']['Rank']
                        funcs['_Rank'].text_color = funcs['_Rank'].active\
                                                    if active['Order']['Rank']\
                                                    else funcs['_Rank'].inactive
                        active['Order']['Cards'] = not active['Order']['Cards']
                        funcs['_Cards'].text_color = funcs['_Cards'].active\
                                                     if active['Order']['Cards']\
                                                     else funcs['_Cards'].inactive

                    if funcs['_Reverse'].button.collidepoint(event.pos):
                        active['Order']['Reverse'] = not active['Order']['Reverse']
                        funcs['_Reverse'].text_color = funcs['_Reverse'].active\
                                                       if active['Order']['Reverse']\
                                                       else funcs['_Reverse'].inactive

def center_text(text_width, text_height, box_width, box_height):
    centered_x = int((box_width - text_width)/2)
    centered_y = int((box_height - text_height)/2)
    return centered_x, centered_y

def get_card(key):
    img = game_screen.cards.hand.card_info[key].get('Name')
    rank = game_data.role.rank_dict.get(img.split('_')[0])
    card_data = dict(('Value', rank.value), ('Title', rank.title))
    return card_data

def check_for_quit(event):
    if event.type == pygame.QUIT:
        SOCK.send(pickle.dumps(None))
        SOCK.close()
        pygame.quit()
        sys.exit()

def display_fps(digits=1):
    text_color = pygame.Color('white')
    fps = round(CLOCK.get_fps(), digits)
    percent_fps = round(fps/30*100, digits)
    fps_text = '{} FPS ({}%)'.format(fps, percent_fps)
    fps_surf = Fonts.small.render(fps_text, True, text_color)
    SURFACE.blit(fps_surf, (0, 0))

def main():
    HomeScreen()
    WaitingRoom()
    Player.rank, Player.cards = pickle.loads(SOCK.recv(2048))
    print(Player.rank)
    game_screen.game_screen()
        
if __name__ == '__main__':
    main()
    pygame.quit()
