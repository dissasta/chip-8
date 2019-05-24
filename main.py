import pygame
import sys

class UInt:
    def __init__(self, max, value):
        self._max = 2 ** max
        self._value = value % self._max

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value % self._max

class CPU:
    def __init__(self, rom):
        self.rom = rom
        self._init_gfx()
        self._init_variables()
        self._init_registers()
        self._init_ram()

    def _init_gfx(self):
        self.gfx_w = 64
        self.gfx_h = 32
        self.gfx_ram = [[0 for y in range(self.gfx_h)] for x in range(self.gfx_w)]

    def _init_variables(self):
        self._opcode = UInt(16, 0)
        self._opcode_name = None
        self._special_opcode = False
        self._cycle_count = 0

    def _init_registers(self):
        self._V = [UInt(16, 0) for x in range(16)]
        self._I = UInt(16, 0)
        self._PC = UInt(16, 512)
        self._DT = UInt(8, 0)
        self._ST = UInt(8, 0)
        self._stack = [UInt(16, 0) for x in range(16)]
        self._SP = UInt(16, 0)
        self._KEYS = [0 for x in range(16)]

    def _init_ram(self):
        self._ram = [UInt(16, 0) for x in range(4096)]
        self._load_fonts()
        self._load_rom()

    def _load_fonts(self):
        self._FONTS = [0xF0, 0x90, 0x90, 0x90, 0xF0, #0
                       0x20, 0x60, 0x20, 0x20, 0x70, #1
                       0xF0, 0x10, 0xF0, 0x80, 0xF0, #2
                       0xF0, 0x10, 0xF0, 0x10, 0xF0, #3
                       0x90, 0x90, 0xF0, 0x10, 0x10, #4
                       0xF0, 0x80, 0xF0, 0x10, 0xF0, #5
                       0xF0, 0x80, 0xF0, 0x90, 0xF0, #6
                       0xF0, 0x10, 0x20, 0x40, 0x40, #7
                       0xF0, 0x90, 0xF0, 0x90, 0xF0, #8
                       0xF0, 0x90, 0xF0, 0x10, 0xF0, #9
                       0xF0, 0x90, 0xF0, 0x90, 0x90, #A
                       0xE0, 0x90, 0xE0, 0x90, 0xE0, #B
                       0xF0, 0x80, 0x80, 0x80, 0xF0, #C
                       0xE0, 0x90, 0x90, 0x90, 0xE0, #D
                       0xF0, 0x80, 0xF0, 0x80, 0xF0, #E
                       0xF0, 0x80, 0xF0, 0x80, 0x80] #F

        for idx, byte in enumerate(self._FONTS, 80):
            self._ram[idx].value = byte

    def _load_rom(self):
        prog_data = len(self._ram) - self._PC.value
        data_stream = [byte for byte in self.rom.read(prog_data)]
        for idx, byte in enumerate(data_stream, self._PC.value):
            self._ram[idx].value = byte

    def key_pressed(self):
        keys = pygame.key.get_pressed()

        self._KEYS[0x1] = keys[pygame.K_1]
        self._KEYS[0x2] = keys[pygame.K_2]
        self._KEYS[0x3] = keys[pygame.K_3]
        self._KEYS[0x4] = keys[pygame.K_q]
        self._KEYS[0x5] = keys[pygame.K_w]
        self._KEYS[0x6] = keys[pygame.K_e]
        self._KEYS[0x7] = keys[pygame.K_a]
        self._KEYS[0x8] = keys[pygame.K_s]
        self._KEYS[0x9] = keys[pygame.K_d]
        self._KEYS[0xA] = keys[pygame.K_z]
        self._KEYS[0xB] = keys[pygame.K_c]
        self._KEYS[0xC] = keys[pygame.K_4]
        self._KEYS[0xD] = keys[pygame.K_r]
        self._KEYS[0xE] = keys[pygame.K_f]
        self._KEYS[0xF] = keys[pygame.K_v]
        self._KEYS[0x0] = keys[pygame.K_x]

    def _fetch_opcode(self):
        pass

    def _decode_opcode(self):
        pass

    def cycle(self):
        self._fetch_opcode()
        self._decode_opcode()

def main():
    rom = r'd:\PONG.ch8'
    rom = open(rom, "rb")
    core = CPU(rom)
    res = (core.gfx_w, core.gfx_h)
    scale = 20
    scaled_res = (res[0] * scale, res[1] * scale)
    clock = pygame.time.Clock()

    white = (255, 255, 255)
    black = (0, 0, 0)

    surface = pygame.Surface(res)
    screen = pygame.display.set_mode(scaled_res)

    while True:

        core.cycle()

        for x in range(core.gfx_w):
            for y in range(core.gfx_h):
                if core.gfx_ram[x][y] == 0:
                    surface.set_at((x, y), white)

        surface.fill(black)

        pygame.transform.scale(surface, scaled_res, screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #elif event.type == pygame.KEYDOWN:
            #    core.key_pressed(event)
        core.key_pressed()

        clock.tick()

if __name__ == "__main__":
    pygame.init()
    main()