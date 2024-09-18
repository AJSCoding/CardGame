# libraries
import pygame
import random
import os
import sys
import operator

# initialises pygame and the music
pygame.init()
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.mixer.music.load("phantomx27s-embrace-164479.mp3")
pygame.mixer.music.play(5, 0)
pygame.font.init()


# class to initialise the background image
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

# class of button to initialise a color, coordinates, size and text
class Button:
    def __init__(self, color, x, y, width, height, text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

# definition to draw the outline of the button and to render the text within the button
    def draw(self, screen, outline = None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 32)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x +(self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

# definition to find the position of the mouse and return true if within the button
    def isOver(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


# definition to count the total from the rank of each card in a players hand
def find_total():
    # locally assigns total a value of 0 to total
    total = 0
    # locally assigns a value of True to checking_total
    checking_total = True

    # if statement to declare an array called values for scores for each player
    if checking_total:
        checking_total = False
        for key in players:
            if num_players == 2:
                values = (players[key][0][0], players[key][1][0])
            if num_players == 3:
                values = (players[key][0][0], players[key][1][0], players[2][0])
            if num_players == 4:
                values = (players[key][0][0], players[key][1][0], players[2][0], players[3][0])

                # for loop to increase score with the value of each card in a players hand
            for i in range(cards_per_player):
                total += int(players[key][i][0])
            player_scores[key] = total

            total = 0
            if num_players == 2:
                values = (players[key][0][0], players[key][1][0])
            if num_players == 3:
                values = (players[key][0][0], players[key][1][0], players[2][0])
            if num_players == 4:
                values = (players[key][0][0], players[key][1][0], players[2][0], players[3][0])


# global string variable of the first state
current_state = "menu"
# global path of the background image
BackGround = Background('background.png', [0,0])
# global path of the menu image
Menu = Background('menu.png', [0,0])
# global path of the how_to_play image
htp = Background ('how_to_play.png', [0,0])
# global card_down_images array
card_down_images = {'OppositeRed'}
# global back_images array
back_images = {}
# global list of all the characters
characters = ['wizard', 'magician', 'swordsman', 'knight']
# global array to store the images
icon_images = {}
# global list of all the suits
suits = ['c', 'd', 'h', 's']
# global list of all the ranks
ranks = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']
# global array to store the card images
card_images = {}
# global list to store the names
names = []
# global font used
myfont = pygame.font.SysFont("monospace", 25)
# global integer used to set the width of the screen
screen_width = 850
# global integer used to set the height of the screen
screen_height = 690
# global integer of the width and height of the card
card_width, card_height = 84, 112.5
# global integer of the space between the cards
space_between_cards = 5
# global integer of the x coordinate of the first card placed
initial_x = 10
# global integer of the y coordinate of the first card placed
initial_y = 20
# global integer of the offset created for each card placed
y_offset = card_height + 46
# global string of inputted text
user_text = ''
# second global font used
base_font = pygame.font.Font(None, 35)
# global dimensions of the rect of the buttons
input_rect = pygame.Rect(200, 200, 140, 32)
# global color of the input bar when active
color_active = pygame.Color("lightskyblue")
# global color of the input bar when not active
color_passive = pygame.Color("gray15")
# declares color as color passive
color = color_passive
# integer variable of count
count = 0
# integer variable of the number of players
num_players = 4
# integer variable of the number of face down cards
back_cards_per_player = 1
# integer variable of the total number of game rounds
rounds = 5
# integer variable of the number of switches
switches = 5
# integer variable of the players turn
playerGo = 0
# boolean variable to reveal all the cards and scores at the end of the game round
reveal = False
# integer variable of the current round in a game round
current_round = 1
# integer variable of the current game round
game = 1
#  integer variable of the total scores
total = 0
# dictionary to store all player scores
player_scores = {}
# dictionary to store the total scores of each player
final_scores = {}
# boolean variable to restart the input loop
restart = False
# boolean variable to show all but the first cards in each hand
show = True

# for loop to join the suits and ranks and find the image path of the card
# cards are scaled and transformed to a specific size
for suit in suits:

    for rank in ranks:
        image_path = os.path.join("cards", f"{suit}{rank}.png")
        original_image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(original_image, (84, 112.5))
        card_images[(rank, suit)] = scaled_image

# for loop to find the image path, before scaling and transforming the image to a specific size
for card_down_image in card_down_images:
    back_path = os.path.join("cards", f"{card_down_image}.png")
    original_image = pygame.image.load(back_path)
    scaled_image3 = pygame.transform.scale(original_image, (84, 112.5))
    back_images[card_down_image] = scaled_image3

# for loop to find the image path of all the character icons, before scaling and transforming the images to a specific size
for character in characters:
    character_path = os.path.join("characters", f"{character}.png")
    original_image = pygame.image.load(character_path)
    scaled_image2 = pygame.transform.scale(original_image, (84, 112.5))
    icon_images[character] = scaled_image2

# sets the screen display with the declared width and height
screen = pygame.display.set_mode((screen_width, screen_height))
# sets caption of the display
pygame.display.set_caption("Card Dealing Simulator")

# declares buttons with specific colors, coordinates, sizes and text through the Button class
startButton = Button((0, 255, 0), 580, 550, 250, 75, 'Start')
howToButton = Button((0, 0, 255), 300, 550, 250, 75, 'How to Play')
quitButton = Button((255, 0, 0), 30, 550, 250, 75, 'Quit')
quit2Button = Button((255, 0, 0), 620, 610, 200, 75, 'Quit')
goButton = Button((255, 0, 0), 620, 520, 200, 75, 'Go')
playerButton2 = Button((100, 250, 100), 400, 172, 250, 75, '2 Players')
playerButton3 = Button((100, 250, 100), 400, 272, 250, 75, '3 Players')
playerButton4 = Button((100, 250, 100), 400, 372, 250, 75, '4 Players')
RoundButton1 = Button((100, 250, 100), 120, 175, 250, 75, '1 Round')
RoundButton3 = Button((100, 250, 100), 120, 275, 250, 75, '3 Rounds')
RoundButton5 = Button((100, 250, 100), 120, 375, 250, 75, '5 Rounds')
shuffleButton = Button((100, 100, 250), 620, 610, 200, 75, 'Shuffle')
switchButton = Button((100, 100, 250), 330, 620, 200, 65, 'Switch/Hide')
keepButton = Button((100, 100, 250), 120, 620, 200, 65, 'Keep/Show')
continueButton = Button((100, 100, 250), 620, 520, 200, 65, 'Continue')
menuButton = Button((100, 100, 250), 620, 620, 200, 65, 'Menu')

# integer variable of the cards of each player
cards_per_player = 2
# dictionary to store the items of each player
players = {}

# boolean variable to determine whether the game is running
running = True
# boolean variable to determine whether a button has been pressed
active = False

# list of all the cards
deck = [(rank, suit) for suit in suits for rank in ranks]
# shuffles the deck of cards
random.shuffle(deck)

# while loop of the game
while running:
# finds position of the mouse
    pos = pygame.mouse.get_pos()

# for loop to stop the game loop on quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

# nested if statement to receive text input from a player
# sets active to True to change the input tab colour on a key input
        if event.type == pygame.KEYDOWN:
            active = True

# decreases the input text by a character on a backspace input
# increases the input text by a unicode character on any other input
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[0: -1]
            else:
                user_text += event.unicode

# appends the user text to the names array on carriage return input
# sets the user text to upper case
            if event.key == pygame.K_RETURN:
                restart = False
                user_text = user_text[0].upper() + user_text[1:]
                user_text = user_text[:-1]
                names.append(user_text)
# clears names array for fresh inputs if character length less than one
                if len(user_text) < 1 and count < num_players:
                    names = []
                    count = 0
                    restart = True
                active = False
                user_text = ""
# clears name array if duplicate entries are found
                if count != num_players:
                    for i in range(len(names) - 1):
                        for j in range(i + 1, len(names)):
                            if names[i] == names[j]:
                                names = []
                                count = 0
                                restart = True

# increases count to ask for next player input
                if restart == False:
                    count += 1

# nested if statement on click
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound("click-button-140881.mp3"))

# if statement to move onto round state and play new music when in menu
            if startButton.isOver(pos) and current_state == "menu":
                current_state = "Round"
                pygame.mixer.music.load("african-funk-202107.mp3")
                pygame.mixer.music.play(5, 0)

# if statement to redeclare the rounds to the button pressed and move onto the start state
            if RoundButton1.isOver(pos) or RoundButton3.isOver(pos) or RoundButton5.isOver(pos):
                if RoundButton1.isOver(pos) and current_state == "Round":
                    rounds = 1
                    current_state = "start"
                elif RoundButton3.isOver(pos) and current_state == "Round":
                    rounds = 3
                    current_state = "start"
                elif RoundButton5.isOver(pos) and current_state == "Round":
                    current_state = "start"

# if statement to redeclare the number of players to the button pressed and the number of switches
# assigns each player a hand of cards and moves onto the pre-game state
            if playerButton2.isOver(pos) or playerButton3.isOver(pos) or playerButton4.isOver(pos):

                if playerButton2.isOver(pos) and current_state == "start":
                    num_players = 2
                    players = {i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)}
                    current_state = "pre-game"
                    switches = 2 * num_players

                elif playerButton3.isOver(pos) and current_state == "start":
                    num_players = 3
                    players = {i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)}
                    current_state = "pre-game"
                    switches = 2* num_players

                elif playerButton4.isOver(pos) and current_state == "start":
                    num_players = 4
                    players = {i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)}
                    current_state = "pre-game"
                    switches = 2 * num_players

