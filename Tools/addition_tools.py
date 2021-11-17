import os.path
import yaml.loader
import pygame
import soundfile as sf


class Based:
    def __init__(self, song_path):
        self.deltaA = 0
        self.deltaB = 0
        self._deltaTime = 0
        self.sampling = 0
        self.a = pygame.mixer.Sound('audios/{}.wav'.format(song_path))
        self.data, self.samplerate = sf.read('audios/{}.wav'.format(song_path))

    def deltaTime(self, ticks):
        self.deltaA = ticks
        self._deltaTime = (self.deltaA - self.deltaB) / 1000.0
        self.deltaB = self.deltaA
        return self._deltaTime

    def FindSampling(self):
        self.sampling = round((len(self.data) / self.a.get_length() / 1000), 0)
        return self.sampling


class Parser:
    # initialize the class instance
    def __init__(self, local_path):
        self.i = None
        self.path = os.path.abspath(local_path)  # find full .yaml file path
        with open(self.path) as file:  # open .yaml file
            self.opened = yaml.load(file, Loader=yaml.FullLoader)  # parse .yaml file

    # getting needed variable from parsed .yaml file
    def get_state(self, name):
        if name in self.opened:  # check accordance of dict element with param
            return self.opened[name]  # returned if successful
        return 'nothing found'  # returned if error


class DEBUG:
    def __init__(self, song, font, screen):
        self.fps = 0
        self.seconds = 0
        self.fps_text = ""
        self.sampling_text = ""
        self.timer = ""
        self.time_text = ""
        self.font = font
        self.screen = screen
        self.all_timer_secs = int(round(song.get_length(), 0))
        self.all_timer = str(self.all_timer_secs // 60) + " : " + str(self.all_timer_secs - (60 * (self.all_timer_secs // 60)))

    def showFPS(self, clock):
        self.fps = "FPS:   " + str(int(clock.get_fps()))
        self.fps_text = self.font.render(self.fps, 1, pygame.Color("white"))
        self.screen.blit(self.fps_text, (10, 10))

    def showSampling(self, sampling):
        self.sampling_text = self.font.render(("sampling is:   " + str(int(sampling * 1000))), 1, pygame.Color('white'))
        self.screen.blit(self.sampling_text, (10, 40))

    def showTimer(self, mus_pos):
        self.seconds = int(round((mus_pos / 1000), 0))
        self.timer = str(self.seconds // 60) + " : " + str(self.seconds - (60 * (self.seconds // 60)))
        self.time_text = self.font.render(("time:   " + self.timer + "   of   " + self.all_timer), 1, pygame.Color('white'))
        self.screen.blit(self.time_text, (10, 70))

    def showWave(self, amplitude):
        self.wave_text = self.font.render(("wave amplitude:   " + str(round(amplitude, 2))), 1, pygame.Color('white'))
        self.screen.blit(self.wave_text, (10, 100))

    def showFrame(self, audiotime, data):
        self.longest_text = self.font.render(("frames:   " + str(audiotime) + " of " + str(len(data))), 1, pygame.Color('white'))
        self.screen.blit(self.longest_text, (10, 130))