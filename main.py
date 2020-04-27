from kivy.config import Config
Config.set('graphics','resizable',0)
from kivy.app import App
from kivy.metrics import cm,dp,sp,Metrics
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from random import shuffle, randrange, choice, choices
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.uix.actionbar import ActionBar,ActionPrevious,ActionView,ActionButton
from kivy.graphics import Color, Rectangle, BorderImage
from kivy.core.audio import SoundLoader
import time
from kivy.uix.image import Image,AsyncImage
from kivy.atlas import Atlas
from kivy.base import runTouchApp
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
# Config.set('graphics', 'width', '1080')
# Config.set('graphics', 'height', '2340')
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.animation import Animation
from kivy.clock import Clock
'''Changelog: 1) Added Wrath of Ashardalon, 2) Changes to tools and deck changes, 3) Added Treasure Tokens, 
4) Monster Tokens and level up system changed, 5) Sound effects added, 6) Much more...
7) Experimental TOEE/Ravenloft Added'''

RESOLUTION_CHOICE = (1280, 720)
def get_resolution():
    try:
        global RESOLUTION_CHOICE
        preferences = JsonStore('settings.json')
        RESOLUTION_CHOICE = tuple(preferences.get('resolution')['resolution'])
    except:
        pass

#Get resolution from choice
get_resolution()

#Metrics/Window
Window.size = RESOLUTION_CHOICE
if Window.height <= 480:
    Metrics.density = 1
    Metrics.fontscale = .8
elif Window.height <= 720:
    Metrics.density = 1.5
    Metrics.fontscale = 0.8
elif Window.height <= 2040:
    Metrics.density = 2
    Metrics.fontscale = .9

#Change Resolution
def resolution_changer(instance,value):
    global RESOLUTION_CHOICE
    resolution_pop = Popup(title='Restart?', separator_color=[0, 100 / 255, 0, 1], title_size='18sp',title_align='center',
                           size_hint=(.4, .25),auto_dismiss=False)
    resolution_grid = BoxLayout(orientation='horizontal')
    resolution_grid_second = GridLayout(cols=1)
    yes_btn = Button(text='YES')
    no_btn = Button(text='NO')
    res_label = Label(text='To apply the changes you need to restart the application. Restart now?',
                                            size_hint_y=None,markup=True,halign='left', valign='bottom')
    res_label.text_size = ((Window.width * .35), None)
    res_label.texture_update()
    res_label.height = res_label.texture_size[1]
    resolution_grid_second.add_widget(res_label)
    resolution_grid.add_widget(yes_btn)
    resolution_grid.add_widget(no_btn)
    resolution_grid_second.add_widget(resolution_grid)
    resolution_pop.content = resolution_grid_second
    resolution_pop.open()

    if value == '1920x1080':
        RESOLUTION_CHOICE = (1920,1080)
    if value == '1280x720':
        RESOLUTION_CHOICE = (1280, 720)
    if value == '720x480':
        RESOLUTION_CHOICE = (720, 480)
    mainbutton.text = 'Resolution: {}'.format(str(RESOLUTION_CHOICE[0]) + 'x' + str(RESOLUTION_CHOICE[1]))
    no_btn.bind(on_release=resolution_pop.dismiss)
    yes_btn.bind(on_release=save_preference)
    yes_btn.bind(on_release=DnDGenerator().stop)


backImages_list = ['images/dnd_background.jpg', 'images/dnd_background_2.jpg', 'images/dnd_background_3.jpg']
shuffle(backImages_list)
fireworks = Image(source='images/fireworks.zip', allow_stretch=True, anim_delay=.1, anim_loop=3,
                          keep_ratio=True,
                          keep_data=False)

win_sound = SoundLoader.load('music/win.ogg')
firework_sound = SoundLoader.load('music/fireworks.ogg')
#Theme Music
# theme = SoundLoader.load('theme.mp3')
# if theme:
#     print("Sound found at %s" % theme.source)
#     print("Sound is %.3f seconds" % theme.length)
#     theme.loop = True
#     theme.play()
#Settings Pop and Values

#Save Preferences
def save_preference(instance):
    global RESOLUTION_CHOICE
    preferences = JsonStore('settings.json')
    preferences.put('music', check=check_music.active)
    preferences.put('save', check=check_save.active)
    preferences.put('resolution', resolution=RESOLUTION_CHOICE)
    settings.dismiss()

settings = Popup(title='Settings', separator_color=[0, 100 / 255, 0, 1], size_hint=(.5, .5),auto_dismiss=False)
grid_settings = GridLayout(cols=1)
grid_settings_second = GridLayout(cols=2,size=(settings.width, settings.height))
check_music = CheckBox(active=True)
check_save = CheckBox(active=False)

# Making a resolution button
resolution = DropDown()
resolutions = ['1920x1080', '1280x720', '720x480']
resolution_choice = Window.size
for item in resolutions:
    # When adding widgets, we need to specify the height manually
    # (disabling the size_hint_y) so the dropdown can calculate
    # the area it needs.

    btn = Button(text=item, size_hint_y=None, height=30)

    # for each button, attach a callback that will call the select() method
    # on the dropdown. We'll pass the text of the button as the data of the
    # selection.
    btn.bind(on_release=lambda btn: resolution.select(btn.text))

    # then add the button inside the dropdown
    resolution.add_widget(btn)
# create a big main button
mainbutton = Button(text='Resolution: {}'.format(str(Window.width) + 'x' + str(Window.height)),size_hint_y=None,height=60)
# show the dropdown menu when the main button is released
# note: all the bind() calls pass the instance of the caller (here, the
# mainbutton instance) as the first argument of the callback (here,
# dropdown.open.).
mainbutton.bind(on_release=resolution.open)

# one last thing, listen for the selection in the dropdown list and
# assign the data to the button text.
# resolution.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
resolution.bind(on_select=resolution_changer)

grid_settings.add_widget(mainbutton)
grid_settings_second.add_widget(Label(text='Autosave'))
grid_settings_second.add_widget(check_save)
grid_settings_second.add_widget(Label(text='Sound'))
grid_settings_second.add_widget(check_music)
#End

grid_settings.add_widget(grid_settings_second)
btn_ok =Button(text='SAVE SETTINGS',font_size='18sp', background_color=(1,0,0,1),size_hint_y=.15)
grid_settings.add_widget(btn_ok)
settings.content = grid_settings
btn_ok.bind(on_release=save_preference)


#Levels Pop
level_pop = Popup(title='Give a level to: ', title_size='18sp',title_align='center',separator_color=[0, 100 / 255, 0, 1],
                         size_hint=(.4, .4))
#Choose heroes pop
prompt_heroes = Popup(title='Choose Heroes or don\'t for random heroes.(1-4)', title_size='18sp',title_align='center',separator_color=[0, 100 / 255, 0, 1],
                         size_hint=(1, 1),auto_dismiss=False)
# prompt_heroes.content = BoxLayout(orientation='vertical')
gridforpop = GridLayout(cols=1)
prompt_heroes.content = gridforpop



#Help Pop and values
text = 'Dungeons and Dragons - Campaign Generator is unofficial' \
       ' Fan Content permitted under the Fan Content Policy. Not approved/endorsed by Wizards. Portions of the materials ' \
       'used are property of Wizards of the Coast. ©Wizards of the Coast LLC.\n\nThis app simulates a campaign using the ' \
       'Dungeons and Dragons board games by Wizards of the Coast.\nInstructions:' \
       ' \n1) Press "Create Campaign" to automatically generate the first adventure of your campaign. First you have to ' \
       'choose the board games that you would like to use for the campaign and then you will be asked to choose the heroes ' \
       'that you would like to have for the entire campaign. You can choose up to 4 heroes. If you choose none, then the ' \
       'app will generate 4 random heroes for you.\n2) Follow the instructions on the adventure case on the bottom left ' \
       'of the screen. There are currently 7 types of adventures: \ni) Slay Monsters - where you need to slay x number of' \
       ' a specific species of monsters. \nii) Save Villager - where you need to rescue an innocent, which means when you' \
       ' find him on the trigger tile (the tile placed between the 9th and 12th tile in the dungeon stack), you need to' \
       'carry him all the way to the starting tile.\niii) Rescue Ally - where you need to save one of your allies. Works' \
       'the same way as the Save Villager except when you find the trigger tile you connect it with an extra tile and add ' \
       '3 monsters on this extra tile. You can use the ally card for this ally if you have it. You need to slay every ' \
       'monster to win this adventure.\niv) Reclaim Item - where you need to reclaim the specific item listed (which means' \
       ' that you will own it after completing the adventure). When you reveal the trigger tile you connect it with an ' \
       'extra one and put the item on this new extra tile along with any monsters/traps that both tiles have. To win just ' \
       'kill every monster and end your turn on the tile with the item (the extra tile).\nv) Destroy Item - where you reveal' \
       ' the item with the trigger tile and you attack it as though it were a monster. You draw monsters/traps as usual ' \
       'and you win when you destroy the item.\nvi) Slay Villain(s) - where you reveal the villain(s) on the trigger tile ' \
       'and you win when you defeat them.\nvii) Kill Boss - where you reveal the boss(es) on the extra tile which is ' \
       'connected to the trigger tile and you win when you kill them.\n3) After you succeed in the adventure you can press' \
       ' the "Next Adventure" button to start the next adventure and so on. If you decide to take a break, you can press' \
       '"Save" so that the app saves the current state of the campaign. Press "Load" when you want to restore the campaign' \
       ' that you saved.\n4) When you start a new adventure you need to follow the instructions listed on Deck Changes, ' \
       'if you can\'t follow one, just adjust as you see fit.\n5) Gold and Items are just notepads for you to note each ' \
       'of these things for each hero.\n6) The Tools button is used for a few things. LVL Up is used to level up the heroes' \
       ' that you want to. Leveling costs 2000 for LVL-2, 3000 for LVL-3 and 4000 for LVL-4. You can also roll a D20 ' \
       'if you feel like it! Monster tokens could be used at the exploration phase for the first three board games, to let' \
       ' you know how many monsters you should place it the new tile.\n\nVillain Rules: Due to many board games in the series, the difficulty is not adjusted correctly. ' \
       'This happens because earlier games in the series were not supposed to be played as a campaign. ' \
       'To counter this, Villains will get three difficulty versions: [EASY], [NORMAL] and [HARD]. You can see the villain changes for each version in the villains manual.'
help = Popup(title='Help', separator_color=[0, 100 / 255, 0, 1], size_hint=(.75, .75))
# help_text = TextInput(text=text, multiline=True, disabled=True, background_color=[0,0,0,0], disabled_foreground_color=[1,1,1,1], size_hint_y=None)
help_text = Label(text=text,size_hint_y=None,markup=True,halign='left', valign='bottom')
help_text.text_size = ((Window.width*.7), None)
help_text.texture_update()
help_text.height = help_text.texture_size[1]
some_scroll = ScrollView()
some_scroll.add_widget(help_text)
help.content = some_scroll