# if statement to re-deal cards on click of shuffle button
            if current_state == "game" and shuffleButton.isOver(pos):
                deck = [(rank, suit) for suit in suits for rank in ranks]
                random.shuffle(deck)
                players = {i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)}

# if statement to change state to how to play on how to button click in the menu state
            if howToButton.isOver(pos) and current_state == "menu":
                current_state = "how_to_play"

# if statement to change state to menu on menu button click in the how to play state
            if menuButton.isOver(pos) and current_state == "how_to_play":
                current_state = "menu"

# if statement to change state to in play on click of hte go button in the game state
# first card is covered in each player's hand
            if goButton.isOver(pos) and current_state == "game":
                current_state = "in_play"
                players2 = {i: [back_images for _ in range(1)] for i in range(num_players)}

# nested if statement on click of the switch button and there are switches available
# nested if statement on click of the keep button
            if switchButton.isOver(pos) and switches != 0 or keepButton.isOver(pos):

# increases the player go by one
                playerGo += 1

# increases the round by one if all players have gone
                if playerGo == num_players:
                    current_round += 1

# increases the number of cards and unrevealed cards by one
                    if current_round > 1 and current_round < 5:
                        cards_per_player += 1
                        back_cards_per_player += 1
                    elif current_round == 5:
                        reveal = True

