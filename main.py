from pygamelib import *
from pickle import load, dump

pygame.init()
windowWidth = 1280
windowHeight = 720
window = pygame.display.set_mode((windowWidth, windowHeight))

class Setting:
    def __init__(self):
        self.skin = None
        self.clock = None
        self.file = None

    def fetchSettings(self):
        if self.openSettingFile():
            settingData = load(self.file)
            self.skin = settingData['skin']
            self.clock = settingData['clock']
            self.closeSettingFile()
        else:
            self.skin = os.path.join(SKINS_DIR, "1.mov")
            self.clock = "default"
            self.updateSetting()

    def structData(self):
        return {'skin':self.skin, 'clock':self.clock}

    def updateSetting(self):
        if self.openSettingFile('wb'):
            settingData = self.structData()
            dump(settingData, self.file)
            self.closeSettingFile()
            return
        else:
            return False

    def openSettingFile(self, mode='rb'):
        try:
            self.file = open(SETTING_FILE, mode)
            return True
        except:
            return False

    def closeSettingFile(self):
        try:
            self.file.close()
            self.file = None
            return True
        except:
            self.file = None
            return False


def closeApplication():
    exit()


def MianMenu():
    run = True
    setting = Setting()
    setting.fetchSettings()

    # Creating Main Frame
    MainFrame = Frame(window, 'frame', (0, 0, 1280, 720),
                    partition=[{'name': 'part_1', 'area': 90, 'color': (0, 0, 255), 'outline': 0},
                               {'name': 'part_2', 'area': 10, 'color': (56, 67, 73), 'outline': 0}])

    SettingButton = Button(window, ICON_SETTING, ICON_SETTING, 120, 0, "", True, win_height=windowHeight,
                           win_width=windowWidth, width=27, perfect_collision_check=False)
    alarmBUtton = Button(window, ICON_ALARM_CLOCK, ICON_ALARM_CLOCK, 70, 0, "", True, win_height=windowHeight,
                           win_width=windowWidth, width=27, perfect_collision_check=False)
    stopWatchButton = Button(window, ICON_STOP_WATCH, ICON_STOP_WATCH, 20, 0, "", True, win_height=windowHeight,
                           win_width=windowWidth, width=27, perfect_collision_check=False)
    clockButton = Button(window, ICON_CLOCK, ICON_CLOCK, 170, 0, "", True, win_height=windowHeight,
                           win_width=windowWidth, width=27, perfect_collision_check=False)

    MainFrame.addComponents(SettingButton, 'part_2', True)
    MainFrame.addComponents(alarmBUtton, 'part_2', True)
    MainFrame.addComponents(stopWatchButton, 'part_2', True)
    MainFrame.addComponents(clockButton, 'part_2', True)

    CalenderFrame = Frame(window, "calender", (600, 120, 500, 450),
                          partition=[{'name': 'part_1', 'area': 15, 'color': (52, 154, 152, 240), 'outline': 0},
                                     {'name': 'part_2', 'area': 85, 'color': (255, 255, 255, 10), 'outline': 0}],
                          borderRadius=(10, 10, 10, 10))

    # Clock Frame
    video = VideoPlayer(window, 0, 0, "assets/skin/2.mp4", True)
    video.activeFrameResizer(1280, aspectRatio=True)
    video.activeFrameCropper((0, 0, 1280, 648))
    digitalClock = DigitalClock(window, (100, 100), 50)
    ClockFrame = Frame(window, "clockFrame", (0, 0, 1280, 648))
    ClockFrame.addComponents(video)
    ClockFrame.addComponents(digitalClock)
    ClockFrame.addComponents(CalenderFrame)

    # Setting Frame
    SettingFrame = Frame(window, 'Setting Frame', (0, 0, 1280, 649),
                         partition=[{'name': 'part_1', 'area': 13, 'color': (34, 41, 47), 'outline': 0},
                                    {'name': 'part_2', 'area': 9, 'color': (52, 154, 152), 'outline': 0},
                                    {'name': 'part_3', 'area': 78, 'color': (42, 49, 55), 'outline': 0}])
    LabelPerformance = Label(window, 10, 10, "Performance", (52, 154, 152), 28, FONT_ADVENTPRO)
    SettingFrame.addComponents(LabelPerformance, 'part_1', True, True)

    # Alarm
    AlarmFrame = Frame(window, "calender", (600, 120, 500, 450),
                       partition=[{'name': 'part_1', 'area': 15, 'color': (52, 154, 152, 240), 'outline': 0},
                                  {'name': 'part_2', 'area': 85, 'color': (255, 255, 255, 10), 'outline': 0}],
                       borderRadius=(10, 10, 10, 10))
    # l = HLayout(12)

    ActiveWindow = SettingFrame
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closeApplication()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    x, y = event.pos
                    if clockButton.rect_collision_check(x, y):
                        ActiveWindow = ClockFrame
                    elif SettingButton.rect_collision_check(x, y):
                        ActiveWindow = SettingFrame

        MainFrame.show()
        ActiveWindow.show()
        pygame.display.update()

MianMenu()

