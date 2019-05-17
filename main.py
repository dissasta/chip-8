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
        pass

    def _load_rom(self):
        prog_data = len(self._ram) - self._PC.value
        data_stream = [byte for byte in self.rom.read(prog_data)]
        for idx, byte in enumerate(data_stream, self._PC.value):
            self._ram[idx].value = byte

    def key_pressed(self, event):
        for i in range(len(self._KEYS)):
            self._KEYS[i] = 0

        if event.key == pygame.K_1:
            self._KEYS[0x1] = 1
        elif event.key == pygame.K_2:
            self._KEYS[0x2] = 1
        elif event.key == pygame.K_3:
            self._KEYS[0x3] = 1
        elif event.key == pygame.K_q:
            self._KEYS[0x4] = 1
        elif event.key == pygame.K_w:
            self._KEYS[0x5] = 1
        elif event.key == pygame.K_e:
            self._KEYS[0x6] = 1
        elif event.key == pygame.K_a:
            self._KEYS[0x7] = 1
        elif event.key == pygame.K_s:
            self._KEYS[0x8] = 1
        elif event.key == pygame.K_d:
            self._KEYS[0x9] = 1
        elif event.key == pygame.K_z:
            self._KEYS[0xa] = 1
        elif event.key == pygame.K_c:
            self._KEYS[0xb] = 1
        elif event.key == pygame.K_4:
            self._KEYS[0xc] = 1
        elif event.key == pygame.K_r:
            self._KEYS[0xd] = 1
        elif event.key == pygame.K_f:
            self._KEYS[0xe] = 1
        elif event.key == pygame.K_v:
            self._KEYS[0xf] = 1
        elif event.key == pygame.K_x:
            self._KEYS[0x0] = 1

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
            elif event.type == pygame.KEYDOWN:
                core.key_pressed(event)

        clock.tick()

if __name__ == "__main__":
    pygame.init()
    main()