# nested if statement to reveal all the cards after 5 cards or if no switches are available on click of the switch button
# otherwise, re-deal all the cards and decrease the switch counter by one
                if switchButton.isOver(pos) and current_state == "in_play":
                    if current_round > 4 or switches == 0:
                        deck = [(rank, suit) for suit in suits for rank in ranks]
                        random.shuffle(deck)
                        players = ({i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)})
                        show = True
                    elif current_round != 5 or switches > 0:
                        show = False
                        switches -= 1
                        deck = [(rank, suit) for suit in suits for rank in ranks]
                        random.shuffle(deck)
                        players = ({i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)})
                        players2 = {i: [back_images for _ in range(back_cards_per_player)] for i in range(num_players)}

# if statement to show all the cards and assign switches with the lowest value of 0 on click of the switch button when switches is 0 or less
                    if switchButton.isOver(pos) and switches <= 0:
                        switches = 0
                        show = True

# nested if statement to show all the cards but the first card on click of the keep button in the in play state
                if keepButton.isOver(pos) and current_state == "in_play":
                    players2 = {i: [back_images for _ in range(1)] for i in range(num_players)}
                    show = True

# if statement to append a new card to all players if a new round is started through the keep button
                    if playerGo == num_players and current_round < 5:
                        deck = [(rank, suit) for suit in suits for rank in ranks]
                        random.shuffle(deck)
                        for i in range (num_players):
                            new_card = ([deck.pop()])
                            players[i].extend(new_card)