#Villain Manual Pop-up
villain = Popup(title='Villains Manual', separator_color=[0, 100 / 255, 0, 1], size_hint=(.75, .75), title_size= '16sp')
some_text = '[size=22sp][b]Wrath of Ashardalon[/b][' \
            '/size]\n\n[size=18sp][color=#c138e7][b][u]1) Ashardalon, ' \
            'Red Dragon[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: AC:15, HP:10, Tactics: Same as ' \
            'Card.\n[' \
            'color=#edde37][NORMAL][/color]: Same as Card.\n[color=#ff0000][HARD][/color]: AC:17, HP:20, ' \
            'Tactics: 1) TAIL SWEEP: 2 DMG + EFFECT, 2) BITE: 2DMG + EFFECT.\n[color=#ae0606][EXTREME][/color]: ' \
            'AC: 18, HP:27, TACTICS: 1) TAIL SWEEP: +12, 2 DMG + EFFECT, 2) BITE: +12, 2DMG + EFFECT.' \
            '\n\n[size=18sp][color=#c138e7][b][u]2) Bellax, ' \
            'Gauth[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card.\n[' \
            'color=#edde37][NORMAL][/color]: AC:17, HP:14, TACTICS: Same as Card.\n[color=#ff0000][HARD][/color]: ' \
            'AC:17, HP:20, TACTICS: + 1 DMG TO ALL TACTICS.\n[color=#ae0606][EXTREME][/color]: ' \
            'AC:18, HP:24, TACTICS: +1 DMG TO ALL TACTICS, +10 ATTACK TO ALL TACTICS.' \
            '\n\n[size=18sp][color=#c138e7][b][u]3) Rage ' \
            'Dragon[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card.\n[' \
            'color=#edde37][NORMAL][/color]: RAGED: AC:14, HP:9, TACTICS: SAME AS CARD, ENRAGED RAGE: AC:16, HP:12, ' \
            'TACTICS: Same as Card.\n[color=#ff0000][HARD][/color]: ' \
            'RAGED: AC:14, HP:11, TACTICS: BITE: 2DMG + EFF, CHARGE: 2DMG + DAZED, ENRAGED RAGE: AC: 16, HP:14, ' \
            'TACTICS: CLAWS: 3DMG + EFF.\n[color=#ae0606][EXTREME][/color]: ' \
            'RAGED: AC:15, HP:12, TACTICS: BITE: 2DMG + EFF, CHARGE: 2DMG + DAZED, ENRAGED RAGE: AC: 17, HP:16, TACTICS: CLAWS: 3DMG + EFF.' \
            '\n\n[size=18sp][color=#229fed][u]4) Kraash, Orc Storm Shaman[/u][' \
            '/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card.\n[color=#edde37][' \
            'NORMAL][/color]: AC:15, HP:10, TACTICS: Same as Card.\n[color=#ff0000][HARD][/color]: AC:16, HP:14, TACTICS: WINDSTORM: 2DMG + EFF, LIGHTNING: 2DMG + EFF\n\n[' \
            'size=18sp][color=#229fed][u]5) Meerak, Kobold Dragonlord[/u][/color][/size]\n[color=#1fed2d][EASY][/color]: ' \
            'Same as Card.\n[color=#edde37][NORMAL][/color]: AC:18, HP:9, TACTICS: Same as Card.\n[color=#ff0000][' \
            'HARD][/color]: AC:18, HP:12, TACTICS: SHORT SWORD: 3DMG.\n\n[' \
            'size=18sp][color=#229fed][u]6) Margrath, Duergar Captain[/u][/color][/size]\n[color=#1fed2d][EASY][' \
            '/color]: ' \
            'Same as Card.\n[color=#edde37][NORMAL][/color]: AC:17, HP:11, TACTICS: Same as Card.\n[color=#ff0000][' \
            'HARD][/color]: AC:18:, HP:14, TACTICS: MORNING STAR: 2DMG + EFF, QUILLS: 2DMG + EFF.\n\n[' \
            'size=18sp][color=#229fed][u]7) Otyugh[/u][/color][/size]\n[color=#1fed2d][EASY][' \
            '/color]: ' \
            'Same as Card.\n[color=#edde37][NORMAL][/color]: AC:15, HP: 14, TACTICS: Same as Card.\n[color=#ff0000][' \
            'HARD][/color]: AC:16, HP:17, TACTICS: TENTACLE: 2DMG + EFF.\n\n[size=22sp][b]The Legend of Drizzt[/b][/size]\n\n[size=18sp][color=#c138e7][b][u]1) Errtu, ' \
            'Balor[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: AC:14, HP:10, Tactics: Same as Card.\n[' \
            'color=#edde37][NORMAL][/color]: Same as Card.\n[color=#ff0000][HARD][/color]: AC:16, HP:25, ' \
            'Tactics: 1) SWORD: +10 + IMMOBILIZED, 2) WHIP: +9, 2DMG + EFFECT.\n[color=#ae0606][EXTREME][/color]: AC: 17, HP:28, TACTICS: 1) SWORD: +11 + IMMOBILIZED, 2) WHIP: +10, 2DMG + EFFECT.' \
            '\n\n[size=18sp][color=#c138e7][b][u]2) ' \
            'Shimmergloom, Shadow Dragon[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card\n[' \
            'color=#edde37][NORMAL][/color]: AC:15, HP: 20, TACTICS: 1) CLAWS: +9, 2DMG + EFFECT, 2) BREATH: +10.\n[' \
            'color=#ff0000][HARD][/color]: AC: 16, HP:23, TACTICS: 1) CLAWS: +10, 2DMG + EFFECT, 2) BREATH: +10, ' \
            '2 DMG + IMMOBILIZED.\n[color=#ae0606][EXTREME][/color]: AC: 16, HP:25, TACTICS: 1) CLAWS: +10, ' \
            '2DMG + EFFECT, 2) BREATH: +10, 2 DMG + IMMOBILIZED, PASSIVE: Whenever Shimmergloom defeats a hero, he gains a permanent +1 AC.\n\n[size=18sp][color=#c138e7][b][u]3) Yvonnel ' \
            'Baenre, Matron Mother[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]:Same as Card.\n[' \
            'color=#edde37][NORMAL][/color]:AC:14, HP:14, TACTICS:Same as Card.\n[color=#ff0000][HARD][/color]: ' \
            'AC:15, HP:22, TACTICS: 1) DAGGER: 2 + POISONED, 2) BLAST OF FIRE: 3 + EFFECT(MISS:1DMG).\n[' \
            'color=#ae0606][EXTREME][/color]: AC:15, HP:27, TACTICS: 1) DAGGER: 3+POISONED, 2) BLAST OF FIRE: ' \
            '3+EFFECT(MISS:1DMG).\n\n[size=18sp][color=#229fed][u]4) Yochlol, Handmaiden of Lolth[/u][' \
            '/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card.\n[color=#edde37][' \
            'NORMAL][/color]: AC: 14, HP: 18, TACTICS: 1) IF IT HAS 9 OR FEWER HP FLIP THE CARD.\n[color=#ff0000][HARD][/color]: AC: 15, HP: 22, TACTICS: 1) IF IT HAS 11 OR FEWER HP FLIP THE CARD\n\n[' \
            'size=18sp][color=#229fed][u]5) Methil El-Viddenvelp[/u][/color][/size]\n[color=#1fed2d][EASY][/color]: ' \
            'Same as Card.\n[color=#edde37][NORMAL][/color]: AC: 13, HP: 14.\n[color=#ff0000][' \
            'HARD][/color]: AC: 14, HP:20.\n\n[size=18sp][color=#229fed][u]6) Artemis Entreri[' \
            '/u][/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card.\n[color=#edde37][NORMAL][/color]: ' \
            'AC:16, HP: 14.\n[color=#ff0000][HARD][/color]: AC:16, HP: 21.\n\n[size=18sp][color=#229fed][u]7) Jarlaxe Baenre[/u][' \
            '/color][/size]\n[color=#1fed2d][EASY][/color]: Same as Card.\n[color=#edde37][NORMAL][/color]: AC: 16, ' \
            'HP: 14.\n[color=#ff0000][HARD][/color]: AC: 17, HP: 20.'
some_other_text = '[size=22sp][b]Waterdeep - Dungeon of the Mad Mage[/b][/size]\n\n[size=18sp][color=#c138e7][b][u]1) Zalthar Shadowdusk[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: AC: 16, HP: 12, TACTICS: 1) NINE LIVES STEALER: +8 , WEAKEN 2.\n[color=#edde37][NORMAL][/color]: AC: 17, HP: 18, TACTICS: 1)NINE LIVES STEALER: +9, WEAKEN 2.\n[color=#ff0000][HARD][/color]: Same as Card.\n[color=#ae0606][EXTREME][/color]: AC: 17, HP: 29, TACTICS: Same as Card.\n\n[size=18sp][color=#c138e7][b][u]2) Dezmyr Shadowdusk[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: AC:15, HP: 6, TACTICS: 1) DEATH TOUCH: 2DMG(1 MISS).\n[color=#edde37][NORMAL][/color]: AC:16, HP: 9, TACTICS: 1)DEATH TOUCH: 3DMG(1 MISS).\n[color=#ff0000][HARD][/color]: Same as Card.\n[color=#ae0606][EXTREME][/color]: AC: 16, HP: 15, TACTICS: Same as Card.\n\n[size=18sp][color=#c138e7][b][u]3) Arcturia[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: AC: 14, HP: 10, TACTICS: Remove 1st Tactic.\n[color=#edde37][NORMAL][/color]: AC: 15, HP: 17, TACTICS: Same as Card.\n[color=#ff0000][HARD][/color]: Same as Card.\n[color=#ae0606][EXTREME][/color]: AC: 16, HP: 26, TACTICS: SPURS +9\n\n[size=18sp][color=#c138e7][b][u]4) Halaster Blackcloak[/u][/b][/color][/size]\n[color=#1fed2d][EASY][/color]: AC: 13, HP: 12, TACTICS: Remove 1st and 2nd Tactic.\n[color=#edde37][NORMAL][/color]: AC 14, HP: 18, TACTICS: Remove 1st Tactic.\n[color=#ff0000][HARD][/color]: Same as Card.\n[color=#ae0606][EXTREME][/color]: AC: 15, HP: 27, TACTICS: Same as Card.\n\n[size=18sp][color=#229fed][u]5) Trobriand[/u][/color][/size]\n[color=#1fed2d][EASY][/color]: AC:12, HP: 11.\n[color=#edde37][NORMAL][/color]: Same as Card.\n[color=#ff0000][HARD][/color]: AC: 13, HP: 23, TACTICS: Same as Card. \n\n[size=18sp][color=#229fed][u]6) Muiral[/u][/color][/size]\n[color=#1fed2d][EASY][/color]: AC:13, HP:9.\n[color=#edde37][NORMAL][/color]: Same as Card.\n[color=#ff0000][HARD][/color]: AC: 14, HP: 19, TACTICS: Same as Card.\n\n[size=18sp][color=#229fed][u]7) Great Gray Ooze[/u][/color][/size]\n[color=#1fed2d][EASY][/color]: AC:15, HP: 10.\n[color=#edde37][NORMAL][/color]: Same as Card.\n[color=#ff0000][HARD][/color]: AC: 17, HP: 22, TACTICS: Same as Card.'
villain_grid = GridLayout(cols=2)
villain_label = Label(text=some_text,size_hint_y=None,markup=True,halign='left', valign='bottom')
villain_label.text_size = ((Window.width*.6)/2, None)
villain_label.texture_update()
villain_label.height = villain_label.texture_size[1]
villain_label_second = Label(text=some_other_text,size_hint_y=None,markup=True,halign='left', valign='bottom')
villain_label_second.text_size = ((Window.width*.6)/2, None)
villain_label_second.texture_update()
villain_label_second.height = villain_label_second.texture_size[1]
other_scroll = ScrollView()
other_scroll.add_widget(villain_label)
other_scroll_second = ScrollView()
other_scroll_second.add_widget(villain_label_second)
villain_grid.add_widget(other_scroll)
villain_grid.add_widget(other_scroll_second)
villain.content = villain_grid

#Choose Board games Pop-up
board_games = Popup(title='Select Board Games:', separator_color=[0, 100 / 255, 0, 1], size_hint=(.75, .75),title_align='center')
castle_raven = ToggleButton(text='Castle Ravenloft',background_color=(0,1,1,1))
wrath_ashard = ToggleButton(text='Wrath of Ashardalon',background_color=(0,1,1,1))
legend_drizzt = ToggleButton(text='The Legend of Drizzt',background_color=(0,1,1,1))
temple_evil = ToggleButton(text='Temple of Elemental Evil',background_color=(0,1,1,1))
tomb_an = ToggleButton(text='Tomb of Annihilation',background_color=(0,1,1,1),disabled=True)
mad_mage = ToggleButton(text='Waterdeep - Dungeon of the Mad Mage',background_color=(0,1,1,1))
grid_board = GridLayout(cols=1)
grid_second_board = GridLayout(cols=2,size=(board_games.width, board_games.height))
grid_second_board.add_widget(castle_raven)
grid_second_board.add_widget(wrath_ashard)
grid_second_board.add_widget(legend_drizzt)
grid_second_board.add_widget(temple_evil)
grid_second_board.add_widget(tomb_an)
grid_second_board.add_widget(mad_mage)
grid_board.add_widget(grid_second_board)
confirm_btn = Button(text='CONFIRM',font_size='18sp', background_color=(1,0,0,1),size_hint_y=.15)
grid_board.add_widget(confirm_btn)
board_games.content = grid_board

