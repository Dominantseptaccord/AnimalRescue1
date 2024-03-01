import pygame
import sys
import random
pygame.init()
win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pygame Adventure")
bg_sound = pygame.mixer.Sound("zad.mp3")
bg_sound.play()
font_title = pygame.font.SysFont('Times New Roman', 70)
sound_on = True
health = 100
wolf_x, wolf_y = -100, -100
sheep_x, sheep_y = 200,200
wolf_speed = 0
safe_sheeps = 0
bg = pygame.image.load("bg.jpg").convert()
bg = pygame.transform.scale(bg, (1280, 720))
size = (50, 100)
fence = pygame.image.load("fence.png").convert_alpha()
fence = pygame.transform.scale(fence,(400,400))
background_image = pygame.image.load("bgmenu.jpg")
sound1 = pygame.mixer.Sound("wolf-howl-sound.mp3")
sheeps = [
    {"x": 900, "y": 550, "speed": 2, "is_left": False, "is_right": False, "is_up": False, "is_down": False},
    {"x": 940, "y": 540, "speed": 2, "is_left": False, "is_right": False, "is_up": False, "is_down": False},
    {"x": 960, "y": 360, "speed": 1, "is_left": False, "is_right": False, "is_up": False, "is_down": False},
    {"x": 960, "y": 500, "speed": 1, "is_left": False, "is_right": False, "is_up": False, "is_down": False},
    {"x": 341, "y": 452, "speed": 1, "is_left": False, "is_right": False, "is_up": False, "is_down": False},
    {"x": random.randint(0, 1280 - 250), "y": 370, "speed": 1, "is_left": False, "is_right": False, "is_up": False, "is_down": False},
]
total_sheeps = len(sheeps)
wolf_appear_time = pygame.time.get_ticks() + 5000
wolf_is_visible = False
magic_stone_image = pygame.image.load('water.png')
magic_stone_image = pygame.transform.scale(magic_stone_image, (20, 20))
magic_stone_x, magic_stone_y = 450, 325
magic_stone_collected = False
magic_stone_rect = magic_stone_image.get_rect(topleft=(magic_stone_x, magic_stone_y))
walk_left = [pygame.transform.scale(pygame.image.load(f"l{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_right = [pygame.transform.scale(pygame.image.load(f"r{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_up = [pygame.transform.scale(pygame.image.load(f"u{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_down = [pygame.transform.scale(pygame.image.load(f"d{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_left1 = [pygame.transform.scale(pygame.image.load(f"el{i}.png").convert_alpha(), size) for i in range(1, 3)]
walk_right1 = [pygame.transform.scale(pygame.image.load(f"er{i}.png").convert_alpha(), size) for i in range(1, 3)]
walk_up1 = [pygame.transform.scale(pygame.image.load(f"eu{i}.png").convert_alpha(), size) for i in range(1, 3)]
walk_down1 = [pygame.transform.scale(pygame.image.load(f"ed{i}.png").convert_alpha(), size) for i in range(1, 3)]
walk_left2 = [pygame.transform.scale(pygame.image.load(f"sl{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_right2 = [pygame.transform.scale(pygame.image.load(f"sr{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_up2 = [pygame.transform.scale(pygame.image.load(f"sd{i}.png").convert_alpha(), size) for i in range(1, 5)]
walk_down2 = [pygame.transform.scale(pygame.image.load(f"su{i}.png").convert_alpha(), size) for i in range(1, 5)]
fence_rect = pygame.Rect(300, 200, 200, 50)
es = pygame.image.load("easy.png")
es = pygame.transform.scale(es, (50, 50))
md = pygame.image.load("middle.png")
md = pygame.transform.scale(md, (50, 50))
df = pygame.image.load("hard.png")
df = pygame.transform.scale(df, (50, 50))
x = 1200
y = 600
speed = 10
anim_count = 0
enim_count = 0
is_left = is_right = is_up = is_down = False
safe_zone_rect = pygame.Rect(550, 300, 50, 50)
clock = pygame.time.Clock()
run = True

font = pygame.font.SysFont('Arial', 50)
def find_nearest_sheep(wolf_x, wolf_y, sheeps):
    if not sheeps:
        return None
    nearest_sheep = min(sheeps, key=lambda sheep: ((sheep["x"] - wolf_x)**2 + (sheep["y"] - wolf_y)**2))
    return nearest_sheep
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)
def main_menu():
    global sound_on, wolf_speed, sheep_speed, wolf_appear_time
    difficulty = "Medium"
    while True:
        win.blit(background_image, (0, 0))
        draw_text('Спасение Животных', font_title, (255, 255, 255), win, 350, 100)
        draw_text('Старт', font, (255, 255, 255), win, 600, 250)
        draw_text('Звук', font, (255, 255, 255), win, 610, 350)
        draw_text('Выйти', font, (255, 255, 255), win, 595, 450)
        win.blit(es,(300,195))
        draw_text('Легкий', font, (255, 255, 255), win, 350, 190)
        win.blit(md, (525, 195))
        draw_text('Средний', font, (255, 255, 255), win, 575, 190)
        win.blit(df,(750,195))
        draw_text('Сложный', font, (255, 255, 255), win, 800, 190)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if 600 <= x <= 730 and 250 <= y <= 300:
                    return difficulty
                elif 610 <= x <= 780 and 350 <= y <= 400:
                    if sound_on:
                        bg_sound.stop()
                        sound_on = False
                    else:
                        bg_sound.play()
                        sound_on = True
                elif 595 <= x <= 710 and 450 <= y <= 550:
                    pygame.quit()
                    sys.exit()
                elif 350 <= x <= 450 and 190 <= y <= 300:  # Легкий
                    difficulty = "Easy"
                elif 575 <= x <= 750 and 190 <= y <= 400:  # Средний
                    difficulty = "Medium"
                elif 800 <= x <= 1100 and 190 <= y <= 550:  # Сложный
                    difficulty = "Hard"
        pygame.display.update()

difficulty_settings = {
    "Easy": {"wolf_speed": 1, "sheep_speed": 1, "wolf_appear_time": pygame.time.get_ticks() + 60000},
    "Medium": {"wolf_speed": 2, "sheep_speed": 5, "wolf_appear_time": pygame.time.get_ticks() + 30000},
    "Hard": {"wolf_speed": 5, "sheep_speed": 1, "wolf_appear_time": pygame.time.get_ticks() + 1000}
}
if __name__ == '__main__':
    if __name__ == '__main__':
        difficulty = main_menu()
        wolf_speed = difficulty_settings[difficulty]["wolf_speed"]
        sheep_speed = difficulty_settings[difficulty]["sheep_speed"]
        wolf_appear_time = difficulty_settings[difficulty]["wolf_appear_time"]
        if (bg_sound.play()): {
            sound1.play()
        }
        while run:
            clock.tick(45)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            # Main character
            if keys[pygame.K_LEFT]:
                x -= speed
                is_left = True
                is_right = is_up = is_down = False
            elif keys[pygame.K_RIGHT]:
                x += speed
                is_right = True
                is_left = is_up = is_down = False
            elif keys[pygame.K_UP]:
                y -= speed
                is_up = True
                is_left = is_right = is_down = False
            elif keys[pygame.K_DOWN]:
                y += speed
                is_down = True
                is_left = is_right = is_up = False
            else:
                is_right = is_left = is_up = is_down = False
                anim_count = 0

            anim_count += 1
            if anim_count + 1 >= 12:
                anim_count = 0
            win.blit(bg, (0, 0))
            win.blit(fence, (400, 1))
            # water
            if not magic_stone_collected:
                win.blit(magic_stone_image, (magic_stone_x, magic_stone_y))
                player_rect = pygame.Rect(x, y, size[0], size[1])

                # Ведро воды
                if player_rect.colliderect(magic_stone_rect):
                    magic_stone_collected = True
            if is_left:
                win.blit(walk_left[anim_count // 3], (x, y))
            elif is_right:
                win.blit(walk_right[anim_count // 3], (x, y))
            elif is_up:
                win.blit(walk_up[anim_count // 3], (x, y))
            elif is_down:
                win.blit(walk_down[anim_count // 3], (x, y))
            else:
                win.blit(walk_down[0], (x, y))

            current_time = pygame.time.get_ticks()
            wolf_is_right = wolf_is_up = wolf_is_down = wolf_is_left = False
            if not wolf_is_visible:
                if current_time >= wolf_appear_time:
                    wolf_is_visible = True  # Волк теперь виден
                    wolf_x, wolf_y = 100, 100  # Начальное положение волка после появления
                else:
                    # Текст обратного отсчета
                    remaining_time = max(0, (wolf_appear_time - current_time) // 1000)
                    countdown_text = font.render(f"WOLF WILL COME IN {remaining_time} SEC", True, (255, 0, 0))
                    win.blit(countdown_text, (500, 20))
            target_sheep = find_nearest_sheep(wolf_x, wolf_y, sheeps)
            if wolf_is_visible:
                if target_sheep:
                    # Сбросить направления движения волка
                    wolf_is_left = wolf_is_right = wolf_is_up = wolf_is_down = False

                    sheep_x, sheep_y = target_sheep["x"], target_sheep["y"]
                    # горизонтальное направление движения волка
                    if wolf_x < sheep_x:
                        wolf_x += wolf_speed
                        wolf_is_right = True
                    elif wolf_x > sheep_x:
                        wolf_x -= wolf_speed
                        wolf_is_left = True

                    # вертикальное направление движения волка
                    if wolf_y < sheep_y:
                        wolf_y += wolf_speed
                        wolf_is_down = True
                    elif wolf_y > sheep_y:
                        wolf_y -= wolf_speed
                        wolf_is_up = True

                    if abs(wolf_x - sheep_x) < 10 and abs(wolf_y - sheep_y) < 10:
                        sheeps.remove(target_sheep)
            clock.tick(60)
            enim_count += 1
            if enim_count + 1 >= 6:
                enim_count = 0
            if wolf_is_left:
                win.blit(walk_left1[enim_count // 3], (wolf_x, wolf_y))
            elif wolf_is_right:
                win.blit(walk_right1[enim_count // 3], (wolf_x, wolf_y))
            elif wolf_is_up:
                win.blit(walk_up1[enim_count // 3], (wolf_x, wolf_y))
            elif wolf_is_down:
                win.blit(walk_down1[enim_count // 3], (wolf_x, wolf_y))
            else:
                win.blit(walk_down1[0], (wolf_x, wolf_y))
            sheep_is_left = sheep_is_right = sheep_is_up = sheep_is_down = False
            safe_distance = 150  # Безопасное расстояние от волка
            sheep_speed = 1  # РЕДАКТИРОВАТЬ
            sheep_follow_distance = 100  # овца начинает следовать за игроком
            safe_distance_from_wolf = 150  # расстояние от волка

            # Расчет расстояний
            for sheep in sheeps:
                distance_to_player = ((sheep["x"] - x) ** 2 + (sheep["y"] - y) ** 2) ** 0.5
                distance_to_wolf = ((sheep["x"] - wolf_x) ** 2 + (sheep["y"] - wolf_y) ** 2) ** 0.5

                # Сброс направлений движения овцы
                sheep["is_left"] = sheep["is_right"] = sheep["is_up"] = sheep["is_down"] = False
                sheep_is_left = sheep_is_right = sheep_is_up = sheep_is_down = False
                # Логика движения овцы
                if distance_to_wolf < safe_distance_from_wolf:
                    if sheep["x"] < wolf_x:
                        sheep["x"] -= sheep["speed"]
                        sheep["is_left"] = True
                    else:
                        sheep["x"] += sheep["speed"]
                        sheep["is_right"] = True
                    if sheep["y"] < wolf_y:
                        sheep["y"] -= sheep["speed"]
                        sheep["is_up"] = True
                    else:
                        sheep["y"] += sheep["speed"]
                        sheep["is_down"] = True
                elif magic_stone_collected and distance_to_player <= sheep_follow_distance:
                    if sheep["x"] < x:
                        sheep["x"] += sheep["speed"]
                        sheep["is_right"] = True
                    elif sheep["x"] > x:
                        sheep["x"] -= sheep["speed"]
                        sheep["is_left"] = True
                    if sheep["y"] < y:
                        sheep["y"] += sheep["speed"]
                        sheep["is_down"] = True
                    elif sheep["y"] > y:
                        sheep["y"] -= sheep["speed"]
                        sheep["is_up"] = True
                elif distance_to_player < safe_distance_from_wolf:
                    if sheep["x"] < x:
                        sheep["x"] -= sheep["speed"]
                        sheep["is_left"] = True
                    else:
                        sheep["x"] += sheep["speed"]
                        sheep["is_right"] = True
                    if sheep["y"] < y:
                        sheep["y"] -= sheep["speed"]
                        sheep["is_up"] = True
                    else:
                        sheep["y"] += sheep["speed"]
                        sheep["is_down"] = True
                if sheep["is_up"]:
                    win.blit(walk_up2[enim_count // 3], (sheep["x"], sheep["y"]))
                elif sheep["is_down"]:
                    win.blit(walk_down2[enim_count // 3], (sheep["x"], sheep["y"]))
                elif sheep["is_left"]:
                    win.blit(walk_left2[enim_count // 3], (sheep["x"], sheep["y"]))
                elif sheep["is_right"]:
                    win.blit(walk_right2[enim_count // 3], (sheep["x"], sheep["y"]))
                else:
                    win.blit(walk_down2[0], (sheep["x"], sheep["y"]))  # Показать овцу стоящей, если нет движения
                sheep_rect = pygame.Rect(sheep["x"], sheep["y"], size[0], size[1])
                for sheep in sheeps[:]:  # Используем копию списка, чтобы избежать ошибок во время итерации
                    sheep_rect = pygame.Rect(sheep["x"], sheep["y"], size[0], size[1])

                    # Проверка столкновения овцы с безопасной зоной
                    if sheep_rect.colliderect(safe_zone_rect):
                        safe_sheeps += 1  # Увеличиваем счетчик безопасных овец
                        sheeps.remove(sheep)  # Удаляем овцу из списка

                    # Проверка условия выигрыша: все овцы в безопасной зоне
                    if safe_sheeps == 6:
                        print("Congratulations! You saved all the sheep!")
                        run = False

                    # Проверка условия проигрыша: волк съел достаточно много овец
                    if total_sheeps - safe_sheeps - len(sheeps) >= 3:  # Если волк съел 3 или более овцы
                        print("You lose! The wolf got too many sheeps.")
                        run = False

            if abs(wolf_x - x) < 10 and abs(wolf_y - y) < 10:
                health -= 1
                if health <= 0:
                    print("You lose!")
                    run = False
            pygame.display.update()
        pygame.quit()
