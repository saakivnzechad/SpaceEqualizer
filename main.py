import pygame
import random
import math
import soundfile as sf
import yaml
import os

pygame.init()

path = os.path.abspath('settings.yaml')
with open(path) as file:
    settings = yaml.load(file, Loader=yaml.FullLoader)

vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3

RES = settings['WIDTH'], settings['HEIGHT']
CENTER = vec2(RES[0] // 2, RES[1] // 2)

class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.1, 0.5)
        self.color = random.choice(settings['COLORS'])
        self.screen_pos = vec2(0, 0)
        self.size = 10

    @staticmethod
    def get_pos3d(scale_pos=35):
        angle = random.uniform(0, 2 * math.pi)
        radius = random.randrange(RES[1] // scale_pos, RES[1]) * scale_pos
        x = radius * math.sin(angle)
        y = radius * math.cos(angle)
        return vec3(x, y, settings['DISTANCE'])

    def update(self):

        self.pos3d.z -= self.vel * app.amplitude
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (settings['DISTANCE'] - self.pos3d.z) / (0.2 * self.pos3d.z)

        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(0.2)

        # mouse
        mouse_pos = CENTER - vec2(pygame.mouse.get_pos())
        self.screen_pos += mouse_pos

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))


class Starfield:
    def __init__(self, app):
        self.stars = [Star(app) for i in range(settings['NUMBER OF STARS'])]

    def run(self):
        [star.update() for star in self.stars]
        self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
        [star.draw() for star in self.stars]


class App:
    def __init__(self):
        pygame.font.init()
        pygame.mixer.music.load('audios/{}.wav'.format(settings['SONG NAME']))
        self.a = pygame.mixer.Sound('audios/{}.wav'.format(settings['SONG NAME']))
        self.data, self.samplerate = sf.read('audios/{}.wav'.format(settings['SONG NAME']))
        self.screen = pygame.display.set_mode(RES)
        self.alpha_surface = pygame.Surface(RES)
        self.alpha_surface.set_alpha(settings['TRAIL ALPHA'])
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 18)
        self.starfield = Starfield(self)
        self.deltaTime = 0
        self.deltaA = 0
        self.deltaB = 0
        self.fps = 0
        self.fps_text = ""
        self.audiotime = 0
        self.amplitude = 0
        self.sampler = (len(self.data) / self.a.get_length()) / 1000
        pygame.mixer.music.play(-1)

        print(self.data)

        print("length is: " + str(self.a.get_length()))

    def update_fps(self):
        self.fps = str(int(self.clock.get_fps()))
        self.fps_text = self.font.render(self.fps, 1, pygame.Color("white"))
        return self.fps_text

    def run(self):
        while True:
            self.audiotime = round(pygame.mixer.music.get_pos() * self.sampler)
            self.amplitude = abs(round((self.data[self.audiotime, 0] * 10), 4))
            print(self.audiotime)
            print(self.amplitude)
            # self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))
            self.screen.blit(self.update_fps(), (10, 0))
            self.starfield.run()

            pygame.display.flip()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()

            self.deltaA = pygame.time.get_ticks()
            self.deltaTime = (self.deltaA - self.deltaB) / 1000.0
            self.deltaB = self.deltaA

            self.clock.tick(settings['FRAMERATE'])


if __name__ == "__main__":
    app = App()
    app.run()
