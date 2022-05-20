import time
import Config
from Array_processing import ArrayProcessing
from Gen_Secondary import SecondaryElements
from Draw_Info import DrawInfo
from Sound_control import SoundControl
from Intro_sort import intro_sort
from Quick_sort import quick_sort
from Merge_sort import merge_sort
import pygame

pygame.init()
n = 150
min_v = -100
max_v = 100
sorting_algorithm = quick_sort
sorting_alg_name = "Quick Sort"
draw_info = DrawInfo()
lst_control = ArrayProcessing(draw_info.screen)
lst_control.generate_list(n, min_v, max_v)
sound = SoundControl()
running = True
sorting = False
ascending = True
is_sorted = {'flag': False, 'ascending': True}
clock = pygame.time.Clock()
box1 = SecondaryElements("Size:", ArrayProcessing.SIDE_PAD / 2, 170, draw_info.screen)
box2 = SecondaryElements("Max value:", DrawInfo.WIDTH / 2 - 100, 170, draw_info.screen)
box3 = SecondaryElements("Min value:", DrawInfo.WIDTH - 3 * ArrayProcessing.SIDE_PAD, 170, draw_info.screen)

while running:
    clock.tick(Config.FPS)
    if sorting:
        try:
            next(sorting_algorithm_generator)
            time.sleep(0.001)
        except StopIteration:
            is_sorted['flag'] = True
            sound.play_sounds("success")
            sorting = False
            sound.stop_sounds("sorting")
    else:
        draw_info.draw(sorting_alg_name, ascending)  # обнуляє фон та малює заголовки
        SecondaryElements.show(box1, box2, box3)  # малює прямокутники та текст до них
        SecondaryElements.draw_error(box1, box2, box3)  # залежить від .show
        lst_control.draw_list()  # малює стовпці
    if is_sorted['flag'] and is_sorted['ascending'] == ascending:
        SecondaryElements.output_success(draw_info.screen)  # напис про успішне сортування
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not sorting:
            if box1.input_rect.collidepoint(event.pos):
                SecondaryElements.set_colors([True, False, False], box1, box2,
                                             box3)  # встановлює колір на рамку, True- активний
                sound.play_sounds("mouse click")
            elif box2.input_rect.collidepoint(event.pos):
                SecondaryElements.set_colors([False, True, False], box1, box2, box3)
                sound.play_sounds("mouse click")
            elif box3.input_rect.collidepoint(event.pos):
                SecondaryElements.set_colors([False, False, True], box1, box2, box3)
                sound.play_sounds("mouse click")
            else:
                SecondaryElements.set_colors([False, False, False], box1, box2, box3)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                sound.play_sounds("press key")
                is_sorted['flag'] = False
                sound.stop_sounds("sorting")
                sorting = False
                if box1.is_data_correct():
                    n = int(box1.get_user_text())
                if box2.is_data_correct():
                    max_v = int(box2.get_user_text())
                if box3.is_data_correct():
                    min_v = int(box3.get_user_text())
                lst_control.generate_list(n, min_v, max_v)  # аргументи або залишаться за замовч або ні
            elif all([event.key == pygame.K_SPACE, not sorting]):
                if not is_sorted['flag'] or ascending != is_sorted['ascending']:
                    sound.play_sounds("press key")
                    sorting = True
                    is_sorted['flag'] = False  # словник для зберігання інформації про стан масиву
                    is_sorted['ascending'] = ascending  # для виведення напису про успішне сортування
                    sound.play_sounds("sorting")
                    sorting_algorithm_generator = sorting_algorithm(lst_control, ascending)
            elif all([event.key == pygame.K_a, not ascending, not sorting]):
                sound.play_sounds("press key")
                ascending = True
            elif all([event.key == pygame.K_d, ascending, not sorting]):
                sound.play_sounds("press key")
                ascending = False
            elif all([event.key == pygame.K_q, not sorting]):
                sound.play_sounds("press key")
                sorting_algorithm = quick_sort  # назва функції для генератора
                sorting_alg_name = "Quick sort"  # назва алгоритму для вивода на екран
            elif all([event.key == pygame.K_m, not sorting]):
                sound.play_sounds("press key")
                sorting_algorithm = merge_sort
                sorting_alg_name = "Merge sort"
            elif all([event.key == pygame.K_i, not sorting]):
                sound.play_sounds("press key")
                sorting_algorithm = intro_sort
                sorting_alg_name = "Intro sort"
            elif event.key in SecondaryElements.ALLOWED_BUTTONS and any(
                    SecondaryElements.is_active(box1, box2, box3)):  # чи є активна комірка
                self = [x for x in SecondaryElements.is_active(box1, box2, box3) if
                        x is not False]  # пошук активної комірки
                sound.play_sounds("press key")
                self[0].add_user_text(event.unicode) if len(
                    self[0].get_user_text()) < 5 else ""  # додавання символу якщо він не п'ятий і >
            elif event.key == pygame.K_BACKSPACE and any(SecondaryElements.is_active(box1, box2, box3)):
                self = [x for x in SecondaryElements.is_active(box1, box2, box3) if
                        x is not False]  # аналогічне видалення символу
                sound.play_sounds("press key")
                self[0].set_user_text(self[0].get_user_text()[:-1])
