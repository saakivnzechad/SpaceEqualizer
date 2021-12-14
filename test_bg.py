import pygame
import Tools.addition_tools as adt
import numpy as np
import taichi as ti
import taichi_glsl as ts
from taichi_glsl import vec2, vec3

ti.init(arch=ti.vulkan) # ti.cpu ti.vulcan ti.opengl ti.metal(macOS)
#load texture
texture = pygame.image.load('concrete.jpg')
texture_size = texture.get_size()[0]
texture_array = pygame.surfarray.array3d(texture).astype(np.float32) / 255


@ti.data_oriented
class PyShader:
    def __init__(self, app):
        self.app = app
        self.screen_array = np.full((width, height, 3), [0,0,0], np.uint8)
        # taichi fields
        self.screen_field = ti.Vector.field(3, ti.uint8, (width, height))
        self.texture_field = ti.Vector.field(3, ti.float32, texture.get_size())
        self.texture_field.from_numpy(texture_array)

    @ti.kernel
    def render(self, time: ti.float32):
        """fragment shader imitation"""
        for frag_coord in ti.grouped(self.screen_field):
            #normalized pixel coords
            uv = (frag_coord - 0.5 * resolution) / resolution.y
            col = vec3(0.0)
            # polar coords
            phi = ts.atan(uv.y, uv.x)
            rho = ts.length(uv)
            
            st = vec2(phi / ts.pi, 0.25 / rho)
            st.x += time / 14
            st.y += time / 2
            col += self.texture_field[st * texture_size]
            
            col *= rho + 0.1
            
            col = ts.clamp(col, 0.0, 1.0)
            
            self.screen_field[frag_coord.x, resolution.y - frag_coord.y] = col * 255
        
    def update(self):
        time = pygame.time.get_ticks() * 1e-03 # time in sec
        self.render(time)
        self.screen_array = self.screen_field.to_numpy()
        
    def draw(self):
        pygame.surfarray.blit_array(self.app.screen, self.screen_array)
        
    def run(self):
        self.update()
        self.draw()
        

class App:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((resolution))
        self.clock = pygame.time.Clock()
        self.shader = PyShader(self)
    
    def run(self):
        while True:
            self.shader.run()
            pygame.display.flip()
            
            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            self.clock.tick(settings['FRAMERATE'])
            pygame.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')
            
    
if __name__ == '__main__':
    parse_settings = adt.Parser('settings.yaml')
    settings = parse_settings.opened
    resolution = width, height = vec2(settings['WIDTH'], settings['HEIGHT'])
    app = App()
    app.run()