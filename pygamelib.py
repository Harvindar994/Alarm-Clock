import pygame
import cv2
import numpy
import os
import threading
import time
import webbrowser
from datetime import datetime

# Common Functions
def openCVFrameToPygameSurface(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = numpy.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    return frame


def extractFramesFromVideo(video, output_dir="", frameCount=None, mirror_effect=False, counterStartPoint=0,
                           skipFrame=0):
    video = cv2.VideoCapture(video)
    counter = counterStartPoint
    frameCounter = 0
    converting = True
    while converting:
        flag, frame = video.read()
        if flag:
            if skipFrame > 0:
                skipFrame -= 1
                continue
            if not mirror_effect:
                frame = cv2.flip(frame, 1)
            cv2.imwrite(os.path.join(output_dir, str(counter)+".jpg"), frame)
            counter += 1
            if frameCount is not None:
                frameCounter += 1
                if not frameCounter < frameCount:
                    converting = False
        else:
            break

    video.release()

def out_text_file(surface, text, size, x, y, color, font_file, return_img = False, bk_color=None):
    try:
        font = pygame.font.Font(font_file, size)
    except OSError:
        font = pygame.font.SysFont(None, size)
    text_img = font.render(text, True, color, bk_color)
    if return_img:
        return text_img
    surface.blit(text_img, [x, y])

def custom_out_text(surface, text, x, x1, y, color, size, f_file):
    text_img = out_text_file(surface, text, size, 0, 0, color, f_file, True)
    put_point_x = x + ((x1 - x) // 2)
    put_point_x = put_point_x - (text_img.get_width() // 2)
    surface.blit(text_img, [put_point_x, y])

def open_url(url):
    try:
        webbrowser.get('chrome').open_new(url)
    except:
        try:
            webbrowser.get('firefox').open_new_tab(url)
        except:
            try:
                webbrowser.open(url, new=1)
            except:
                return False
    return True

def fadeout(surface, page, x, y):
    path = os.path.join(DIR_TEMP_DATA, "welcome_screen.png")
    pygame.image.save(surface, path)
    temp_image = pygame.image.load(path)
    temp_image = temp_image.convert()
    temp_image2 = page.convert()
    i = 255
    i2 = 0
    while i > 0:
        temp_image.set_alpha(i)
        temp_image2.set_alpha(i2)
        surface.blit(temp_image2, [x, y])
        surface.blit(temp_image, [x, y])
        i -= 5
        i2 += 5
        pygame.display.update()

def createBluredImg(input_img, output_img, ksize=(7, 7), sigmaX=0):
    try:
        image = cv2.imread(input_img)
        Gaussian_blur = cv2.GaussianBlur(image, ksize, sigmaX)
        cv2.imwrite(output_img, Gaussian_blur)
    except:
        return False
    return True

def collision(maskFirst, maskSecond, maskFirstPos_x, maskFirstPos_y, maskSecondPos_x, maskSecondPos_y):
	offset = (int(maskFirstPos_x - maskSecondPos_x), int(maskFirstPos_y - maskSecondPos_y))
	result = maskSecond.overlap(maskFirst, offset)
	return result


class Frame:
    def __init__(self, surface, name, area, backgroundColor=None, partition=None, borderRadius=None, outline=0):
        self.name = name
        self.x, self.y, self.width, self.height = area
        self.areaUnit = self.height / 100
        self.borderRadius = borderRadius
        self.surface = surface
        self.outline = outline

        """
        data structure of partition will be in percentage.
        structure: {'area': area_in_percentage, 'color': RGB_color, 'outline': Width_of_outline_in_pixel}
        note: partition will work to define different area with different color, and it will be in the vertical way.
        """
        self.partitions = None
        self.totalPartitions = 0
        self.rePartition(partition)
        self.backgroundColor = backgroundColor

        """
        this list is containing all the default attribute that should be available in Component.
        """
        self.defaultAttributes = ['show', 'x', 'y']

        """
        This list will be containing all the elements that user will add in the frame
        """
        self.elements = []

    def addComponents(self, element):
        # Here checking that all the default attributes is available in the give object or not.
        attributes = element.__dir__()
        for attribute in self.defaultAttributes:
            if attribute not in attributes:
                print(f"'{attribute}' is not available in the give object")
                return

        # defining the actual position of element according to the frame.
        element.x = self.x + element.x
        element.y = self.y + element.y

        # here adding the element in the list.
        self.elements.append(element)
        return True

    def rePartition(self, partitions):
        if partitions is None:
            self.partitions = None
        else:
            totalArea = 100
            Current_y = self.y
            self.partitions = []
            for partition in partitions:
                area = partition['area']
                if totalArea >= area:
                    totalArea -= area
                    height = (self.areaUnit*area)
                    partition['area'] = (self.x, Current_y, self.width, height)
                    self.partitions.append(partition)
                    Current_y += height
                else:
                    print(f'There is not enough space create partition, Partition Info:{partition}')
                    break
            self.totalPartitions = len(self.partitions)

    def show(self):
        if self.backgroundColor is not None and self.partitions is not None:
            if self.borderRadius is not None:
                pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                 width=self.outline,
                                 border_top_left_radius=self.borderRadius[0],
                                 border_top_right_radius=self.borderRadius[1],
                                 border_bottom_right_radius=self.borderRadius[2],
                                 border_bottom_left_radius=self.borderRadius[3])
            else:
                pygame.draw.rect(self.surface, self.backgroundColor, (self.x, self.y, self.width, self.height),
                                 width=self.outline)
        elif self.partitions is not None:
            counter = 0
            while counter < self.totalPartitions:
                partition = self.partitions[counter]
                area = partition['area']
                if 'color' in partition:
                    color = partition["color"]
                else:
                    if self.backgroundColor is not None:
                        color = self.backgroundColor
                    else:
                        color = (60, 63, 65)
                if 'outline' in partition:
                    outline = partition['outline']
                else:
                    outline = self.outline
                if self.borderRadius is not None:
                    if counter == 0:
                        pygame.draw.rect(self.surface, color, area, width=outline,
                                         border_top_left_radius=self.borderRadius[0],
                                         border_top_right_radius=self.borderRadius[1])
                    elif counter == self.totalPartitions - 1:
                        pygame.draw.rect(self.surface, color, area, width=outline,
                                         border_bottom_right_radius=self.borderRadius[2],
                                         border_bottom_left_radius=self.borderRadius[3])
                    else:
                        pygame.draw.rect(self.surface, color, area, width=outline)
                else:
                    pygame.draw.rect(self.surface, color, area, width=self.outline)
                counter += 1
            self.showElements()

    def showElements(self):
        for element in self.elements:
            element.show()
            

class VideoPlayer:
    def __init__(self, surface, x, y, video, play_in_loop=False, mirror_effect=False):
        self.video = video
        self.surface = surface
        self.VideoReader = None
        self.FileOpened = False
        self.x = x
        self.y = y
        self.playInLoop = play_in_loop
        self.open()
        self.FrameResizer = False
        self.mirrorEffect = mirror_effect
        self.height = None
        self.width = None
        self.frameCrop = None

    def maintainAspectRatio(self):
        video = cv2.VideoCapture(self.video)
        flag, frame = video.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = numpy.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        height = frame.get_height()
        width = frame.get_width()
        self.height = int((self.width * (height/width)))
        video.release()

    def activeFrameCropper(self, area):
        """
        :param area: (x, y, width, height)
        :return: None
        """
        self.frameCrop = area

    def deactivateFrameCropper(self):
        self.frameCrop = None

    def activeMirrorEffect(self):
        self.mirrorEffect = True

    def deactivateMirrorEffect(self):
        self.mirrorEffect = False

    def activeFrameResizer(self, width=600, height=600, aspectRatio=False):
        self.FrameResizer = True
        self.width = width
        self.height = height
        if aspectRatio:
            self.maintainAspectRatio()

    def deactivateFrameResizer(self):
        self.FrameResizer = False

    def open(self):
        try:
            self.VideoReader = cv2.VideoCapture(self.video)
        except:
            self.FileOpened = False
            return False
        self.FileOpened = True

    def close(self):
        self.VideoReader.release()
        self.FileOpened = False

    def show(self):
        if self.FileOpened:
            repeat = True
            while repeat:
                flag, frame = self.VideoReader.read()
                if flag:
                    if not self.mirrorEffect:
                        frame = cv2.flip(frame, 1)

                    if self.FrameResizer:
                        frame = cv2.resize(frame, (self.width, self.height), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                    if self.frameCrop is not None:
                        x, y, width, height = self.frameCrop
                        frame = frame[y:y+height, x:x+width]  # frame[y:y+height, x:x+width]
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = numpy.rot90(frame)
                    frame = pygame.surfarray.make_surface(frame)
                    self.surface.blit(frame, (self.x, self.y))
                    repeat = False
                else:
                    self.close()
                    if self.playInLoop:
                        self.open()


# modification in classes is needed in all the classes that is bellow


class ProgressBar:
    def __init__(self, screen, progress_rect, progress_rect_color, background_rect=None, background_rect_color=None,
                 text_color=(255, 255, 255), show_percentage=False, text_size=14, default_value=100, font_style=Font_sofiapro_light):
        self.screen = screen
        self.x, self.y, self.max_width, self.height = progress_rect
        # now here deciding the current width of progress bar according to current value.
        self.unit_width = self.max_width/100
        self.set_value(default_value)

        self.progress_rect_color = progress_rect_color
        if background_rect is None:
            self.background_rect = background_rect
        else:
            self.background_rect = background_rect
            self.background_rect_color = background_rect_color
        self.text_size = text_size
        self.text_color = text_color
        self.font_style = font_style
        self.show_percentage_flag = show_percentage

        # now deciding the position text.
        test_text = out_text_file(self.screen, "100%", self.text_size, 0, 0, self.text_color, self.font_style, True)
        text_width = test_text.get_width()
        text_height = test_text.get_height()
        x, y, width, height = progress_rect
        self.text_x = x+width
        self.text_x1 = self.text_x+text_width+8
        self.text_y = (self.y+(self.height//2))-(text_height//2)

    def set_value(self, value):
        if value >= 0 and value <= 100:
            self.value = value
            self.width = self.value*self.unit_width
        elif value<=0:
            self.value = 0
            self.width =self.value*self.unit_width
        elif value>=100:
            self.value = 100
            self.width = self.value * self.unit_width

    def show_percentage(self):
        custom_out_text(self.screen, str(int(self.value)) + "%", self.text_x, self.text_x1, self.text_y, self.text_color,
                        self.text_size, self.font_style)

    def show(self):
        if self.background_rect is not None:
            pygame.draw.rect(self.screen, self.background_rect_color, self.background_rect)
        pygame.draw.rect(self.screen, self.progress_rect_color, (self.x, self.y, self.width, self.height))
        if self.show_percentage_flag:
            custom_out_text(self.screen, str(int(self.value)) + "%", self.text_x, self.text_x1, self.text_y, self.text_color,
                            self.text_size, self.font_style)


class DigitalClock:
    def __init__(self, position, font_size, dateFontSize = 20, show_date=True, font_color=WHITE_COLOR, font_file = Font_Quicksand_Regular, screen=GameWindow):
        self.x, self.y = position
        self.screen = screen
        self.dateFontSize = dateFontSize
        self.fontColor = font_color
        self.fontSize = font_size
        self.font_file = font_file
        self.showDate = show_date
        self.time = ""
        self.date = ""
        self.date_x = None
        self.date_y = None

    def update_time(self):
        now = datetime.now()
        # for date.
        date = now.strftime("%B %d, %Y")
        # for time
        time = now.strftime("%H : %M : %S")
        self.time = out_text_file(GameWindow, time, self.fontSize, 0, 0, self.fontColor, self.font_file, True).convert_alpha()
        if self.showDate:
            self.date = out_text_file(GameWindow, date, self.dateFontSize, 0, 0, self.fontColor, self.font_file, True).convert_alpha()
            # self.date_x = (self.x + self.time.get_width()) - self.date.get_width()
            if self.date_y == None:
                self.date_y = self.y + self.time.get_height()-5

    def set_position(self):
        pass

    def set_font_size(self):
        pass

    def show(self):
        self.update_time()
        self.screen.blit(self.time, (self.x, self.y))
        if self.showDate:
            self.screen.blit(self.date, (self.x, self.date_y))


class SoundManager:
    sounds = {}  # this dict will store all sound file which is loaded in the game. and any object of this class can access.
    settingData = None

    def __init__(self):
        pass

    def load_sound(self, name, sound_file, default_volume=None):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.stop()
            self.sounds.pop(name)

        self.sounds[name] = pygame.mixer.Sound(sound_file)
        if default_volume != None:
            pygame.mixer.Sound.set_volume(self.sounds[name], default_volume)

    def play_sound(self, name, loop=0, maxmim_time=None):
        if self.settingData.game_sound:
            if name in self.sounds:
                if maxmim_time == None:
                    pygame.mixer.Sound.play(self.sounds[name], loop)
                else:
                    pygame.mixer.Sound.play(self.sounds[name], loop, maxmim_time)
            else:
                return "FNF"
                # File Not Found

    def set_volume(self, name, volume):
        # Max Value 1.0
        # Min Value 0.0
        if name in self.sounds:
            pygame.mixer.Sound.set_volume(self.sounds[name], volume)
        else:
            return "FNF"
            # File Not Found

    def clear_music(self):
        for key, sound in self.sounds.items():
            try:
                sound.stop()
                self.sounds.pop(key)
            except:
                pass

    def stop_sound(self, name='all'):
        if name == 'all':
            for key, sound in self.sounds.items():
                try:
                    sound.stop()
                except:
                    pass
        elif name in self.sounds:
            try:
                sound.stop()
            except:
                return "U_to_S"
            # unable to stop sound.
        else:
            return "FNF"
        # File Not Found


class SequentialAnimation:
    def __init__(self, screen, img_dir, x, y, screen_width, screen_height, auto_postion_at_center=False, create_mask=False):
        self.screen = screen

        # fetching path of all images which is available in side of img_dir.
        loader_images_path = getListOfFiles(img_dir, False)

        # sorting paths in acceding order.
        loader_images_path = sortImagesPath(loader_images_path, img_dir)

        # loading all image.
        self.loader_images = [pygame.image.load(image_path).convert_alpha() for image_path in loader_images_path]

        # creating mask of all images which i loaded in "self.loader_images" but when create_mask will be true.
        if create_mask:
            self.masked_images = []
            for image in self.loader_images:
                self.masked_images.append(pygame.mask.from_surface(image))

        # creating variable for maintaining the index of loader_images list.
        self.counter = 0

        # get height and width of sequence image.
        self.image_width = self.loader_images[self.counter].get_width()
        self.image_height = self.loader_images[self.counter].get_height()

        # creating system to fix location of animation in the center of the screen.
        if auto_postion_at_center:
            self.x = int((screen_width/2) - (self.image_width/2))
            self.y = int((screen_height/2) - (self.image_height/2))-25
        else:
            self.x = x
            self.y = y

        # this variable will store total number of images.
        self.total_images = len(self.loader_images)

        # loader will active until active_state variable will hold True.
        self.active_state = False

    def show(self):
        self.screen.blit(self.loader_images[self.counter], (self.x, self.y))
        self.counter += 1
        if self.counter >= self.total_images:
            self.counter = 0

    def collide(self, other_mask, x, y):
        if collision(self.masked_images[self.counter], other_mask, self.x, self.y, x, y):
            return True
        else:
            return False

class Loader(SequentialAnimation):
    def __init__(self, screen, img_dir, x, y, screen_width, screen_height, auto_postion_at_center=False):
        super(Loader, self).__init__(screen, img_dir, x, y, screen_width, screen_height, auto_postion_at_center)

    def start(self):
        sub = self.screen.subsurface((self.x, self.y, self.image_width, self.image_height))
        image_file = os.path.join(DIR_TEMP_DATA, "temp_img.jpg")
        pygame.image.save(sub, image_file)
        self.background_cover = pygame.image.load(image_file)
        while self.active_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closeGame()

            self.screen.blit(self.background_cover, (self.x, self.y))
            self.show()
            pygame.display.update()
            clock.tick(60)
        self.counter = 0


class RadioButton(SoundManager):
    Groups = {}

    def __init__(self, screen, text, text_size, radio_img, active_img, hover_img, x, y, group=None, active_state=False,
                 text_color=WHITE_COLOR, font_style=Font_Quicksand_Regular):
        self.screen = screen

        # loading image
        self.radio_img = pygame.image.load(radio_img).convert_alpha()
        self.active_img = pygame.image.load(active_img).convert_alpha()
        self.hover_img = pygame.image.load(hover_img).convert_alpha()

        # creating button mask in order to check collision of mouse with button.
        self.button_mask = pygame.mask.from_surface(self.active_img)

        # position of radio button.
        self.x = x
        self.y = y

        # creating text image.
        self.row_text = text
        self.text = out_text_file(screen, text, text_size, 0, 0, text_color, font_style, True)

        # deciding position of text.
        self.text_x = self.x + self.active_img.get_width() + 10
        self.text_y = int((self.y + (self.active_img.get_height()/2)) - (text_size/2))-2

        # creating variable to state button state.
        self.active_state = active_state

        # creating group of radio buttons.
        self.group = group
        if group is not None:
            if group in self.Groups:
                self.Groups[group].append(self)
            else:
                self.Groups[group] = [self]

    def place_config(self, event):
        if self.active_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.y += 1
                    self.text_y += 1
                if event.key == pygame.K_UP:
                    self.y -= 1
                    self.text_y -= 1
                if event.key == pygame.K_LEFT:
                    self.x -= 1
                    self.text_x -= 1
                if event.key == pygame.K_RIGHT:
                    self.x += 1
                    self.text_x += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(f"Button :{self.row_text}, X :{self.x}, Y:{self.y}, Group:{self.group}")

    def collide(self, x, y):
        global PYIMG_MOUSE_COLLSISION_POINT_MASK
        if collision(PYIMG_MOUSE_COLLSISION_POINT_MASK, self.button_mask, x, y, self.x, self.y):
            return True
        else:
            return False

    def place(self, event=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.group is not None and event is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.collide(mouse_x, mouse_y):
                    self.play_sound(SOUND_BUTTON_CLICK)
                    if not self.active_state:
                        for button in self.Groups[self.group]:
                            try:
                                button.active_state = False
                            except:
                                pass
                        self.active_state = True
                        return True

        if event is None:
            self.screen.blit(self.text, (self.text_x, self.text_y))
            if self.collide(mouse_x, mouse_y) and not self.active_state:
                self.screen.blit(self.hover_img, (self.x, self.y))
            elif self.active_state:
                self.screen.blit(self.active_img, (self.x, self.y))
            else:
                self.screen.blit(self.radio_img, (self.x, self.y))
        return False


class Button(SoundManager):
    def __init__(self, surface, image, hover_img, x, y, caption_text='', press_effact=False, button_text=None,
                 button_text_size=28, button_text_color=(255, 255, 255), text_file=Font_Kollektif,
                 list_menu=None, command=None, perfect_collision_check=True):
        self.linked_list = list_menu
        self.surface = surface
        self.command = command
        self.caption = caption_text
        self.press_effact = press_effact
        self.perfect_collision_check = perfect_collision_check
        if type(image) != str:
            self.image = image
        else:
            self.image = pygame.image.load(image).convert_alpha()
            self.image_mask = pygame.mask.from_surface(self.image)
            self.aspect_ration_x = self.image.get_width() / self.image.get_height()
        if type(hover_img) != str:
            self.hover_img = self.image
        else:
            self.hover_img = pygame.image.load(hover_img).convert_alpha()
        self.button_text = button_text
        self.button_text_size = button_text_size
        self.x = x
        self.y = y
        self.x1 = x+self.image.get_width()
        self.y1 = y+self.image.get_height()

        if press_effact:
            img = pygame.transform.scale(self.hover_img, ((self.hover_img.get_width()-4), (self.hover_img.get_height()-4))).convert_alpha()
            self.hover_img = img
        if button_text != None and type(button_text) == str:
            self.button_text_img = out_text_file(surface, button_text, button_text_size, 0, 0, button_text_color, text_file, True)
            self.button_text_x = (self.x+(self.image.get_width()/2))-(self.button_text_img.get_width()/2)
            self.button_text_y = (self.y+(self.image.get_height()/2))-(self.button_text_img.get_height()/2)

    def config_Place(self, event=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.surface.blit(self.image, (mouse_x, mouse_y))
        try:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("MOUSE POS : ", event.pos,
                      ", Width : ", self.image.get_width(),
                      ", Height : ", self.image.get_height(),
                      ", Object_x : ", self.x,
                      ", Object_y : ", self.y)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    self.y -= 1
                if event.key == pygame.K_d:
                    self.y += 1
                if event.key == pygame.K_l:
                    self.x -= 1
                if event.key == pygame.K_r:
                    self.x += 1
                if event.key == pygame.K_DOWN:
                    img_height = self.image.get_height() - 5
                    self.image = pygame.transform.scale(self.hover_img, (int(self.aspect_ration_x*img_height),
                                                        img_height))
                if event.key == pygame.K_UP:
                    img_height = self.image.get_height() + 5
                    self.image = pygame.transform.scale(self.hover_img, (int(self.aspect_ration_x * img_height),
                                                        img_height))
        except:
            pass

    def collide(self, x, y, clicked=False):
        global PYIMG_MOUSE_COLLSISION_POINT_MASK
        if self.perfect_collision_check:
            if collision(PYIMG_MOUSE_COLLSISION_POINT_MASK, self.image_mask, x, y, self.x, self.y):
                if clicked:
                    self.play_sound(SOUND_BUTTON_CLICK)
                return True
            else:
                return False
        else:
            return self.rect_collision_check(x, y, clicked)

    def rect_collision_check(self, x, y, clicked=False):
        if (x > self.x) and (x < self.x1) and (y > self.y) and (y < self.y1):
            if clicked:
                self.play_sound(SOUND_BUTTON_CLICK)
            return True
        else:
            return False

    def config(self, config_dict):
        if type(config_dict) != dict:
            return
        if 'position' in config_dict:
            pos = config_dict['position']
            if type(pos) == list and len(pos) == 2:
                self.x, self.y = pos
            else:
                return

    def place(self, events=None):
        global Mouse_x
        global Mouse_y
        global event
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        #     if events != None:
        # if type(self.linked_list) == List_menu:
        #         for event in events:
        #             if event.type == pygame.MOUSEBUTTONDOWN:
        #                 if event.button == 1:
        #                     mouse_x, mouse_y = event.pos
        #                     if self.collide(mouse_x, mouse_y):
        #                         if self.linked_list.list_state:
        #                             self.linked_list.list_state = False
        #                         else:
        #                             self.linked_list.list_state = True
        if self.collide(Mouse_x, Mouse_y):
            if self.press_effact:
                self.surface.blit(self.hover_img, [self.x+2, self.y+2])
            else:
                self.surface.blit(self.hover_img, [self.x, self.y])
            if len(self.caption) != 0:
                caption(self.caption, self.x1+2, self.y-16)
        else:
            self.surface.blit(self.image, [self.x, self.y])
        if self.button_text != None and type(self.button_text) == str:
            self.surface.blit(self.button_text_img, [self.button_text_x, self.button_text_y])


class Scroll_Button:
    def __init__(self,surface, x, x1, y, bar_thickness, pointer_img, pointer_hover_img = None, zero_value_pinter_img = None,
                 zero_value_pointer_hover_img = None, defult_value = None, text_color=WHITE_COLOR, filled_bar_color=LIGHT_PURPLE,
                 non_filled_bar_color=WHITE_COLOR):
        self.surface = surface
        self.x = x
        self.x1 = x1
        self.y = y
        self.text_color = text_color
        self.filled_bar_color = filled_bar_color
        self.non_filled_bar_color = non_filled_bar_color
        self.thickness = bar_thickness
        self.pointer_img = pointer_img
        self.pointer_hover_img = pointer_hover_img if pointer_hover_img!=None else self.pointer_img
        self.zero_value_pointer_img = zero_value_pinter_img if zero_value_pinter_img!=None else self.pointer_img
        self.zero_value_pointer_hover_img = zero_value_pointer_hover_img if zero_value_pinter_img!=None and zero_value_pointer_hover_img!=None else self.zero_value_pointer_img if zero_value_pinter_img!=None else self.pointer_hover_img
        self.pointer_img = pygame.image.load(self.pointer_img).convert_alpha()
        self.pointer_img_mask = pygame.mask.from_surface(self.pointer_img)
        self.pointer_hover_img = pygame.image.load(self.pointer_hover_img).convert_alpha()
        self.zero_value_pointer_img = pygame.image.load(self.zero_value_pointer_img).convert_alpha()
        self.zero_value_pointer_hover_img = pygame.image.load(self.zero_value_pointer_hover_img).convert_alpha()
        self.value = float(0)
        self.pointer_width = self.pointer_img.get_width()
        self.pointer_height = self.pointer_img.get_height()
        self.step_value = 100/(((self.x1-self.x)+2)-self.pointer_width)
        self.pointer_x = self.x-1
        if defult_value != None:
            self.pointer_x = self.pointer_x+int(defult_value/self.step_value)
            self.value = defult_value
        self.pointer_y = (self.y + int(self.thickness/2))-int(self.pointer_height/2)
        self.move_pointer = False
        self.pointer_mouse_dis = 0
        self.font_size = self.thickness+15
        self.persentage_y = (self.y+(self.thickness/2))-(self.font_size/2+3)

    def collide(self, x, y):
        global PYIMG_MOUSE_COLLSISION_POINT_MASK
        if collision(PYIMG_MOUSE_COLLSISION_POINT_MASK, self.pointer_img_mask, x, y, self.pointer_x, self.pointer_y):
            return True
        else:
            return False

    def config_value(self, persentage):
        self.pointer_x = (self.x-1) + (int(persentage / self.step_value))
        self.value = persentage

    def place(self, events=None):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if events != None:
            if events.type == pygame.MOUSEBUTTONDOWN:
                if events.button == 1:
                    mouse_x, mouse_y = events.pos
                    if self.collide(mouse_x, mouse_y):
                        self.pointer_mouse_dis = mouse_x - self.pointer_x
                        self.move_pointer = True
            if events.type == pygame.MOUSEBUTTONUP:
                if events.button == 1:
                    self.move_pointer = False
        if self.move_pointer:
            if mouse_x-self.pointer_mouse_dis >= self.x and mouse_x-self.pointer_mouse_dis <= self.x1-self.pointer_width:
                self.pointer_x = mouse_x-self.pointer_mouse_dis
            if mouse_x-self.pointer_mouse_dis < self.x:
                self.pointer_x = self.x-1
            if mouse_x-self.pointer_mouse_dis > self.x1-self.pointer_width:
                self.pointer_x = self.x1-self.pointer_width+1
            self.value = (self.pointer_x - (self.x-1))*self.step_value
            if events == None:
                custom_out_text(self.surface, str(int(self.value)) + '%', self.x1 + 15, self.x1 + 45, self.persentage_y,
                                self.text_color, self.font_size, Font_Kollektif)

        if events == None:
            pygame.draw.rect(self.surface, self.non_filled_bar_color,
                             [self.x, self.y, self.x1 - self.x, self.thickness])
            pygame.draw.rect(self.surface, self.filled_bar_color, [self.x, self.y, self.pointer_x-self.x+2, self.thickness])

            if self.value <= 0:
                if self.move_pointer or self.collide(mouse_x, mouse_y):
                    self.surface.blit(self.zero_value_pointer_hover_img, [self.pointer_x, self.pointer_y])
                else:
                    self.surface.blit(self.zero_value_pointer_img, [self.pointer_x, self.pointer_y])
            else:
                if self.move_pointer or self.collide(mouse_x, mouse_y):
                    self.surface.blit(self.pointer_hover_img, [self.pointer_x, self.pointer_y])
                else:
                    self.surface.blit(self.pointer_img, [self.pointer_x, self.pointer_y])
