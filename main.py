import pygame
import random
import math
import soundfile as sf
import Tools.addition_tools as adt

pygame.init()


class Star:
    def __init__(self, app):
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
        self.pos3d.z -= self.vel * settings['SPEED'] * based.FindAmplitude(pygame.mixer.music.get_pos(), settings['AMPLITUDE COEFFICIENT'])[1]
        self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d

        self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
        self.size = (settings['DISTANCE'] - self.pos3d.z) / (settings['SIZE'] * self.pos3d.z)

        # rotate xy
        self.pos3d.xy = self.pos3d.xy.rotate(settings['ROTATION'] * based.FindAmplitude(pygame.mixer.music.get_pos(), settings['AMPLITUDE COEFFICIENT'])[1])

        # mouse
        mouse_pos = CENTER - vec2(pygame.mouse.get_pos())
        self.screen_pos += mouse_pos

    def draw(self):
        pygame.draw.rect(screen, self.color, (*self.screen_pos, self.size, self.size))


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
        self.alpha_surface = pygame.Surface(RES)
        self.alpha_surface.set_alpha(settings['TRAIL ALPHA'])
        self.clock = pygame.time.Clock()
        self.starfield = Starfield(self)
        pygame.mixer.music.play(-1)


    def run(self):
        while True:

            # self.screen.fill('black')
            screen.blit(self.alpha_surface, (0, 0))

            if settings['IS DEBUG MODE']: debug.showFPS(self.clock)

            self.starfield.run()

            pygame.display.flip()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    print(self.starfield.stars)
                    exit()

            self.clock.tick(settings['FRAMERATE'])


if __name__ == "__main__":

    parse_settings = adt.Parser('settings.yaml')
    settings = parse_settings.opened

    RES = settings['WIDTH'], settings['HEIGHT']
    global_font = pygame.font.SysFont("Arial", 18)
    screen = pygame.display.set_mode(RES)

    based = adt.Based(settings['SONG NAME'])
    if settings['IS DEBUG MODE']: debug = adt.DEBUG(pygame.mixer.Sound('audios/{}.wav'.format(settings['SONG NAME'])), global_font, screen)

    vec2, vec3 = pygame.math.Vector2, pygame.math.Vector3
    CENTER = vec2(RES[0] // 2, RES[1] // 2)

    app = App()
    app.run()