# if statement with for loop to append all the scores of the players in each round to the final scores dictionary on click of the continue button
            if continueButton.isOver(pos) and current_state == "in_play" and reveal == True:

                for key, value in player_scores.items():
                    if key in final_scores:
                        final_scores[key] += value
                    else:
                        final_scores[key] = value

# if statement to start new round depending on the number of rounds chosen
                if game < rounds:
                    print(final_scores)
                    game += 1
                    cards_per_player = 2
                    deck = [(rank, suit) for suit in suits for rank in ranks]
                    random.shuffle(deck)
                    players = ({i: [deck.pop() for _ in range(cards_per_player)] for i in range(num_players)})
                    reveal = False
                    switches = 2 * num_players
                    back_cards_per_player = 1
                    playerGo = 0
                    current_round = 1
                    current_state = "game"

# otherwise change the state to results
                else:
                    current_state = "results"
                    print(final_scores)
# exits the program on clck of the quit button
            if quitButton.isOver(pos) and current_state == "menu" or quit2Button.isOver(pos) and current_state == "in_play" or quitButton.isOver(pos) and current_state == "results":
                running = False

# fills the screen with white rgb value for the menu image to be shown as a background
# shows the image path of fredericko after scaling and transforming the image path at a set destination
    screen.fill([255, 255, 255])
    screen.blit(Menu.image, Menu.rect)
    image_path = "Fredericko.png"
    original_image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale(original_image, (130, 162.5))
    screen.blit(scaled_image, (screen_width / 1.16, 1))

# nested if statement to draw the input bar that is transformed and scaled at a set destination
    if current_state == "pre-game":

        if active:
            color = color_active
        else:
            color = color_passive

        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(430, text_surface.get_width() + 10)

# draw title with start, how to play and quit buttons in menu state
    if current_state == "menu":
        font = pygame.font.SysFont('comicsans', 35)
        text = font.render('Welcome to Cards With Character', 1, (0, 0, 0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 3 - text.get_height() / 2))
        startButton.draw(screen, (0, 0, 0))
        howToButton.draw(screen, (0, 0, 0))
        quitButton.draw(screen, (0, 0, 0))

# draw title with player 2, player 3 and player 4 buttons in start state
    if current_state == "start":
        text = font.render('How many people are playing?', 1, (0, 0, 0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 5.5 - text.get_height() / 2))
        playerButton2.draw(screen, (0, 0, 0))
        playerButton3.draw(screen, (0, 0, 0))
        playerButton4.draw(screen, (0, 0, 0))

# draw title with round 1, round 3 and round 5 buttons in the round state
    elif current_state == "Round":
        text = font.render('How Many Rounds would you like?', 1, (0, 0, 0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 5 - text.get_height() / 2))
        RoundButton1.draw(screen, (0, 0, 0))
        RoundButton3.draw(screen, (0, 0, 0))
        RoundButton5.draw(screen, (0, 0, 0))

# if current state is pre-game
    elif current_state == "pre-game":

