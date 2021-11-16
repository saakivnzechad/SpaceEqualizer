import pygame
import random
import math
import soundfile as sf
import Tools.addition_tools as adt

pygame.init()



class Star:
    def __init__(self, app):
        self.screen = app.screen
        self.pos3d = self.get_pos3d()
        self.vel = random.uniform(0.1, 1.0)
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
        self.pos3d.z -= self.vel * settings['SPEED'] * app.amplitude
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (settings['DISTANCE'] - self.pos3d.z) / (settings['SIZE'] * self.pos3d.z)

        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(settings['ROTATION'] * app.amplitude)

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
        self.fps = 0
        self.fps_text = ""
        self.wave_text = ""
        self.audiotime = 0
        self.amplitude = 0
        self.all_timer_secs = int(round(self.a.get_length(), 0))
        self.all_timer = str(self.all_timer_secs // 60) + " : " + str(self.all_timer_secs - (60 * (self.all_timer_secs // 60)))
        self.sampling = (len(self.data) / self.a.get_length()) / 1000 + 1
        self.sampling_text = self.font.render(("sampling is:   " + str(int(self.sampling * 1000))), 1, pygame.Color('white'))
        pygame.mixer.music.play(-1)

        print(self.data)

        print("length is: " + str(self.a.get_length()))

    def DEBUG(self):
        self.fps = "FPS:   " + str(int(self.clock.get_fps()))
        self.fps_text = self.font.render(self.fps, 1, pygame.Color("white"))
        self.wave_text = self.font.render(("wave amplitude:   " + str(self.amplitude)), 1, pygame.Color('white'))
        self.longest_text = self.font.render(("frames:   " + str(self.audiotime) + " of " + str(len(self.data))), 1, pygame.Color('white'))
        self.seconds = int(round((pygame.mixer.music.get_pos() / 1000), 0))
        self.timer = str(self.seconds // 60) + " : " + str(self.seconds - (60 * (self.seconds // 60)))
        self.time_text = self.font.render(("time:   " + self.timer + "   of   " + self.all_timer), 1, pygame.Color('white'))
        return self.fps_text, self.wave_text, self.longest_text, self.time_text

    def run(self):
        while True:
            self.audiotime = round(pygame.mixer.music.get_pos() * self.sampling)
            self.amplitude = abs(round((self.data[self.audiotime, 0] * settings['AMPLITUDE COEFFICIENT']), 9))
            print(str(self.audiotime) + " : " + str(self.amplitude))
            # self.screen.fill('black')
            self.screen.blit(self.alpha_surface, (0, 0))

            if settings['IS DEBUG MODE']:
                self.screen.blit(self.DEBUG()[0], (10, 10))
                self.screen.blit(self.sampling_text, (10, 40))
                self.screen.blit(self.DEBUG()[1], (10, 70))
                self.screen.blit(self.DEBUG()[2], (10, 100))
                self.screen.blit(self.DEBUG()[3], (10, 130))

            self.starfield.run()

            pygame.display.flip()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()

            self.clock.tick(settings['FRAMERATE'])


if __name__ == "__main__":

    parse_settings = adt.Parser('settings.yaml')
    settings = parse_settings.opened
    based = adt.Based()

    vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
    RES = settings['WIDTH'], settings['HEIGHT']
    CENTER = vec2(RES[0] // 2, RES[1] // 2)

    app = App()
    app.run()
