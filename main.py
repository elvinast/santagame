import math
import random
from pgzero.builtins import Actor, keyboard, keys, sounds
from pygame import Rect
import pgzrun

# ------------------ WINDOW SETTINGS ------------------
WIDTH, HEIGHT = 800, 600

# ------------------ GAME STATES ------------------
is_menu = True
is_running = False
is_lost = False
is_won = False
sound_on = True

# ------------------ UI ELEMENTS ------------------
btn_start = Rect(WIDTH//2 - 100, HEIGHT//2 - 80, 200, 50)
btn_sound = Rect(WIDTH//2 - 100, HEIGHT//2 - 10, 200, 50)
btn_exit  = Rect(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50)

# ------------------ GLOBAL VARIABLES ------------------
points = 0
total_items = 0
frame_tick = 0
active_music = None

# game objects
platform_list = []
enemy_list = []
gift_list = []

# ------------------ CLASSES ------------------

class Santa:
    def __init__(self):
        self.animations = {
            "idle_r": ["santa_idle1", "santa_idle2"],
            "idle_l": ["santa_idle1_left", "santa_idle2_left"],
            "walk_r": ["santa_walk1", "santa_walk2"],
            "walk_l": ["santa_walk1_left", "santa_walk2_left"],
            "jump_r": ["santa_jump"],
            "jump_l": ["santa_jump_left"],
        }
        self.pose = "idle_r"
        self.index = 0
        self.sprite = Actor(self.animations[self.pose][0], (60, HEIGHT-100))

        self.vy = 0
        self.jump_strength = 15
        self.gravity = 0.8
        self.speed = 5
        self.facing_right = True
        self.on_ground = False
        self.anim_counter = 0

    def physics(self, platforms):
        moving = False

        if keyboard.left:
            self.sprite.x -= self.speed
            self.facing_right = False
            self.pose = "walk_l" if self.on_ground else "jump_l"
            moving = True

        elif keyboard.right:
            self.sprite.x += self.speed
            self.facing_right = True
            self.pose = "walk_r" if self.on_ground else "jump_r"
            moving = True

        if not moving and self.on_ground:
            self.pose = "idle_r" if self.facing_right else "idle_l"

        if keyboard.space and self.on_ground:
            self.vy = -self.jump_strength
            self.on_ground = False
            self.pose = "jump_r" if self.facing_right else "jump_l"
            if sound_on:
                try:
                    sounds.jump.play()
                except:
                    pass

        self.vy += self.gravity
        self.sprite.y += self.vy

        self.sprite.x = max(30, min(WIDTH - 30, self.sprite.x))
        self.on_ground = False

        # Collision with platforms
        for p in platforms:
            if self.sprite.colliderect(p.rect):
                if self.vy > 0 and self.sprite.bottom <= p.rect.bottom:
                    self.sprite.bottom = p.rect.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0 and self.sprite.top >= p.rect.top:
                    self.sprite.top = p.rect.bottom
                    self.vy = 0

        return self.sprite.top > HEIGHT  # fell below screen

    def animate(self):
        if "jump" in self.pose:
            self.sprite.image = self.animations[self.pose][0]
        else:
            self.index = (self.index + 1) % len(self.animations[self.pose])
            self.sprite.image = self.animations[self.pose][self.index]

    def draw(self):
        self.sprite.draw()


class Platform:
    def __init__(self, x, y, w):
        self.rect = Rect(x, y, w, 20)
        self.color = (90, 200, 250)

    def draw(self):
        screen.draw.filled_rect(self.rect, self.color)
        screen.draw.rect(self.rect, (255, 255, 255))


class Grinch:
    def __init__(self, x, y, left, right, img):
        self.frames = [img]
        self.sprite = Actor(img, (x, y - 30))
        self.left, self.right = left, right
        self.speed = 1.5
        self.dir = 1

    def update(self):
        self.sprite.x += self.speed * self.dir
        if self.sprite.x >= self.right:
            self.dir = -1
        elif self.sprite.x <= self.left:
            self.dir = 1

    def draw(self):
        self.sprite.draw()


class Snowman:
    def __init__(self, x, y):
        self.sprite = Actor("snowman", (x, y))
        self.start_x, self.start_y = x, y
        self.timer = random.uniform(0, math.pi * 2)

    def update(self):
        self.timer += 0.03
        self.sprite.x = self.start_x + math.cos(self.timer) * 100
        self.sprite.y = self.start_y + math.sin(self.timer * 1.5) * 30

    def draw(self):
        self.sprite.draw()


class Gift:
    def __init__(self, x, y):
        self.sprite = Actor("gift", (x, y - 20))
        self.offset = 0
        self.t = random.uniform(0, math.pi * 2)

    def update(self):
        self.t += 0.1
        self.offset = math.sin(self.t) * 5

    def draw(self):
        screen.blit(self.sprite.image,
                    (self.sprite.x - self.sprite.width // 2,
                     self.sprite.y - self.sprite.height // 2 + self.offset))

# ------------------ MAIN FUNCTIONS ------------------

def play_music(track):
    global active_music
    if sound_on:
        try:
            if active_music:
                active_music.stop()
            active_music = getattr(sounds, track)
            active_music.play(-1)
        except:
            pass


def switch_sound():
    global sound_on
    sound_on = not sound_on
    if not sound_on and active_music:
        active_music.stop()
    elif sound_on:
        play_music("menu_music")


def build_level():
    global platform_list, enemy_list, gift_list, total_items

    platform_list.clear()
    enemy_list.clear()
    gift_list.clear()

    p = platform_list.append
    p(Platform(0, HEIGHT - 50, WIDTH))
    p(Platform(150, 470, 180))
    p(Platform(380, 420, 200))
    p(Platform(70, 370, 150))
    p(Platform(320, 320, 180))
    p(Platform(550, 370, 180))
    p(Platform(600, 270, 150))
    p(Platform(250, 220, 200))
    p(Platform(500, 170, 180))

    enemy_list.append(Grinch(450, 420, 400, 560, "grinch1"))
    enemy_list.append(Grinch(380, 320, 340, 480, "grinch2"))
    enemy_list.append(Snowman(600, 250))

    locations = [
        (200, 470), (480, 420), (150, 370), (400, 320), (650, 370),
        (680, 270), (330, 220), (580, 170), (350, 420), (120, 320)
    ]
    count = random.randint(3, 10)
    for x, y in random.sample(locations, count):
        gift_list.append(Gift(x, y))
    total_items = len(gift_list)


def begin_game():
    global is_running, is_menu, is_lost, is_won, points, santa, frame_tick
    is_menu = False
    is_running = True
    is_lost = False
    is_won = False
    points = 0
    frame_tick = 0

    santa = Santa()
    build_level()
    play_music("game_music")


def update():
    global is_lost, is_won, frame_tick, points

    frame_tick += 1
    if is_menu or is_lost or is_won:
        return

    # hero physics
    fell = santa.physics(platform_list)
    if fell:
        end_game(lost=True)
        return

    # enemies
    for e in enemy_list:
        e.update()
        if e.sprite.colliderect(santa.sprite):
            end_game(lost=True)
            return

    # gifts
    for g in gift_list[:]:
        g.update()
        if g.sprite.colliderect(santa.sprite):
            gift_list.remove(g)
            points += 1
            if sound_on:
                try:
                    sounds.coin.play()
                except:
                    pass
            if points >= total_items:
                end_game(won=True)
                return

    if frame_tick % 10 == 0:
        santa.animate()


def end_game(lost=False, won=False):
    global is_lost, is_won
    is_lost, is_won = lost, won
    if active_music:
        active_music.stop()
    if sound_on:
        try:
            (sounds.gameover if lost else sounds.win).play()
        except:
            pass


def draw():
    screen.clear()
    if is_menu:
        draw_menu()
    elif is_running:
        draw_game()


def draw_menu():
    screen.blit("background_game", (0, 0))

    # moving snow dots
    for i in range(15):
        x = (i * 60 + frame_tick) % WIDTH
        y = (i * 40) % HEIGHT
        screen.draw.filled_circle((x, y), 3, (255, 255, 255))

    screen.draw.text("SANTA'S GIFT DELIVERY", center=(WIDTH//2, 80),
                     fontsize=48, color=(26, 52, 255))
    screen.draw.text("Collect all gifts to win!", center=(WIDTH//2, 150),
                     fontsize=28, color=(26, 52, 255))

    border = Rect(btn_exit.x, btn_exit.y, btn_exit.width, btn_exit.height)

    # buttons
    for rect, label in [(btn_start, "START GAME"),
                        (btn_sound, f"SOUND: {'ON' if sound_on else 'OFF'}"),
                        (btn_exit, "EXIT")]:
        screen.draw.filled_rect(rect, (30, 144, 255))
        screen.draw.rect(border, (255, 255, 255))
        screen.draw.text(label, center=rect.center, fontsize=26, color="white")

    screen.draw.text("Arrow Keys = Move    SPACE = Jump",
                     center=(WIDTH//2, HEIGHT - 50),
                     fontsize=22, color=(255, 255, 200))


def draw_game():
    screen.blit("background_game", (0, 0))

    for p in platform_list:
        p.draw()
    for g in gift_list:
        g.draw()
    for e in enemy_list:
        e.draw()
    santa.draw()

    screen.draw.text(f"Gifts: {points}/{total_items}",
                     (10, 10), fontsize=32, color=(26, 52, 255))

    if is_lost or is_won:
        overlay = Rect(150, 200, 500, 200)
        screen.draw.filled_rect(overlay, (201, 223, 254))
        msg = "YOU WON!" if is_won else "GAME OVER!"
        text2 = "All gifts delivered!" if is_won else f"Gifts: {points}/{total_items}"
        screen.draw.text(msg, center=(WIDTH//2, HEIGHT//2 - 40),
                         fontsize=60, color=(26, 52, 255))
        screen.draw.text(text2, center=(WIDTH//2, HEIGHT//2 + 20),
                         fontsize=32, color=(26, 52, 255))
        screen.draw.text("Press ENTER to menu",
                         center=(WIDTH//2, HEIGHT//2 + 60),
                         fontsize=24, color=(26, 52, 255))


def on_mouse_down(pos):
    global is_menu
    if is_menu:
        if btn_start.collidepoint(pos):
            begin_game()
        elif btn_sound.collidepoint(pos):
            switch_sound()
        elif btn_exit.collidepoint(pos):
            exit()


def on_key_down(key):
    global is_menu, is_running, is_lost, is_won
    if (is_lost or is_won) and key == keys.RETURN:
        is_menu, is_running, is_lost, is_won = True, False, False, False
        play_music("menu_music")


santa = Santa()
if sound_on:
    play_music("menu_music")

pgzrun.go()