# for loop to draw all the characters with an x offset
        if count <= num_players:
            x_offset = 95

            for character in characters:
                screen.blit(icon_images[character], (initial_x + x_offset, 300))
                x_offset += 175
            x_offset = 95

# for loop to draw all the names with an x offset
            for name in names:
                text_surface = myfont.render(name, False, (255, 255, 255))
                screen.blit(text_surface, (initial_x + x_offset, 420))
                x_offset += 175

# if statement to render after all players have a name assigned
        if count == num_players:
            go = font.render("Type anything to Start", 1, (0, 0, 0))
            screen.blit(go, (195, screen_height / 4 - 20 - text.get_height() / 2))

# if statement to move to the game state after shuffling all the player names with their corresponding icons
        if count > num_players:
            pygame.time.delay(1000)
            names = names[:-1]
            words = [name for name in names]
            icons = [character for character in characters]
            temp = list(zip(words, icons))
            random.shuffle(temp)
            words, icons = zip(*temp)
            words, icons = list(words), list(icons)
            character_name = {i: [words.pop()] for i in range(num_players)}
            player_character = {i: [icons.pop()] for i in range(num_players)}
            current_state = "game"
# if statement to render the text for a player name input
        if count < num_players:
            instruction = font.render("Player " + f"{count + 1}", 1, (0, 0, 0))
            title = font.render("Type your Player name", 1, (0, 0, 0))
            screen.blit(instruction, (350, screen_height / 8 - text.get_height() / 2))
            screen.blit(title, (195, screen_height / 4 - 10 - text.get_height() / 2))

# if statement to render if an invalid input has been received
        if restart == True:
            text = font.render('A duplicate/null value has been received!', 1, (0, 0, 0))
            screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 1.3 - text.get_height() / 2))
            text = font.render('Try again', 1, (0, 0, 0))
            screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 1.2 - text.get_height() / 2))

# if current state is game, render the background image with the shuffle button
    elif current_state == "game":
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        shuffleButton.draw(screen, (0, 0, 0))
        goButton.draw(screen, (0, 0, 0))

# for loop to render all the cards for each player and the face down card images
        for player, cards in players.items():
            x_offset = 95
            x_offset3 = 95

            for card in cards:
                screen.blit(card_images[(card[0],card[1])], (initial_x + x_offset, initial_y + (player * y_offset)))
                x_offset += card_width + space_between_cards

            for card_down_image in card_down_images:
                screen.blit(back_images[card_down_image], (initial_x + x_offset3, initial_y + (player * y_offset)))
                x_offset3 += card_width + space_between_cards

# render quit button with background and the number of switches available if state is in play
    elif current_state == "in_play":
        myfont.set_underline(True)
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
        quit2Button.draw(screen, (0, 0, 0))
        if reveal != True:
            text = font.render('Switches: ' + f'{switches}  ', 1, (255, 255, 255))
            screen.blit(text, (screen_width - text.get_width() - 10, 550))
            text = font.render('Round ' + f'{game}' + '.' + f'{current_round}', 1, (255, 255, 255))
            screen.blit(text, (screen_width - text.get_width() - 60, 505))

# for loop to render the cards of each player
        for player, cards in players.items():
            x_offset = 95

            for card in cards:
                screen.blit(card_images[(card[0],card[1])], (initial_x + x_offset, initial_y + (player * y_offset)))
                x_offset += card_width + space_between_cards

# render the keep button if still in a round and the switch button is switches are available
        if reveal != True:
            keepButton.draw(screen, (0, 0, 0))
            if switches != 0:
                switchButton.draw(screen, (0, 0, 0))
# render face down images
            for player2, cards in players2.items():
                x_offset = 95

                for card in cards:
                    screen.blit(back_images[card_down_image], (initial_x + x_offset, initial_y + (player2 * y_offset)))
                    x_offset += card_width + space_between_cards

        # otherwise render the continue button
        else:
            continueButton.draw(screen, (0, 0, 0))