#Tools Pop-up
toolbox = Popup(title='Tools:', separator_color=[0, 100 / 255, 0, 1], size_hint=(.4, .4),title_align='center')
gridbig_tools = BoxLayout(orientation='vertical')
gridtools = GridLayout(cols=2)
toolbox.content = gridbig_tools

#Difficulty Pop-up
difficulty_sel = Popup(title='Select Difficulty:', separator_color=[0, 100 / 255, 0, 1], size_hint=(.4, .3),title_align='center')
grid_diff = GridLayout(cols=2)
normal_diff = Button(text='Normal',background_color=(0,1,1,1))
hard_diff = Button(text='Hard',background_color=(0,1,1,1))
grid_diff.add_widget(normal_diff)
grid_diff.add_widget(hard_diff)
difficulty_sel.content = grid_diff

#Load preferences
def load_preference():
    try:
        preferences = JsonStore('settings.json')
        check_music.active = preferences.get('music')['check']
        check_save.active = preferences.get('save')['check']
    except:
        pass
#Load
load_preference()


class MyUI(FloatLayout):

    def __init__(self, **kwargs):
        super(MyUI, self).__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, .6) # green; colors range from 0-1 instead of 0-255

            self.rect = Rectangle(size=self.size,
                                  pos=self.pos,source=backImages_list[0])
        self.bind(pos=self.update_rect, size=self.update_rect)
        # ActionBar
        self.menubar = ActionBar(pos_hint={'top': 1})
        self.menuview = ActionView()
        self.menubar.add_widget(self.menuview)
        self.menuAcPrevious = ActionPrevious(id='ap',with_previous=False,title='Dungeons And Dragons Campaign Generator',size_hint_x=None,width=0,app_icon_width=.1)
        # self.menuAcPrevious.bind(on_release=test)
        self.menuview.add_widget(self.menuAcPrevious)
        self.settings = ActionButton(text='Settings')
        self.menuview.add_widget(self.settings)
        self.villain_manual = ActionButton(text='Villains Manual')
        self.menuview.add_widget(self.villain_manual)
        self.help = ActionButton(text='Help')
        self.menuview.add_widget(self.help)
        self.add_widget(self.menubar)
        # self.menuAcPrevious.clear_widgets()


        # Labels/Texts
        self.add_widget(Label(text='Tavern', size_hint=(.1, .05), pos_hint={'x': 0, 'y': .85}))
        # self.tavern = TextInput(multiline=False, disabled=True, size_hint=(.16, .05), pos_hint={'x': .02, 'y': .80},
        #                         disabled_foreground_color=[1,1,1,1], background_disabled_normal='',
        #                         font_size='14sp',background_color=[0,0,0,0])
        self.tavern = Label(size_hint=(None, None),width=Window.width*.16,height=Window.height*.05, pos_hint={'x': .02, 'y': .8},font_size='14sp',valign='top')
        # self.tavern = Label(size_hint=(.1, .07), pos_hint={'x': .02, 'y': .8},font_size='14sp',valign='top')
        self.tavern.text_size = self.tavern.width, self.tavern.height
        self.add_widget(self.tavern)
        self.add_widget(Label(text='Heroes', size_hint=(.1, .05), pos_hint={'x': .15, 'y': .85}))
        # self.heroes = TextInput(multiline=True, size_hint=(.12, .3), pos_hint={'x': .15, 'y': .55}, disabled=True,
        #                         disabled_foreground_color=[1, 1, 1, 1], background_disabled_normal='',background_color=[0,0,0,0])
        self.heroes = Label(size_hint=(None, None), width=Window.width * .12, height=Window.height * .3,
                            pos_hint={'x': .15, 'y': .54}, font_size='15sp', valign='top')
        # self.heroes = Label(size_hint=(.1, .45), pos_hint={'x': .15, 'y': .54}, font_size='15sp', valign='top')
        self.heroes.text_size = self.heroes.width, self.heroes.height
        self.add_widget(self.heroes)
        self.add_widget(Label(text='Gold', size_hint=(.1, .05), pos_hint={'x': .36, 'y': .85}))
        self.gold = TextInput(multiline=True, size_hint=(.12, .26), pos_hint={'x': .36, 'y': .59}, input_filter='int',foreground_color=[1,1,1,1],background_color=[1,1,1,.1],font_size='15sp')
        self.add_widget(self.gold)
        self.add_widget(Label(text='LVL', size_hint=(.1, .05), pos_hint={'x': .23, 'y': .85}))
        # self.lvl = TextInput(multiline=True, size_hint=(.03, .3), pos_hint={'x': .26, 'y': .55}, input_filter='int',foreground_color=[1,1,1,1],background_color=[0,0,0,0],disabled=True,
        #                         disabled_foreground_color=[1, 1, 1, 1], background_disabled_normal='')
        self.lvl = Label(size_hint=(None, None), width=Window.width * .03, height=Window.height * .3,
                         pos_hint={'x': .26, 'y': .54}, valign='top', font_size='15sp')
        self.lvl.text_size = self.lvl.width, self.lvl.height
        self.add_widget(self.lvl)
        self.add_widget(Label(text='Items', size_hint=(.1, .05), pos_hint={'x': .48, 'y': .85}))
        self.itembox = TextInput(multiline=True, size_hint=(.12, .26), pos_hint={'x': .48, 'y': .59},foreground_color=[1,1,1,1],background_color=[1,1,1,.1],font_size='15sp')
        self.add_widget(self.itembox)
        self.add_widget(Label(text='Deck Changes', size_hint=(.1, .05), pos_hint={'x': .7, 'y': .85}))
        # self.deck_change = TextInput(multiline=True, size_hint=(.24, .45), pos_hint={'x': .64, 'y': .4},disabled=True,
        #                              disabled_foreground_color=[1, 1, 1, 1], background_disabled_normal='',
        #                              font_size='14sp',foreground_color=[1,1,1,1],background_color=[0,0,0,0])
        self.deck_change = Label(size_hint=(None, None), width=Window.width * .24, height=Window.height * .45,
                                 pos_hint={'x': .64, 'y': .4}, valign='top')
        self.deck_change.text_size = self.deck_change.width, self.deck_change.height
        self.add_widget(self.deck_change)
        self.add_widget(Label(text='Difficulty', size_hint=(.1, .05), pos_hint={'x': .88, 'y': .85}))
        # self.diff = TextInput(multiline=True, size_hint=(.05, .05), pos_hint={'x': .9, 'y': .78}, disabled=True,
        #                       disabled_foreground_color=[1, 1, 1, 1], background_disabled_normal='',foreground_color=[1,1,1,1],background_color=[0,0,0,0])
        self.diff = Label(size_hint=(None, None), width=Window.width * .05, height=Window.height * .05,
                         pos_hint={'x': .9, 'y': .79}, valign='top')
        self.diff.text_size = self.diff.width, self.diff.height
        self.add_widget(self.diff)
        self.add_widget(Label(text='Adventure No', size_hint=(.1, .05), pos_hint={'x': .02, 'y': .76}))
        # self.advno = TextInput(multiline=False, size_hint=(.05, .05), pos_hint={'x': .03, 'y': .71},disabled=True,
        #                        disabled_foreground_color=[1, 1, 1, 1], background_disabled_normal='',foreground_color=[1,1,1,1],background_color=[0,0,0,0])
        self.advno = Label(size_hint=(None, None), width=Window.width * .05, height=Window.height * .05,
                          pos_hint={'x': .03, 'y': .71}, valign='top')
        self.advno.text_size = self.advno.width, self.advno.height
        self.add_widget(self.advno)
        # self.advno.text = '1'
        # self.diff.text = '10'
        self.add_widget(
            Label(text='Adventure Case', size_hint=(.1, .05), pos_hint={'x': .1, 'y': .35}, font_size='14sp'))
        self.adv_case = Label(size_hint=(None, None), width=Window.width / 2, height=Window.height / 2.5,
                              pos_hint={'x': .05, 'y': .04}, font_size='18sp')

        self.adv_case.text_size = self.adv_case.width, self.adv_case.height - sp(10)
        self.add_widget(self.adv_case)
        self.add_widget(Label(text='Tiles', size_hint=(.1, .05), pos_hint={'x': .7, 'y': .35}))
        self.tiles = Label(size_hint=(None, None), width=Window.width / 2, height=Window.height / 3.8,
                              pos_hint={'x': .5, 'y': .15}, font_size='14sp')
        self.adv_case.text_size = self.adv_case.width, self.adv_case.height
        self.add_widget(self.tiles)


        # Buttons
        self.create = Button(text='Create Campaign', font_size='14sp', size_hint=(.15, .1),
                             pos_hint={'x': .2, 'y': .4}, background_color=[70/255,70/255,70/255,.8],background_normal='')
        self.add_widget(self.create)
        self.create.bind(on_release=difficulty_sel.open)
        self.next_adv = Button(text='Next Adventure', font_size='14sp', size_hint=(.15, .1),
                               pos_hint={'x': .45, 'y': .48}, background_normal='', background_color=[145/255, 23/255, 60/255, .8],
                               disabled=True)
        self.next_adv.bind(on_release=self.next_adventure)
        self.saving = Button(text='Save', font_size='14sp', size_hint=(.1, .07), pos_hint={'x': .03, 'y': .5},
                             background_color=[0, .2, 1,.7], disabled=True, background_normal='')
        self.add_widget(self.saving)
        self.saving.bind(on_release=self.save_state)
        self.loading = Button(text='Load', font_size='14sp', size_hint=(.1, .07), pos_hint={'x': .03, 'y': .42},
                              background_color=[0, .2, 1, .7], background_normal='')
        self.add_widget(self.loading)
        self.loading.bind(on_release=self.load_state)
        # Monster Tokens
        self.monster_tokens = Button(text='Monster Tokens', font_size='14sp', background_color=[.2, 1, .8, 1])
        gridtools.add_widget(self.monster_tokens)
        self.monster_tokens.bind(on_release=self.monster_tokens_menu)
        # toolbox.bind(on_dismiss=self.restore_tools)

        # PopUp Button
        self.help.bind(on_release=help.open)
        self.settings.bind(on_release=settings.open)
        self.villain_manual.bind(on_release=villain.open)
        #Toolbox open
        self.tools = Button(text='Tools', font_size='14sp', size_hint=(.15, .1),
                             pos_hint={'x': .45, 'y': .38}, background_color=[.5, 1, 1, 1])
        self.tools.bind(on_release=toolbox.open)
        # Roll-A-Die
        self.roll_die = Button(text='Roll D20', font_size='14sp',background_normal='images/d20.png', size_hint=(.15,
                                                                                                                .35),
                               background_down='images/d20.png', background_disabled_normal='images/d20.png',
                               disabled_color=(1,1,
                                                                                                                1,1))
        # gridtools.add_widget(self.roll_die)
        # self.add_widget(self.roll_die)
        self.roll_die.bind(on_release=self.rolling_die)
        # toolbox.bind(on_dismiss=self.restore_tools)

        # Level up button
        self.level_up = Button(text='LVL UP!', font_size='14sp',
                               background_color=[0, .2, 1, 1], background_normal='')
        gridtools.add_widget(self.level_up)
        self.level_up.bind(on_release=self.get_level)

        #Treasure Tokens button
        self.treasure_tokens_button = Button(text='Treasure Tokens', font_size='14sp',
                               background_color=[189/255, 178/255, 60/255, 1], background_normal='')
        gridtools.add_widget(self.treasure_tokens_button)
        self.treasure_tokens = ['100'] * 9 + ['200'] * 11 + ['300'] * 5 + ['400'] * 2 + ['treasure'] * 5 + ['500']
        shuffle(self.treasure_tokens)
        self.treasure_tokens_button.bind(on_release=self.treasure_tokens_menu)

        # Various Variables
        self.all_heroes = set()
        self.tilesets = set()
        self.specific_tiles = set()
        self.extra_tiles = set()
        self.items = set()
        self.villains_easy = set()
        self.villains_normal = set()
        self.villains_hard = set()
        self.bosses = set()
        self.defeated_boss = ''
        self.monster_types = set()

        normal_diff.bind(on_release=self.campaign_normal)
        hard_diff.bind(on_release=self.campaign_hard)
        gridbig_tools.add_widget(gridtools)
        gridbig_tools.add_widget(self.roll_die)

    def campaign_normal(self, instance):
        '''Here the compaign is created for the very first time- Normal Difficulty'''

        try:
            self.remove_widget(fireworks)
        except:
            pass
        # Get difficulty for campaign
        self.campaign_diff = 'normal'
        # Select board games before continuing
        board_games.open()
        confirm_btn.bind(on_release=self.check_board_active)

    def campaign_hard(self, instance):
        '''Here the compaign is created for the very first time- Hard Difficulty'''

        try:
            self.remove_widget(fireworks)
        except:
            pass
        #Get difficulty for campaign
        self.campaign_diff = 'hard'
        #Select board games before continuing
        board_games.open()
        confirm_btn.bind(on_release=self.check_board_active)

    def check_board_active(self, instance):
        if castle_raven.state == 'down' or wrath_ashard.state == 'down' or legend_drizzt.state == 'down' or temple_evil.state == 'down' or tomb_an.state == 'down' or mad_mage.state == 'down':
            self.campaign_two()

    def campaign_two(self):
        global CP_TAVERNS, PARTICIPANTS, ALLY, ALL_HEROES, SLAY_MONSTERS, SAVE_INNOCENT, RECLAIM_ITEM, DESTROY_ITEM, \
            SLAY_VILLAINS, SLAY_BOSSES, SLAY_MONSTERS_TXT, SAVE_INNOCENT_TXT, RECLAIM_ITEM_TXT, DESTROY_ITEM_TXT, \
            SLAY_VILLAINS_EASY_TXT, SLAY_VILLAINS_HARD_TXT, SAVE_ALLY_TXT, SPECIFIC_TILES, MAGE_SPECIFIC, \
            CAVERN_SPECIFIC, DRIZZT_SPECIFIC, EXTRA_TILES_DRIZZT, EXTRA_TILES_MAGE, EXTRA_TILES_CAVERN, CURRENT_ADV, \
            SAVE_ALLY, TOEE_SPECIFIC, EXTRA_TILES_TOEE, RAVENLOFT_SPECIFIC, EXTRA_TILES_RAVENLOFT

        difficulty_sel.dismiss()
        board_games.dismiss()
        self.saving.disabled = False
        self.setting_adv()
        self.defeated_boss = ''

        ALL_HEROES = list(self.all_heroes)
        ALL_HEROES.sort()

        # Clear Gold * Items
        self.gold.text = '0'
        self.itembox.text = 'None'
        # I will enable LOAD here later
        self.deck_change.text = 'You Begin with the combined Starter Deck of all the participating board games. Make two decks for treasure, one ' \
                                'with items and one with gold/fortunes. Each time you defeat a monster you draw from the gold/fortunes deck.'
        # Reseting
        self.advno.text = '1'
        self.diff.text = '1'
        # Tavern(s)
        tavern_names = ['Prancing Pony', 'Heroes\' Bar', 'Monster Fear', 'Little Bear', 'The Great Escape',
                        'Fear of the Dark', 'The Charming One', 'Pua\'s Bar', 'Nowhere', 'Asgard\'s Finest']
        shuffle(tavern_names)
        CP_TAVERNS = tavern_names[0:3:]
        # First tavern (Adventures 1-4)
        self.tavern.text = str(CP_TAVERNS[0])
        # Participants
        # ALL_HEROES = ['Drizzt', 'Catie-Brie', 'Bruenor', 'Wulfgar', 'Artemis', 'Athrogate', 'Jarlaxe', 'Regis', 'Atka',
        #                'Marcon', 'Cormac', 'Nayeli', 'Trosper']
        #Lets see if we can make players choose if they want to
        self.hero_buttons = []
        if self.num_boards == 5:
            self.another_grid = GridLayout(cols=5, size=(prompt_heroes.width, prompt_heroes.height))
        elif self.num_boards == 4:
            self.another_grid = GridLayout(cols=4, size=(prompt_heroes.width, prompt_heroes.height))
        elif self.num_boards == 3:
            self.another_grid = GridLayout(cols=3, size=(prompt_heroes.width, prompt_heroes.height))
        else:
            self.another_grid = GridLayout(cols=2,size=(prompt_heroes.width, prompt_heroes.height))
        for hero in range(len(ALL_HEROES)):
            btn = ToggleButton(text=ALL_HEROES[hero],background_color=(0,1,1,1))
            self.another_grid.add_widget(btn)
            self.hero_buttons.append(btn)
        # if len(self.hero_buttons) % 2 == 0:
        #     for i in range (2):
        #         prompt_heroes.content.add_widget(Label())
        # else:
        #     for i in range(3):
        #         prompt_heroes.content.add_widget(Label())
        self.dismiss_b = Button(text='CONFIRM',font_size='18sp', background_color=(1,0,0,1),size_hint_y=.15)
        prompt_heroes.content.add_widget(self.another_grid)
        prompt_heroes.content.add_widget(self.dismiss_b)
        prompt_heroes.open()
        for button in self.hero_buttons:
            button.bind(on_release=self.callback)
        self.dismiss_b.bind(on_release=self.campaign_three)

    def campaign_three(self,instance):
        global CP_TAVERNS, PARTICIPANTS, ALLY, ALL_HEROES, SLAY_MONSTERS, SAVE_INNOCENT, RECLAIM_ITEM, DESTROY_ITEM, \
            SLAY_VILLAINS, SLAY_BOSSES, SLAY_MONSTERS_TXT, SAVE_INNOCENT_TXT, RECLAIM_ITEM_TXT, DESTROY_ITEM_TXT, \
            SLAY_VILLAINS_EASY_TXT, SLAY_VILLAINS_HARD_TXT, SAVE_ALLY_TXT, SPECIFIC_TILES, MAGE_SPECIFIC, CAVERN_SPECIFIC, \
            DRIZZT_SPECIFIC, EXTRA_TILES_DRIZZT, EXTRA_TILES_MAGE, EXTRA_TILES_CAVERN, CURRENT_ADV, SAVE_ALLY, \
            ASHARDALON_SPECIFIC, CHAMBER_RANDOM_TXT, TOEE_SPECIFIC, EXTRA_TILES_TOEE, RAVENLOFT_SPECIFIC, \
            EXTRA_TILES_RAVENLOFT
        self.lvl.text = ''
        self.heroes.text = ''
        self.rect.source = backImages_list[0]
        try:
            self.add_widget(self.next_adv)
        except:
            pass
        self.next_adv.disabled = False
        try:
            self.add_widget(self.tools)
        except:
            pass
        PARTICIPANTS = []
        tilesets = list(self.tilesets)
        prompt_heroes.dismiss()
        for button in self.hero_buttons:
            if button.state == 'down':
                self.lvl.text += '1\n'
                PARTICIPANTS.append(button.text)
                self.heroes.text += (
                            button.text + '\n')
        self.heroes.text = self.heroes.text.rstrip('\n')
        if PARTICIPANTS == []:
            shuffle(ALL_HEROES)
            PARTICIPANTS = ALL_HEROES[0:4:]
            self.lvl.text = '1\n1\n1\n1\n'
            self.heroes.text = (PARTICIPANTS[0] + '\n' + PARTICIPANTS[1] + '\n' + PARTICIPANTS[2] + '\n' + PARTICIPANTS[3])
        #Clear buttons for heroes
        for btn in self.hero_buttons:
            prompt_heroes.content.remove_widget(self.another_grid)
        prompt_heroes.content.remove_widget(self.dismiss_b)
        del self.hero_buttons
        # Adventures 1-4 and 5-9 won't use cavern tiles and on adventures 10-13 we exchange dungeon tiles with cavern ones
        shuffle(tilesets)
        # We need to use certain triggers for changing tilesets inbetween
        trigger_change = randrange(4, 9)
        # print (trigger_change)
        # if len(tilesets) == 1:
        self.tiles.text = (tilesets[0])
        # Get antihero list
        self.antihero = []
        if legend_drizzt.state == 'down':
            self.antihero = [x for x in ['Artemis', 'Jarlaxe'] if x not in PARTICIPANTS]
        if self.campaign_diff == 'normal':
            SLAY_VILLAINS += [x + ' [EASY]' for x in self.antihero]
        elif self.campaign_diff == 'hard':
            SLAY_VILLAINS += [x + ' [NORMAL]' for x in self.antihero]
        # Cases Sector
        SAVE_ALLY = [x for x in ALL_HEROES if x not in PARTICIPANTS and x not in self.antihero]
        adv_types = ['CHAMBER_RANDOM', SLAY_MONSTERS, SAVE_INNOCENT, SAVE_ALLY, RECLAIM_ITEM, DESTROY_ITEM, SLAY_VILLAINS,
                     SLAY_BOSSES]
        if wrath_ashard.state == 'normal':
            adv_types.remove('CHAMBER_RANDOM')
        CURRENT_ADV = choice(adv_types[:-1:])
        # Set specific dungeon tiles if specific adv type
        if CURRENT_ADV == 'CHAMBER_RANDOM':
            self.tiles.text = 'Dungeon (Ashardalon)'

        CHAMBER_RANDOM_TXT = ['Who knows what will this adventure unveil? Draw a chamber card when you reveal the '
                              'trigger tile!']
        SLAY_MONSTERS_TXT = ['You find yourself once again in the ' + self.tavern.text + ' tavern. The barkeeper '
                                                                                         'seems to have a quest for you. You ask him what the quest is. He whispers to you that he wants you to slay ' + str(
            randrange(3, 6)) + ' ' + str(choice(SLAY_MONSTERS)),
                             'There is only one path left to advance, but it seems that it is currently crowded by lots of monsters. If you want to proceed, you need to slay ' + str(
                                 randrange(3, 6)) + ' ' + str(choice(SLAY_MONSTERS)),
                             'The night has come but the heroes cannot sleep.'
                             ' The screams of monsters in the dungeon has kept them awake. They must clean things up. Slay ' + str(
                                 randrange(3, 6)) + ' ' + str(choice(SLAY_MONSTERS))]

        SAVE_INNOCENT_TXT = ['Things are bad! you just learned that a certain individual named ' + choice(
            SAVE_INNOCENT) + ' has gone missing. There is no time to lose, you hurry on to the rescue!', 'On your '
                                                                                                         'way to the tavern you hear a woman shouting! Her child has gone missing! You rush to the rescue. Rescue ' + choice(
            SAVE_INNOCENT)]
        self.current_item_choice = choice(RECLAIM_ITEM)
        RECLAIM_ITEM_TXT = [
            'You just learned of the existance of the ' + self.current_item_choice + ' item. You need to get'
                                                                                     ' your hands on it, since it will help you on your quest.',
            'Back on the ' + self.tavern.text + ' you take notice on some bounties. There is a very interesting one which would give ' + str(
                choice([900, 1200,
                        1500])) + ' Gold to whoever retrieves the ' + self.current_item_choice + '. You decide to '
                                                                                              'investigate for the specific item. You can either keep the item at the end of this adventure, or give it to receive the gold.',
            'Rumors have it that a legendary item is hidden deep in the dungeon. It was owned hundreds of years ago by kings of old. ' + str(
                choice(
                    PARTICIPANTS)) + ' is so interested in ' + self.current_item_choice + ' and urges all of the heroes to the search of the item.']

        self.destroy_item_choice = choice(DESTROY_ITEM)
        DESTROY_ITEM_TXT = ['You get informed that a certain item deep in the dungeon corrupts everything it touches!'
                            ' Destroy ' + self.destroy_item_choice + ' before it is too late.',
                            'The air feels heavier... Each step that the heroes take feels even heavier... ' +
                            choice(
                                PARTICIPANTS) + ' tells everyone that this is because of the ' + self.destroy_item_choice + ' item, which corrupted this land. The choice is clear, you need to destroy it.']

        self.slay_villain_choice = choice(SLAY_VILLAINS)
        SLAY_VILLAINS_EASY_TXT = [
            'There is one thing standing before you and the rest of your quest. ' + self.slay_villain_choice + '! Kill the villain(s)!',
            self.slay_villain_choice + ' appear(s) to be in charge of many monsters in the dungeon. Eliminating it/them means that the heroes can roam a bit more freely on the dungeon.']

        SLAY_VILLAINS_HARD_TXT = ['An ultimate test for your party! Kill ' + choice(SLAY_BOSSES),
                                  'The time has finally come to confront ' + choice(
                                      SLAY_BOSSES) + '. Ready or not here the heroes go!']

        SAVE_ALLY_TXT = ['Your fellow companion has been imprisoned! You must free your '
                         'companion at once!']
        ALLY = None
        # Specific Tiles
        # if len(tilesets) == 1:
        # if len(tilesets) == 1:
        if tilesets[0] == 'Dungeon (Mad Mage) / Cavern (Mad Mage)':
            trigger_tile = choice(MAGE_SPECIFIC)
            extra_trigger_tile = choice(EXTRA_TILES_MAGE)
        elif tilesets[0] == 'Cavern (Drizzt)':
            trigger_tile = choice(DRIZZT_SPECIFIC)
            extra_trigger_tile = choice(EXTRA_TILES_DRIZZT)
        elif tilesets[0] == 'Dungeon (Ashardalon)':
            trigger_tile = choice(ASHARDALON_SPECIFIC)
            extra_trigger_tile = ''
        elif tilesets[0] == 'Dungeon (Castle Ravenloft)':
            trigger_tile = choice(RAVENLOFT_SPECIFIC)
            extra_trigger_tile = choice(EXTRA_TILES_RAVENLOFT)
        elif tilesets[0] == 'Dungeon (ToEE)':
            if self.slay_villain_choice.startswith('Fire Elemental (Villain)'):
                trigger_tile = 'Fire Altar'
            elif self.slay_villain_choice.startswith('Water Elemental (Villain)'):
                trigger_tile = 'Water Altar'
            elif self.slay_villain_choice.startswith('Earth Elemental (Villain)'):
                trigger_tile = 'Earth Altar'
            elif self.slay_villain_choice.startswith('Air Elemental (Villain)'):
                trigger_tile = 'Air Altar'
            else:
                trigger_tile = choice(TOEE_SPECIFIC)
            if trigger_tile == 'Fire Altar':
                extra_trigger_tile = 'Elemental Fire Node'
            elif trigger_tile == 'Water Altar':
                extra_trigger_tile = 'Elemental Water Node'
            elif trigger_tile == 'Earth Altar':
                extra_trigger_tile = 'Elemental Earth Node'
            elif trigger_tile == 'Air Altar':
                extra_trigger_tile = 'Elemental Air Node'
            else:
                extra_trigger_tile = choice(EXTRA_TILES_TOEE)

        if CURRENT_ADV == 'CHAMBER_RANDOM':
            trigger_tile = choice(ASHARDALON_SPECIFIC)
            extra_trigger_tile = ''
            self.adv_case.text = ('???' + '\n')
            self.adv_case.text += (choice(CHAMBER_RANDOM_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
        if CURRENT_ADV == SLAY_MONSTERS:
            self.adv_case.text = ('SLAY MONSTERS' + '\n')
            self.adv_case.text += (choice(SLAY_MONSTERS_TXT))
        elif CURRENT_ADV == SAVE_INNOCENT:
            self.adv_case.text = ('SAVE VILLAGER' + '\n')
            self.adv_case.text += (choice(SAVE_INNOCENT_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile)
        elif CURRENT_ADV == SAVE_ALLY:
            self.adv_case.text = ('RESCUE ALLY' + '\n')
            ALLY = choice(SAVE_ALLY)
            self.adv_case.text += (choice(SAVE_ALLY_TXT) + '\n')
            self.adv_case.text += ('Rescue ' + ALLY + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)
            try:
                ALL_HEROES.remove(ALLY)  # print(ALL_HEROES)
            except:
                pass
        elif CURRENT_ADV == RECLAIM_ITEM:
            self.adv_case.text = ('RECLAIM ITEM' + '\n')
            self.adv_case.text += (choice(RECLAIM_ITEM_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)
            RECLAIM_ITEM.remove(self.current_item_choice)
        elif CURRENT_ADV == DESTROY_ITEM:
            self.adv_case.text = ('DESTROY ITEM' + '\n')
            self.adv_case.text += (choice(DESTROY_ITEM_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '. Place after the 10th tile.' + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)
            DESTROY_ITEM.remove(self.destroy_item_choice)
        elif CURRENT_ADV == SLAY_VILLAINS:
            self.adv_case.text = ('DEFEAT VILLAIN(S)' + '\n')
            self.adv_case.text += (choice(SLAY_VILLAINS_EASY_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile)
            SLAY_VILLAINS.remove(self.slay_villain_choice)
        elif CURRENT_ADV == SLAY_BOSSES:
            self.adv_case.text = ('DEFEAT BOSS' + '\n')
            self.adv_case.text += (choice(SLAY_VILLAINS_HARD_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)

        # Check for autosave:
        if check_save.active:
            self.save_state(instance)

    def next_adventure(self, instance):

        global CP_TAVERNS, PARTICIPANTS, ALLY, ALL_HEROES, SLAY_MONSTERS, SAVE_INNOCENT, RECLAIM_ITEM, DESTROY_ITEM, \
            SLAY_VILLAINS, SLAY_BOSSES, SLAY_MONSTERS_TXT, SAVE_INNOCENT_TXT, RECLAIM_ITEM_TXT, DESTROY_ITEM_TXT,\
            SLAY_VILLAINS_EASY_TXT, SLAY_VILLAINS_HARD_TXT, CURRENT_ADV, SAVE_ALLY, BOSS, ASHARDALON_SPECIFIC, \
            CHAMBER_RANDOM_TXT

        # Get the chosen difficulty
        if self.campaign_diff == 'normal':
            if self.advno.text == '5':
                SLAY_VILLAINS = list(self.villains_normal)
                SLAY_VILLAINS += [x + ' [NORMAL]' for x in self.antihero if x not in PARTICIPANTS]
        elif self.campaign_diff == 'hard':
            if self.advno.text == '5':
                SLAY_VILLAINS = list(self.villains_hard)
                SLAY_VILLAINS += [x + ' [HARD]' for x in self.antihero if x not in PARTICIPANTS]
        BOSS = ''
        # Check if the campaign is over
        if self.advno.text == '13':
            self.adv_case.text = ('-- THE CAMPAIGN IS OVER! CONGRATULATIONS!!! --')
            self.does_fireworks()
            self.next_adv.disabled = True
            self.remove_widget(self.next_adv)
            self.remove_widget(self.tools)
            return

        # Win Sound
        if win_sound:
            if check_music.active:
                win_sound.loop = False
                win_sound.volume = .5
                win_sound.play()

        # Check for defeated boss
        if (self.advno.text == '5') or (self.advno.text == '9') or (self.advno.text == '13'):
            try:
                SLAY_BOSSES.remove(self.defeated_boss)
                self.defeated_boss = ''
                print(SLAY_BOSSES)
            except:
                pass
        self.adv_case.text = ''
        # Add Difficulty text to bosses
        if self.campaign_diff == 'normal':
            if self.advno.text == '1':
                SLAY_BOSSES = [villain + ' [EASY]' for villain in SLAY_BOSSES]
            if self.advno.text == '5':
                SLAY_BOSSES = [villain.replace('[EASY]', ' [NORMAL]') for villain in SLAY_BOSSES]
            if self.advno.text == '9':
                SLAY_BOSSES = [villain.replace('[NORMAL]', ' [HARD]') for villain in SLAY_BOSSES]
        if self.campaign_diff == 'hard':
            if self.advno.text == '1':
                SLAY_BOSSES = [villain + ' [NORMAL]' for villain in SLAY_BOSSES]
            if self.advno.text == '5':
                SLAY_BOSSES = [villain.replace('[NORMAL]', ' [HARD]') for villain in SLAY_BOSSES]
            if self.advno.text == '9':
                SLAY_BOSSES = [villain.replace('[HARD]', ' [EXTREME]') for villain in SLAY_BOSSES]
        # Getting new list of heroes in case of a rescue
        if ALLY != None:
            PARTICIPANTS.append(ALLY)
            self.heroes.text += ('\n' + ALLY)
            self.lvl.text += '1\n'
        ALLY = None
        # Get new ally if you defeated an anti-hero
        if self.slay_villain_choice in ['Artemis [EASY]', 'Athrogate [EASY]', 'Jarlaxe [EASY]', 'Artemis [NORMAL]',
                                     'Athrogate [NORMAL]', 'Jarlaxe [NORMAL]', 'Artemis [HARD]', 'Athrogate [HARD]',
                                     'Jarlaxe [HARD]'] and CURRENT_ADV == SLAY_VILLAINS:
            self.slay_villain_choice = self.slay_villain_choice.replace(' [EASY]', '')
            self.slay_villain_choice = self.slay_villain_choice.replace(' [NORMAL]', '')
            self.slay_villain_choice = self.slay_villain_choice.replace(' [HARD]', '')
            PARTICIPANTS.append(self.slay_villain_choice)
            self.heroes.text += ('\n' + self.slay_villain_choice)
            self.lvl.text += '1\n'
        # Getting new Adventure Number and Difficulty Increases
        self.advno.text = str(int(self.advno.text) + 1)
        if self.campaign_diff == 'normal':
            the_step = choice((0, 1, 1, 1, 1, 2))
        if self.campaign_diff == 'hard':
            the_step = choice((1, 1, 2, 2, 2, 3))
        self.diff.text = str(int(self.diff.text) + (the_step))
        # Deck Changes according to the difficulty change
        if the_step == 0:
            self.deck_change.text = '1) Switch 1 copper coin card for a silver one'
        else:
            self.deck_change.text = '1) Remove {0} monster(s) from the basic deck and add {0} from the advanced one.\n' \
                                    '2) Remove {0} monster card(s) which {2} bring monsters.\n' \
                                    '3) Switch {5} copper coin card(s) for {5} silver coin card(s)\n' \
                                    '4) Remove {0} encounter(s) from the basic deck and add {0} from the advanced one.\n' \
                                    '5) Remove {1} encounter(s) which {3} nothing.\n' \
                                    '6) Remove {1} trap(s) from the basic deck and add {1} from the advanced one.\n' \
                                    '7) Switch {4} copper coin card(s) for {4} gold coin card(s).'.format(the_step*self.num_boards,(the_step-1)*self.num_boards, 'doesn\'t' if the_step*self.num_boards == 1 else 'don\'t', 'does' if (the_step-1)*self.num_boards == 1 else 'do', 1 if (the_step == 2 ) else 0, the_step)
        # Set new Tavern if needed
        if self.advno.text == '5':
            self.tavern.text = CP_TAVERNS[1]
            self.rect.source = backImages_list[1]
        elif self.advno.text == '10':
            self.tavern.text = CP_TAVERNS[2]
            self.rect.source = backImages_list[2]
        # Same part as Campaign
        # Tilesets
        tilesets = list(self.tilesets)
        shuffle(tilesets)
        # We need to use certain triggers for changing tilesets inbetween
        trigger_change = randrange(4, 9)
        # print (trigger_change)
        # if len(tilesets) == 1:
        self.tiles.text = (tilesets[0])
        # else:
        #     self.tiles.text = (
        #                 tilesets[0] + '\nchange to\n' + tilesets[1] + '\nafter ' + str(trigger_change) + '\ntiles')
        # Cases Sector
        SAVE_ALLY = [x for x in ALL_HEROES if x not in PARTICIPANTS and x not in self.antihero]
        try:
            ALL_HEROES.remove(ALLY)
        except:
            pass
        # print (save_ally)
        adv_types = ['CHAMBER_RANDOM', SLAY_MONSTERS, SAVE_INNOCENT, SAVE_ALLY, RECLAIM_ITEM, DESTROY_ITEM, SLAY_VILLAINS,
                     SLAY_BOSSES]
        if wrath_ashard.state == 'normal':
            adv_types.remove('CHAMBER_RANDOM')
        if not SAVE_ALLY:
            adv_types.remove(SAVE_ALLY)
        if not RECLAIM_ITEM:
            adv_types.remove(RECLAIM_ITEM)
        if not DESTROY_ITEM:
            adv_types.remove(DESTROY_ITEM)
        if not SLAY_VILLAINS:
            adv_types.remove(SLAY_VILLAINS)
        if self.advno.text == '5' or self.advno.text == '9' or self.advno.text == '13':
            BOSS = choice(SLAY_BOSSES)
            self.defeated_boss = BOSS
            CURRENT_ADV = adv_types[-1]
        else:
            CURRENT_ADV = choice(adv_types[:-1:])
        # Set specific dungeon tiles if specific adv type
        if CURRENT_ADV == 'CHAMBER_RANDOM':
            self.tiles.text = 'Dungeon (Ashardalon)'

        # Cases Texts Templates
        CHAMBER_RANDOM_TXT = ['Who knows what will this adventure unveil? Draw a chamber card when you reveal the '
                              'trigger tile!']
        SLAY_MONSTERS_TXT = ['You find yourself once again in the ' + self.tavern.text + ' tavern. The barkeeper '
                                                                                         'seems to have a quest for you. You ask him what the quest is. He whispers to you that he wants you to '
                                                                                         'slay ' + str(
            randrange(3, 6)) + ' ' + str(choice(SLAY_MONSTERS)), 'The night has come but the heroes cannot sleep.'
                                                                 ' The screams of monsters in the dungeon has kept them awake. They must clean things up. Slay ' + str(
            randrange(3, 6)) + ' ' + str(choice(SLAY_MONSTERS)),
                             'There is only one path left to advance, but it seems that it is currently crowded by lots of monsters. If you want to proceed, slay ' + str(
                                 randrange(3, 6)) + ' ' + str(choice(SLAY_MONSTERS))]

        SAVE_INNOCENT_TXT = ['Things are bad! you just learned that a certain individual named ' + choice(SAVE_INNOCENT)
                             + ' has gone missing. There is no time to lose, you hurry on to the rescue!',
                             'On your way to the tavern'
                             ' you hear a woman shouting! Her child has gone missing! You rush to the rescue. Rescue ' + choice(
                                 SAVE_INNOCENT),
                             'One cannot even enjoy a fine beer after an exhausting adventure! Well, it is because the barkeeper is MIA since he went to search for something in the dungeon. It seems that it falls to you to rescue him.']

        try:
            self.current_item_choice = choice(RECLAIM_ITEM)
        except:
            self.current_item_choice = ''
        try:
            self.destroy_item_choice = choice(DESTROY_ITEM)
        except:
            self.destroy_item_choice = ''
        try:
            self.slay_villain_choice = choice(SLAY_VILLAINS)
        except:
            self.slay_villain_choice = ''

        RECLAIM_ITEM_TXT = [
            'You just learned of the existance of the ' + self.current_item_choice + ' item. You need to get'
                                                                                     ' your hands on it, since it will help you on your quest.',
            'Back on the ' + self.tavern.text + ' you take notice on some bounties. There is a very interesting one which would give ' + str(
                choice([
                    900, 1200,
                    1500])) + ' Gold to whoever retrieves the ' + self.current_item_choice + '. You decide to '
                                                                                          'investigate for the specific item. You can either keep the item at the end of this adventure, or give it to receive the gold.',
            'Rumors have it that a legendary item is hidden deep in the dungeon. It was owned hundreds of years ago by kings of old. ' + str(
                choice(
                    PARTICIPANTS)) + ' is so interested in ' + self.current_item_choice + ' and urges all of the heroes to the search of the item.']

        DESTROY_ITEM_TXT = ['You get informed that a certain item deep in the dungeon corrupts everything it touches!'
                            ' Destroy ' + self.destroy_item_choice + ' before it is too late.',
                            'The air feels heavier... Each step that the heroes take feels even heavier... ' +
                            choice(
                                PARTICIPANTS) + ' tells everyone that this is because of the ' + self.destroy_item_choice + ' item, which corrupted this land. The choice is clear, you need to destroy it.']
        SLAY_VILLAINS_EASY_TXT = [
            'There is one thing standing before you and the rest of your quest. ' + self.slay_villain_choice + '! Kill the villain(s)!',
            self.slay_villain_choice + ' appear(s) to be in charge of many monsters in the dungeon. Eliminating it/them means that the heroes can roam a bit more freely on the dungeon.']
        SLAY_VILLAINS_HARD_TXT = ['An ultimate test for your party! Kill ' + BOSS,
                                  'The time has finally come to confront ' + BOSS + '. Ready or not here the heroes go!']

        SAVE_ALLY_TXT = ['Your fellow companion has been imprisoned! You must free your '
                         'companion at once!']
        # Specific Tiles
        # if len(tilesets) == 1:
        if tilesets[0] == 'Dungeon (Mad Mage) / Cavern (Mad Mage)':
            extra_trigger_tile = choice(EXTRA_TILES_MAGE)
            if int(self.advno.text) < 10:
                trigger_tile = choice(MAGE_SPECIFIC)
            else:
                trigger_tile = choice(CAVERN_SPECIFIC)
        elif tilesets[0] == 'Cavern (Drizzt)':
            trigger_tile = choice(DRIZZT_SPECIFIC)
            extra_trigger_tile = choice(EXTRA_TILES_DRIZZT)
        elif tilesets[0] == 'Dungeon (Ashardalon)':
            trigger_tile = choice(ASHARDALON_SPECIFIC)
            extra_trigger_tile = ''
        elif tilesets[0] == 'Dungeon (Castle Ravenloft)':
            trigger_tile = choice(RAVENLOFT_SPECIFIC)
            extra_trigger_tile = choice(EXTRA_TILES_RAVENLOFT)
        elif tilesets[0] == 'Dungeon (ToEE)':
            if self.slay_villain_choice.startswith('Fire Elemental (Villain)') and CURRENT_ADV == SLAY_VILLAINS:
                trigger_tile = 'Fire Altar'
            elif self.slay_villain_choice.startswith('Water Elemental (Villain)') and CURRENT_ADV == SLAY_VILLAINS:
                trigger_tile = 'Water Altar'
            elif self.slay_villain_choice.startswith('Earth Elemental (Villain)') and CURRENT_ADV == SLAY_VILLAINS:
                trigger_tile = 'Earth Altar'
            elif self.slay_villain_choice.startswith('Air Elemental (Villain)') and CURRENT_ADV == SLAY_VILLAINS:
                trigger_tile = 'Air Altar'
            else:
                trigger_tile = choice(TOEE_SPECIFIC)
            if trigger_tile == 'Fire Altar':
                extra_trigger_tile = 'Elemental Fire Node'
            elif trigger_tile == 'Water Altar':
                extra_trigger_tile = 'Elemental Water Node'
            elif trigger_tile == 'Earth Altar':
                extra_trigger_tile = 'Elemental Earth Node'
            elif trigger_tile == 'Air Altar':
                extra_trigger_tile = 'Elemental Air Node'
            else:
                extra_trigger_tile = choice(EXTRA_TILES_TOEE)

        if CURRENT_ADV == 'CHAMBER_RANDOM':
            trigger_tile = choice(ASHARDALON_SPECIFIC)
            extra_trigger_tile = ''
            self.adv_case.text = ('???' + '\n')
            self.adv_case.text += (choice(CHAMBER_RANDOM_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
        if CURRENT_ADV == SLAY_MONSTERS:
            self.adv_case.text = ('SLAY MONSTERS' + '\n')
            self.adv_case.text += (choice(SLAY_MONSTERS_TXT))
        elif CURRENT_ADV == SAVE_INNOCENT:
            self.adv_case.text = ('SAVE VILLAGER' + '\n')
            self.adv_case.text += (choice(SAVE_INNOCENT_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile)
        elif CURRENT_ADV == SAVE_ALLY:
            self.adv_case.text = ('RESCUE ALLY' + '\n')
            ALLY = choice(SAVE_ALLY)
            self.adv_case.text += (choice(SAVE_ALLY_TXT) + '\n')
            self.adv_case.text += ('Rescue ' + ALLY + '\n')
            # PARTICIPANTS.append(ALLY)
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)
            try:
                ALL_HEROES.remove(ALLY)
            except:
                pass
        elif CURRENT_ADV == RECLAIM_ITEM:
            self.adv_case.text = ('RECLAIM ITEM' + '\n')
            self.adv_case.text += (choice(RECLAIM_ITEM_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)
            RECLAIM_ITEM.remove(self.current_item_choice)
        elif CURRENT_ADV == DESTROY_ITEM:
            self.adv_case.text = ('DESTROY ITEM' + '\n')
            self.adv_case.text += (choice(DESTROY_ITEM_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '. Place after the 10th tile.' + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)
            DESTROY_ITEM.remove(self.destroy_item_choice)
        elif CURRENT_ADV == SLAY_VILLAINS:
            self.adv_case.text = ('DEFEAT VILLAIN(S)' + '\n')
            self.adv_case.text += (choice(SLAY_VILLAINS_EASY_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile)
            SLAY_VILLAINS.remove(self.slay_villain_choice)
        elif CURRENT_ADV == SLAY_BOSSES:
            self.adv_case.text = ('DEFEAT BOSS' + '\n')
            self.adv_case.text += (choice(SLAY_VILLAINS_HARD_TXT) + '\n')
            self.adv_case.text += ('Trigger Tile: ' + trigger_tile + '\n')
            self.adv_case.text += ('Extra Trigger Tile: ' + extra_trigger_tile)

        # Check for autosave:
        if check_save.active:
            self.save_state(instance)


    def setting_adv(self):

        global CAVERN_SPECIFIC, MAGE_SPECIFIC, DRIZZT_SPECIFIC, EXTRA_TILES_DRIZZT, EXTRA_TILES_MAGE, SLAY_MONSTERS, \
            SAVE_INNOCENT, SAVE_ALLY, RECLAIM_ITEM, DESTROY_ITEM, SLAY_VILLAINS, SLAY_BOSSES, ASHARDALON_SPECIFIC, \
            TOEE_SPECIFIC, EXTRA_TILES_TOEE, RAVENLOFT_SPECIFIC, EXTRA_TILES_RAVENLOFT
        self.all_heroes.clear()
        self.tilesets.clear()
        self.items.clear()
        self.villains_easy.clear()
        self.villains_normal.clear()
        self.villains_hard.clear()
        self.bosses.clear()
        self.monster_types.clear()
        # ----- Drizzt Variables Start here ------
        if legend_drizzt.state == 'down':
            # Check if Drizzt Board Game is enabled so we enable certain sets
            self.all_heroes.update(
                ['Drizzt', 'Catie-Brie', 'Bruenor', 'Wulfgar', 'Artemis', 'Athrogate', 'Jarlaxe', 'Regis'])
            self.tilesets.update(['Cavern (Drizzt)'])
            self.items.update(['Cat\'s Eye Headband', 'Belt of Storm Giant Strength', 'Bracers of the Blinding Strike',
                               'Wand of Magic Missiles', 'Necklace of Speed'])
            self.villains_easy.update(
                ['2 Feral Trolls', 'Dinin Do\'Urden and Feral Troll', 'Yochlol, Handmaiden of Lolth [EASY]'
                    , 'Methil El-Viddenvelp [EASY]'])
            self.villains_normal.update(
                ['2 Feral Trolls and Dinin Do\'Urden', 'Yochlol, Handmaiden of Lolth [NORMAL]',
                 'Methil El-Viddenvelp [NORMAL]'])
            self.villains_hard.update(['Yochlol, Handmaiden of Lolth [HARD]', 'Methil El-Viddenvelp [HARD]'])
            self.bosses.update(['Errtu, Balor', 'Yvonnel Baenre, Matron Mother','Shimmergloom, Shadow Dragon'])
            self.monster_types.update(['Goblin', 'Drow-Humanoid'])

        # ----- Mad Mage Variables Start here ------
        if mad_mage.state == 'down':
            # Check if Mad Mage Board Game is enabled so we enable certain sets
            self.all_heroes.update(['Atka', 'Marcon', 'Cormac', 'Nayeli', 'Trosper'])
            self.tilesets.update(['Dungeon (Mad Mage) / Cavern (Mad Mage)'])
            self.items.update(['Scaladar Control Ring (Mad Mage)', 'Zalthar\'s Nine Lives Stealer (Mad Mage)'])
            self.villains_easy.update(
                ['Death Tyrant', '2 Zombie Beholders', 'Scaladar', 'The False Halaster', 'Muiral [EASY]',
                 'Great Gray Ooze [EASY]','Trobriand [EASY]'])
            self.villains_normal.update(
                ['Death Tyrant and 2 Zombie Beholders', 'Scaladar and The False Halaster', 'Muiral [NORMAL]',
                 'Great Gray Ooze [NORMAL]','Trobriand [NORMAL]'])
            self.villains_hard.update(
                ['Muiral [HARD]', 'Great Gray Ooze [HARD]', 'Death Tyrant, 2 Zombie Beholders and Scaladar',
                 'Trobriand [HARD]'])
            self.bosses.update(['Zalthar Shadowdusk and Dezmyr Shadowdusk', 'Arcturia', 'Halaster Blackcloak'])
            self.monster_types.update(['Human', 'Undead'])

        # ----- Wrath of Ashardalon Variables Start here ------
        if wrath_ashard.state == 'down':
            # Check if Wrath of Ashardalon Board Game is enabled so we enable certain sets
            self.all_heroes.update(['Vistra', 'Keyleth', 'Tarak', 'Quinn', 'Heskan'])
            self.tilesets.update(['Dungeon (Ashardalon)'])
            self.items.update(['Pearl of Power', 'Vorpal Sword', 'Gauntlets of Ogre Power', 'Ring of Shooting Stars',
            'Blessed Shield', 'Throwing Shield'])
            self.villains_easy.update(['Margrath, Duergar Captain [EASY]', 'Otyugh [EASY]', 'Kraash, '
            'Orc Storm Shaman [EASY]', 'Meerak, Kobold Dragonlord [EASY]'])
            self.villains_normal.update(['Margrath, Duergar Captain [NORMAL]', 'Otyugh [NORMAL]', 'Kraash, '
            'Orc Storm Shaman [NORMAL]', 'Meerak, Kobold Dragonlord [NORMAL]'])
            self.villains_hard.update(['Margrath, Duergar Captain [HARD]', 'Otyugh [HARD]', 'Kraash, '
            'Orc Storm Shaman [HARD]', 'Meerak, Kobold Dragonlord [HARD]'])
            self.bosses.update(['Ashardalon, Red Dragon', 'Bellax, Gauth', 'Rage Drake'])
            self.monster_types.update(['Orc', 'Reptile'])

        # ----- TOEE Variables Start here ------
        if temple_evil.state == 'down':
            # Check if TOEE Board Game is enabled so we enable certain sets
            self.all_heroes.update(['Talon', 'Nymmestra', 'Barrowin', 'Ratshadow', 'Alaeros'])
            self.tilesets.update(['Dungeon (ToEE)'])
            self.items.update(['Cloak of Protection', 'Flame Tongue', 'Frost Brand', 'Horn of Blasting'])
            self.villains_easy.update(
                ['Water Elemental (Villain)[EASY]', 'Air Elemental (Villain)[EASY]', 'Fire Elemental (Villain)'\
                '[EASY]', 'Earth Elemental (Villain)[EASY]'])
            self.villains_normal.update(
                ['Water Elemental (Villain)[NORMAL]', 'Air Elemental (Villain)[NORMAL]', 'Fire Elemental (Villain)'\
                '[NORMAL]', 'Earth Elemental (Villain)[NORMAL]'])
            self.villains_hard.update(
                ['Water Elemental (Villain)[HARD]', 'Air Elemental (Villain)[HARD]', 'Fire Elemental (Villain)'\
                '[HARD]', 'Earth Elemental (Villain)[HARD]'])
            self.bosses.update(['Velathidros, Black Dragon', 'Swerglemergle, Ettin', 'Arkaschic Thunn, Salamander'])
            self.monster_types.update(['Human', 'Elemental'])

        # ----- Ravenloft Variables Start here ------
        if castle_raven.state == 'down':
            # Check if Ravenloft Board Game is enabled so we enable certain sets
            self.all_heroes.update(['Immeril', 'Allisa', 'Arjhan', 'Kat', 'Thorgrim'])
            self.tilesets.update(['Dungeon (Castle Ravenloft)'])
            self.items.update(['Crystal Ball'])
            self.villains_easy.update(['Klak, Kobold Sorcerer[EASY]', 'Howling Hag[EASY]', 'Werewolf[EASY]',\
                                       'Zombie Dragon[EASY]', 'Young Vampire[EASY]'])
            self.villains_normal.update(['Klak, Kobold Sorcerer[NORMAL]', 'Howling Hag[NORMAL]',
            'Werewolf[NORMAL]', 'Zombie Dragon[NORMAL]', 'Young Vampire[NORMAL]'])
            self.villains_hard.update(['Klak, Kobold Sorcerer[HARD]', 'Howling Hag[HARD]',
            'Werewolf[HARD]', 'Zombie Dragon[HARD]', 'Young Vampire[HARD]'])
            self.bosses.update(['Gravestorm, Dracolich', 'Flesh Golem', 'Count Strahd Von Zarovich'])
            self.monster_types.update(['Undead', 'Animal'])

        self.num_boards = [castle_raven.state, wrath_ashard.state, legend_drizzt.state, temple_evil.state,
                           tomb_an.state, mad_mage.state].count('down')
        # Cases Sector
        ASHARDALON_SPECIFIC = ['Dire Chamber Entrance', 'Horrid Chamber Entrance']
        CAVERN_SPECIFIC = ['Cavern of Ooze', 'Halaster\'s Rune', 'The Runestone']
        MAGE_SPECIFIC = ['Graves', 'Underground River', 'The Gauntlet', 'The Ossuary']
        TOEE_SPECIFIC = ['Oubliette', 'Fire Altar', 'Pool of Olhydra', 'Guard Room', 'Water Altar', 'Earth Altar'\
                         ,'Air Altar', 'Massacre Site', 'Furnace Room']
        RAVENLOFT_SPECIFIC = ['Rotting Nook', 'Fetid Den', 'Arcane Circle', 'Dark Fountain', 'Secret Stairway',\
        'Chapel', 'Workshop', 'Laboratory']
        DRIZZT_SPECIFIC = ['Dark Chasm', 'Underground River (Drizzt)', 'Crystal Shard', 'Drow Glyph', 'Broken Door']
        EXTRA_TILES_DRIZZT = ['Ancient Throne', 'Rocky Lair']
        EXTRA_TILES_MAGE = ['Mirror Gate / Arch Gate', 'Shadowdusk Hold / Arch Gate']
        EXTRA_TILES_TOEE = ['Elemental Air Node', 'Elemental Water Node', 'Elemental Fire Node', 'Elemental Earth Node']
        EXTRA_TILES_RAVENLOFT = ['Lonely Crypt', 'King\'s Crypt', 'Ireena Kolyana\'s Crypt', 'Stahd\'s Crypt',\
        'Crypt of Barov and Ravenovia', 'Crypt of Sergei Von Zarovich', 'Crypt of Artimus', 'Prince Aurel\'s Crypt']
        SLAY_MONSTERS = list(self.monster_types)
        SAVE_INNOCENT = ['Mark', 'Roy', 'Dave', 'Dianna', 'Gabel', 'Joe']
        RECLAIM_ITEM = list(self.items)
        DESTROY_ITEM = ['Malefic Sword(AC: 11 - HP: 10)', 'Necklace of the Greedy(AC: 14 - HP: 9)',
                        'Stardust Wand(AC: 13 - HP: 14)', 'Enchanting Flute(AC: 8 - HP: 18)']
        if self.campaign_diff == 'normal':
            SLAY_VILLAINS = list(self.villains_easy)
        elif self.campaign_diff == 'hard':
            SLAY_VILLAINS = list(self.villains_normal)
        SLAY_BOSSES = list(self.bosses)

    def save_state(self, instance):
        global PARTICIPANTS,RECLAIM_ITEM,DESTROY_ITEM, SLAY_VILLAINS,CURRENT_ADV,SLAY_BOSSES
        self.store = JsonStore('save.json')
        # put some values
        self.store.put('all_heroes', list=ALL_HEROES)
        self.store.put('taverns', list=CP_TAVERNS)
        self.store.put('tavern', name=self.tavern.text)
        self.store.put('heroes', name=self.heroes.text)
        self.store.put('deck_changes', name=self.deck_change.text)
        self.store.put('adv_no', number=self.advno.text)
        self.store.put('difficulty', number=self.diff.text, mode=self.campaign_diff)
        self.store.put('adv_case', name=self.adv_case.text)
        self.store.put('tiles', name=self.tiles.text)
        self.store.put('gold', number=self.gold.text)
        self.store.put('items', name=self.itembox.text, list=RECLAIM_ITEM, destroy=DESTROY_ITEM)
        self.store.put('boss', name=self.defeated_boss, villain=SLAY_VILLAINS, choice=self.slay_villain_choice, bosses=SLAY_BOSSES)
        self.store.put('participants', name=PARTICIPANTS)
        self.store.put('check_raven', checked=castle_raven.state)
        self.store.put('check_wrath', checked=wrath_ashard.state)
        self.store.put('check_drizzt', checked=legend_drizzt.state)
        self.store.put('check_temple', checked=temple_evil.state)
        self.store.put('check_tomb', checked=tomb_an.state)
        self.store.put('check_mage', checked=mad_mage.state)
        self.store.put('ally', name=ALLY)
        self.store.put('lvl', name=self.lvl.text)
        self.store.put('current_adv', name=CURRENT_ADV)

    def load_state(self, instance):

        global CP_TAVERNS, RECLAIM_ITEM, ALL_HEROES, SLAY_VILLAINS, SLAY_BOSSES, ALLY, PARTICIPANTS, SAVE_ALLY, DESTROY_ITEM,CURRENT_ADV
        try:
            self.store = JsonStore('save.json')
            self.tavern.text = self.store.get('tavern')['name']
            CP_TAVERNS = self.store.get('taverns')['list']
            self.heroes.text = self.store.get('heroes')['name']
            self.deck_change.text = self.store.get('deck_changes')['name']
            self.advno.text = self.store.get('adv_no')['number']
            self.diff.text = self.store.get('difficulty')['number']
            self.tiles.text = self.store.get('tiles')['name']
            self.gold.text = self.store.get('gold')['number']
            self.itembox.text = self.store.get('items')['name']
            self.adv_case.text = self.store.get('adv_case')['name']
            self.lvl.text = self.store.get('lvl')['name']
            self.defeated_boss = self.store.get('boss')['name']
            self.slay_villain_choice = self.store.get('boss')['choice']
            self.campaign_diff = self.store.get('difficulty')['mode']
            CURRENT_ADV = self.store.get('current_adv')['name']
            castle_raven.state = self.store.get('check_raven')['checked']
            wrath_ashard.state = self.store.get('check_wrath')['checked']
            legend_drizzt.state = self.store.get('check_drizzt')['checked']
            temple_evil.state = self.store.get('check_temple')['checked']
            tomb_an.state= self.store.get('check_tomb')['checked']
            mad_mage.state = self.store.get('check_mage')['checked']
            ALLY = self.store.get('ally')['name']
            ALL_HEROES = self.store.get('all_heroes')['list']
            PARTICIPANTS = self.store.get('participants')['name']
            self.antihero = []
            if legend_drizzt.state == 'down':
                self.antihero = [x for x in ['Artemis', 'Jarlaxe'] if x not in PARTICIPANTS]
            SAVE_ALLY = [x for x in ALL_HEROES if x not in PARTICIPANTS and x not in self.antihero]
            self.setting_adv()
            RECLAIM_ITEM = self.store.get('items')['list']
            DESTROY_ITEM = self.store.get('items')['destroy']
            SLAY_VILLAINS = self.store.get('boss')['villain']
            SLAY_BOSSES = self.store.get('boss')['bosses']
            if int(self.advno.text) >= 5:
                self.rect.source = backImages_list[1]
            elif int(self.advno.text) >= 10:
                self.rect.source = backImages_list[2]
            else:
                self.rect.source = backImages_list[0]
            try:
                SLAY_BOSSES.remove(self.defeated_boss)
                self.defeated_boss = ''
            except:
                pass
            self.create.disabled = False
            try:
                self.add_widget(self.next_adv)
                self.add_widget(self.tools)
            except:
                pass
            self.next_adv.disabled = False
            self.saving.disabled = False
            # self.adv_case.font_size = '14'
        except:
            # self.adv_case.text = 'IT LOOKS LIKE YOU DON\'T HAVE A SAVE FILE!'
            return

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def does_fireworks(self):
        try:
            self.add_widget(fireworks)
            fireworks.reload()
        except:
            return
        # Fireworks Sound
        if firework_sound:
            if check_music.active:
                firework_sound.loop = False
                firework_sound.volume = .6
                firework_sound.play()

    def callback(self,instance):
        # print(self.hero_buttons)
        sum_down = 0
        for button in self.hero_buttons:
            if button.state == 'down':
                sum_down += 1
        # print(sum_down)
        if sum_down > 4:
            instance.state = 'normal'

    def get_level(self, instance):
        global PARTICIPANTS
        level_grid = GridLayout(cols=2)
        self.all_buttons = []
        for hero in PARTICIPANTS:
            btn = Button(text=hero)
            level_grid.add_widget(btn)
            self.all_buttons.append(btn)
        level_pop.content = level_grid
        level_pop.open()
        for button in self.all_buttons:
            button.bind(on_release=self.leveling)

    def leveling(self,instance):
        global PARTICIPANTS
        level_pop.dismiss()

        # Just a Level Up Sound
        level = SoundLoader.load('music/level_up.ogg')
        if level:
            if check_music.active:
                level.loop = False
                level.volume = .5
                level.play()
        # Sound over
        self.congr_pop = Popup(title='Congratulations!', title_size='18sp', title_align='center',
                             separator_color=[0, 100 / 255, 0, 1],
                             size_hint=(.2, .2),auto_dismiss=False)
        self.congr_pop.open()
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text=instance.text + ' gained a level!'))
        self.congr_pop.content = box
        hero_index = PARTICIPANTS.index(instance.text)
        lvl_list = [int(x) for x in self.lvl.text.splitlines()]
        lvl_list[hero_index] += 1
        string_list = [str(x) for x in lvl_list]
        self.lvl.text = '\n'.join(string_list)
        self.lvl.text += '\n'
        Clock.schedule_once(self.wait_pop, 2)

    def wait_pop(self,*args):
        self.congr_pop.auto_dismiss = True

    def rolling_die(self,instance):
        # Just a Dice Roll Sound
        dice = SoundLoader.load('music/dice.ogg')
        if dice:
            if check_music.active:
                dice.loop = False
                dice.volume = .5
                dice.play()
        # Sound over
        self.roll_die.disabled = True
        toolbox.auto_dismiss = False
        self.function_interval = Clock.schedule_interval(self.update_die, .1)
        Clock.schedule_once(self.stop_interval, 1)

    def update_die(self,*args):
        self.roll_die.text = str(randrange(1,21))

    def stop_interval(self,*args):
        self.function_interval.cancel()
        toolbox.auto_dismiss = True
        self.roll_die.disabled = False

    # def restore_tools(self,instance):
    #     self.roll_die.text = 'Roll D20'
    #     self.monster_tokens.text = 'Monster Tokens'

    def treasure_tokens_menu(self,instance):
        self.treasure_pop = Popup(title='Draw a Token by clicking on it: ', title_size='18sp', title_align='center',
                             separator_color=[0, 100 / 255, 0, 1],
                             size_hint=(.5, .7))
        treasure_layout = BoxLayout(orientation='vertical',spacing='10sp')
        # treasure_layout = GridLayout(cols=1)
        self.treasure_pick = Button(text='', font_size='14sp',background_normal='treasure_tokens/treasureback.jpg',
                                    background_disabled_normal='treasure_tokens/treasureback.jpg', size_hint=(.4,.1),
                                    pos_hint= {'x': .3}, background_down='treasure_tokens/treasureback.jpg')
        self.treasure_pick.bind(on_release=self.anim_treasure)
        self.shuffle_btn = Button(text='Reshuffle', font_size='14sp', background_color=(1,0,1,1),
                             size_hint=(.4, .05), pos_hint={'x': .3})
        self.shuffle_btn.bind(on_release=self.reset_treasure)
        treasure_layout.add_widget(self.treasure_pick)
        self.treasure_remaining = Label(text='There are {} tokens remaining.'.format(len(self.treasure_tokens)),size_hint=(.4,.03), pos_hint= {'x': .3})
        treasure_layout.add_widget(self.treasure_remaining)
        treasure_layout.add_widget(self.shuffle_btn)
        self.treasure_pop.content = treasure_layout
        self.treasure_pop.open()

    def anim_treasure(self, *args):
        click_sound = SoundLoader.load('music/click.ogg')
        if click_sound:
            if check_music.active:
                click_sound.loop = False
                click_sound.volume = .5
                click_sound.play()
        if not self.treasure_tokens:
            self.reset_treasure()
        self.treasure_pick.disabled = True
        self.treasure_pop.auto_dismiss = False
        self.shuffle_btn.disabled = True
        # anim = Animation(width=-self.treasure_pick.width, t='in_quad')
        anim = Animation(background_color=(1,1,1,0),duration=.6)
        anim.start(self.treasure_pick)
        Clock.schedule_once(self.get_treasure, .6)

    def get_treasure(self,instance):
        # anim = Animation(width=Window.width/5, t='out_quad')
        anim = Animation(background_color=(1, 1, 1, 1),duration=.6)
        anim.start(self.treasure_pick)
        try:
            if self.treasure_tokens[0] == '100':
                self.treasure_pick.background_disabled_normal='treasure_tokens/100gp.jpg'
                self.treasure_pick.background_normal = 'treasure_tokens/100gp.jpg'
                self.treasure_pick.background_down = 'treasure_tokens/100gp.jpg'
            elif self.treasure_tokens[0] == '200':
                self.treasure_pick.background_disabled_normal='treasure_tokens/200gp.jpg'
                self.treasure_pick.background_normal = 'treasure_tokens/200gp.jpg'
                self.treasure_pick.background_down = 'treasure_tokens/200gp.jpg'
            elif self.treasure_tokens[0] == '300':
                self.treasure_pick.background_disabled_normal='treasure_tokens/300gp.jpg'
                self.treasure_pick.background_normal = 'treasure_tokens/300gp.jpg'
                self.treasure_pick.background_down = 'treasure_tokens/300gp.jpg'
            elif self.treasure_tokens[0] == '400':
                self.treasure_pick.background_disabled_normal='treasure_tokens/400gp.jpg'
                self.treasure_pick.background_normal = 'treasure_tokens/400gp.jpg'
                self.treasure_pick.background_down = 'treasure_tokens/400gp.jpg'
            elif self.treasure_tokens[0] == '500':
                self.treasure_pick.background_disabled_normal='treasure_tokens/500gp.jpg'
                self.treasure_pick.background_normal = 'treasure_tokens/500gp.jpg'
                self.treasure_pick.background_down = 'treasure_tokens/500gp.jpg'
            elif self.treasure_tokens[0] == 'treasure':
                self.treasure_pick.background_disabled_normal='treasure_tokens/TreasureItem.jpg'
                self.treasure_pick.background_normal = 'treasure_tokens/TreasureItem.jpg'
                self.treasure_pick.background_down = 'treasure_tokens/TreasureItem.jpg'
            self.treasure_pick.texture_update()
            del self.treasure_tokens[0]
            self.treasure_remaining.text = 'There are {} tokens remaining.'.format(len(self.treasure_tokens))
            Clock.schedule_once(self.enable_treasure_pick, .6)
        except:
            # self.reset_treasure(instance)
            pass

    def enable_treasure_pick(self,*args):
        self.treasure_pick.disabled = False
        self.treasure_pop.auto_dismiss = True
        self.shuffle_btn.disabled = False


    def reset_treasure(self,*args):
        self.treasure_tokens = ['100'] * 9 + ['200'] * 11 + ['300'] * 5 + ['400'] * 2 + ['treasure'] * 5 + ['500']
        shuffle(self.treasure_tokens)
        self.treasure_remaining.text = 'There are {} tokens remaining.'.format(len(self.treasure_tokens))
        self.treasure_pick.background_normal = 'treasure_tokens/treasureback.jpg'
        self.treasure_pick.background_disabled_normal = 'treasure_tokens/treasureback.jpg'
        self.treasure_pick.background_down = 'treasure_tokens/treasureback.jpg'

    def monster_tokens_menu(self,*args):
        self.monster_pop = Popup(title='Draw a Token by clicking on it: ', title_size='18sp', title_align='center',
                             separator_color=[0, 100 / 255, 0, 1],
                             size_hint=(.5, .4))
        monster_layout = BoxLayout(orientation='vertical', spacing='10sp')
        # treasure_layout = GridLayout(cols=1)
        self.monster_tokens_pick = Button(text='', font_size='14sp', background_normal='monster_tokens/monster_tokens_back.jpg',
                                    background_disabled_normal='monster_tokens/monster_tokens_back.jpg', size_hint=(.4, .1),
                                    pos_hint={'x': .3},background_down='monster_tokens/monster_tokens_back.jpg')
        self.monster_tokens_pick.bind(on_release=self.anim_monster)
        monster_layout.add_widget(self.monster_tokens_pick)
        self.monster_pop.content = monster_layout
        self.monster_pop.open()

    def anim_monster(self, *args):
        # Just a Click Sound on Button press
        click_sound = SoundLoader.load('music/click.ogg')
        if click_sound:
            if check_music.active:
                click_sound.loop = False
                click_sound.volume = .5
                click_sound.play()
        # Click sound over
        self.monster_tokens_pick.disabled = True
        self.monster_pop.auto_dismiss = False
        anim = Animation(background_color=(1, 1, 1, 0), duration=.6)
        anim.start(self.monster_tokens_pick)
        Clock.schedule_once(self.get_tokens, .6)

    def get_tokens(self,instance):
        anim = Animation(background_color=(1, 1, 1, 1), duration=.6)
        anim.start(self.monster_tokens_pick)
        if self.campaign_diff == 'normal':
            weight = (.2, .5, .2, .1, 0)
        elif self.campaign_diff == 'hard':
            weight = (0, .4, .3, .2, .1)
        the_choice = int(choices((0, 1, 2, 3, 4), weight)[0])
        if the_choice == 0:
            self.monster_tokens_pick.background_disabled_normal = 'monster_tokens/0.jpg'
            self.monster_tokens_pick.background_normal = 'monster_tokens/0.jpg'
            self.monster_tokens_pick.background_down = 'monster_tokens/0.jpg'
        if the_choice == 1:
            self.monster_tokens_pick.background_disabled_normal = 'monster_tokens/1.jpg'
            self.monster_tokens_pick.background_normal = 'monster_tokens/1.jpg'
            self.monster_tokens_pick.background_down = 'monster_tokens/1.jpg'
        if the_choice == 2:
            self.monster_tokens_pick.background_disabled_normal = 'monster_tokens/2.jpg'
            self.monster_tokens_pick.background_normal = 'monster_tokens/2.jpg'
            self.monster_tokens_pick.background_down = 'monster_tokens/2.jpg'
        if the_choice == 3:
            self.monster_tokens_pick.background_disabled_normal = 'monster_tokens/3.jpg'
            self.monster_tokens_pick.background_normal = 'monster_tokens/3.jpg'
            self.monster_tokens_pick.background_down = 'monster_tokens/3.jpg'
        if the_choice == 4:
            self.monster_tokens_pick.background_disabled_normal = 'monster_tokens/4.jpg'
            self.monster_tokens_pick.background_normal = 'monster_tokens/4.jpg'
            self.monster_tokens_pick.background_down = 'monster_tokens/4.jpg'
        Clock.schedule_once(self.enable_monster_pick, .6)

    def enable_monster_pick(self,*args):
        self.monster_tokens_pick.disabled = False
        self.monster_pop.auto_dismiss = True


class DnDGenerator(App):

    def build(self):
        self.icon = 'icon.ico'
        self.title = 'Dungeons & Dragons Campaign Generator'
        return MyUI()


if __name__ == '__main__':
    DnDGenerator().run()