# for loop to render all the character icons
        y_offset2 = 0
        x_offset2 = 0

        for player, characters in player_character.items():

            for character in characters:
                screen.blit(icon_images[character], (initial_x + (player * x_offset2), initial_y + y_offset2))
                y_offset2 += card_height + 50

        y_offset3 = 110
        x_offset3 = 0

# for loop to render all the player names and highlight the name in green if it`s the players go, starting from player 1
        for player, names in character_name.items():

            for name in names:

                try:
                    if name == character_name[playerGo][0]:
                        text_surface = myfont.render(name, False, (0, 255, 0))
                        screen.blit(text_surface, (initial_x + (player * x_offset3), initial_y + y_offset3))
                        y_offset3 += card_height + 50
                    else:
                        text_surface = myfont.render(name, False, (255, 0, 0))
                        screen.blit(text_surface, (initial_x + (player * x_offset3), initial_y + y_offset3))
                        y_offset3 += card_height + 50
                except:
                    playerGo = 0

# if statement to use the find_total definition to calculate the scores of each hand
        if show != False:
            find_total()
            x_offset = 0
            i = 0

# for loop to render the scores of each hand depending on how many players are playing
            for i in range(3):
                x_offset += 100
                text = font.render(f'{character_name[i][0][0]}' + ': ' + f'{player_scores[i]}', 1, (255, 119, 0))
                screen.blit(text, (screen_width / 1.17 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 - 350 + x_offset))
                if i == num_players - 1:
                    break

# if statement to render that the scores are unknown when show is false
        if show == False:
            text = font.render(f'Scores: ?', 1, (255, 119, 0))
            screen.blit(text, (screen_width / 1.17 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 - 250))

# render the title and quit button in results state before calculating the scores of each player through the find_total definition
    if current_state == "results":
        quitButton.draw(screen, (0, 0, 0))
        find_total()

        text = font.render('Total Scores', 1, (255, 119, 0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 - 300))
        x_offset = 0
        i = 0

# for loop to render all the total scores of each player based on the number of players
        for i in range(3):
            x_offset += 110
            text = font.render(f'{character_name[i][0]}' + ': ' + f'{final_scores[i]} points', 1, (255, 119, 0))
            screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2 - 300 + x_offset))
            if i == num_players - 1:
                break
# finds the maximum final score and renders its corresponding player name as the winner
        winner = max(final_scores.items(), key = operator.itemgetter(1))[0]
        text = font.render(f'The winner is: {character_name[winner][0]}', 1, (255, 119, 0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 1.3 - text.get_height() / 2))

# renders the title and menu button in the how to play state
    elif current_state == "how_to_play":
        screen.fill([255, 255, 255])
        screen.blit(htp.image, htp.rect)
        menuButton.draw(screen, (0, 0, 0))
        text_font = pygame.font.SysFont('cambriamath', 18)
        text = font.render ('How to Play!', 1, (200,0,0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 10 - text.get_height() / 2))

# renders the paragraph of text that set to uppercase and returned to a new line depending on the instance of \n
        paragraph = '\n\nThe players` turn is shown by their name being highlighted in green!\n\nthe aim of the game is to have a hand of cards with the highest ranks!\n\n when it is your turn, decide to keep your last card\nor mess around with your mates by switching all hands!\n\nhowever, be careful of how many switches are left!\nDecide whether you want to gamble and gain better cards\nor stick with what you have!'
        paragraph = paragraph.upper()
        lines = paragraph.split('\n')
        for i, line in enumerate(lines):
            text = text_font.render(line, True, (80, 0, 255))
            screen.blit(text, (60, 60 + (40 * i)))
        text = text_font.render ('The game ends when all players receive 5 cards', 1, (255, 0, 0))
        screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 1.24 - text.get_height() / 2))

# updates the pygame display while running
    pygame.display.flip()
    pygame.display.update()

# quits the pygame display when not running
pygame.quit()