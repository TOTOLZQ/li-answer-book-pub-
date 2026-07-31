from M5 import Display
import M5
import random
import time

class Config:
    SCREEN_WIDTH = 240
    SCREEN_HEIGHT = 135
    CENTER_X = 120
    CENTER_Y = 67
    TITLE_Y = 6
    CONTENT_Y = 52
    HINT_Y = 110
    BOOT_FADE_STEPS = 20
    BOOT_FADE_DELAY_MS = 40
    SHUFFLE_COUNT = 12
    SHUFFLE_DELAY_MS = 50
    MULTI_CLICK_MS = 400

class Colors:
    BG = 0x000000
    BORDER = 0x2A2A2A
    GOLD = 0xD4AF37
    GOLD_LIGHT = 0xF0D878
    GREEN = 0x90EE90
    ORANGE = 0xFFA500
    RED = 0xFF4444
    GRAY_LIGHT = 0x999999
    GRAY_MID = 0x666666
    GRAY_DARK = 0x444444
    LINE = 0x333333
    LINE_DIM = 0x1A1A1A
    HINT = 0x555555
    WHITE = 0xFFFFFF

class Lang:
    ZH = 0
    EN = 1

class PageType:
    MENU = 0
    GAME = 1

class AnimPhase:
    NONE = 0
    BOOT_FADE = 1
    SHUFFLE = 2

class ModeType:
    ANSWER_BOOK = 0
    COIN = 1
    DICE = 2
    FORTUNE = 3
    NUMBER = 4

ModeNames = [
    "答案之书",
    "抛硬币",
    "掷色子",
    "今日运势",
    "幸运数字",
]

ModeNames_EN = [
    "Book of Answers",
    "Coin Flip",
    "Roll Dice",
    "Fortune",
    "Lucky Number",
]

Strings = {
    "menu_title": ["选择玩法", "Select Game"],
    "menu_hint": ["1切 2进 3语", "1:Nxt 2:Ent 3:Lang"],
    "answer_title": ["答案之书", "Book of Answers"],
    "answer_subtitle": ["书中写道", "The book says"],
    "answer_prompt": ["想一想你的问题", "Think of your question"],
    "coin_title": ["抛硬币", "Coin Flip"],
    "dice_title": ["掷色子", "Roll Dice"],
    "fortune_title": ["今日运势", "Fortune"],
    "number_title": ["幸运数字", "Lucky Number"],
    "game_hint_idle": ["1开 2回 3语", "1:Go 2:Bk 3:Lang"],
    "game_hint_result": ["1再 2回 3语", "1:Again 2:Bk 3:Lang"],
}

ANSWERS = [
    "相信自己的直觉", "现在不是时候", "答案是肯定的", "答案是否定的",
    "再等等看", "跟随你的心", "机会来了", "保持耐心",
    "做出改变", "顺其自然", "勇敢尝试", "不要犹豫",
    "相信过程", "事情会好转", "听从建议", "保持乐观",
    "重新考虑", "会有惊喜", "专注当下", "一切都会好的",
    "放手一搏", "保持沉默", "主动出击", "等待时机",
    "换个角度想", "你已经知道答案", "不要回头", "继续前进",
    "倾听内心", "答案就在眼前", "别想太多", "相信命运",
    "需要勇气", "好好休息", "放下执念", "珍惜当下",
    "大胆去爱", "学会拒绝", "守住底线", "回归初心",
    "不必强求", "时间会证明", "迈出第一步", "听从直觉",
    "保持热爱", "拥抱变化", "放过自己", "去做就好",
    "相信奇迹", "答案在你心中",
]

ANSWERS_EN = [
    "Trust your intuition", "Not now", "Yes", "No",
    "Wait and see", "Follow your heart", "Opportunity knocks", "Be patient",
    "Make a change", "Go with the flow", "Be brave", "Do not hesitate",
    "Trust the process", "Things will get better", "Take advice", "Stay optimistic",
    "Reconsider", "A surprise awaits", "Focus on now", "Everything will be fine",
    "Take the leap", "Stay silent", "Take initiative", "Wait for the right time",
    "Think differently", "You already know", "Do not look back", "Keep moving",
    "Listen to your heart", "The answer is near", "Do not overthink", "Trust fate",
    "Courage needed", "Rest well", "Let it go", "Cherish the moment",
    "Love boldly", "Learn to say no", "Hold your ground", "Return to basics",
    "Do not force it", "Time will tell", "Take the first step", "Trust your gut",
    "Stay passionate", "Embrace change", "Forgive yourself", "Just do it",
    "Believe in miracles", "The answer is within you",
]

FORTUNES = [
    ("大吉", Colors.GOLD),
    ("吉", Colors.GREEN),
    ("中平", Colors.WHITE),
    ("凶", Colors.ORANGE),
    ("大凶", Colors.RED),
]

FORTUNES_EN = [
    ("Great Luck", Colors.GOLD),
    ("Good Luck", Colors.GREEN),
    ("Neutral", Colors.WHITE),
    ("Bad Luck", Colors.ORANGE),
    ("Very Bad Luck", Colors.RED),
]

class AppState:
    def __init__(self):
        self.lang = Lang.ZH
        self.current_page = PageType.MENU
        self.current_mode = ModeType.ANSWER_BOOK
        self.menu_index = 0
        self.result_value = None
        self.shuffle_values = []
        self.click_count = 0
        self.first_click_ms = 0
        self.anim_phase = AnimPhase.NONE
        self.anim_step = 0
        self.anim_last_ms = 0

    def reset_click(self):
        self.click_count = 0
        self.first_click_ms = 0

    def start_anim(self, phase):
        self.anim_phase = phase
        self.anim_step = 0
        self.anim_last_ms = time.ticks_ms()

state = AppState()

def t(key):
    return Strings[key][state.lang]

def get_mode_names():
    return ModeNames_EN if state.lang == Lang.EN else ModeNames

def get_answers():
    return ANSWERS_EN if state.lang == Lang.EN else ANSWERS

def get_coin_values():
    return ["Heads", "Tails"] if state.lang == Lang.EN else ["正面", "反面"]

def get_fortunes():
    return FORTUNES_EN if state.lang == Lang.EN else FORTUNES

def interpolate_color(c1, c2, ratio):
    r = int(((c1 >> 16) & 0xFF) * (1 - ratio) + ((c2 >> 16) & 0xFF) * ratio)
    g = int(((c1 >> 8) & 0xFF) * (1 - ratio) + ((c2 >> 8) & 0xFF) * ratio)
    b = int((c1 & 0xFF) * (1 - ratio) + (c2 & 0xFF) * ratio)
    return (r << 16) | (g << 8) | b

def draw_centered_text(text, y, color=Colors.GOLD, bg=Colors.BG):
    Display.setTextColor(color, bg)
    w = Display.textWidth(text)
    Display.setCursor((Config.SCREEN_WIDTH - w) // 2, y)
    Display.print(text)

def draw_card_border(color=Colors.BORDER):
    Display.drawRoundRect(1, 1, 238, 133, 6, color)

def draw_title(text, color=Colors.GOLD):
    draw_centered_text(text, Config.TITLE_Y, color=color)

def draw_hint(text, color=Colors.HINT):
    draw_centered_text(text, Config.HINT_Y, color=color)

def draw_status_bar():
    text = "EN" if state.lang == Lang.EN else "中"
    Display.setTextColor(Colors.GRAY_MID, Colors.BG)
    Display.setCursor(Config.SCREEN_WIDTH - 44, Config.TITLE_Y)
    Display.print(text)

def draw_menu():
    Display.clear(Colors.BG)
    draw_card_border()
    draw_title(t("menu_title"))
    count = len(ModeNames)
    idx = state.menu_index
    names = get_mode_names()
    for i in range(3):
        item_idx = (idx + i - 1) % count
        y = 38 + i * 24
        if i == 1:
            Display.fillRoundRect(30, y - 4, 180, 24, 4, Colors.GRAY_DARK)
            color = Colors.GOLD
        else:
            color = Colors.GRAY_MID
        draw_centered_text(names[item_idx], y, color=color)
    Display.drawLine(230, 36, 230, 84, Colors.GRAY_DARK)
    dot_y = 36 + int(idx * 48 / (count - 1))
    Display.fillCircle(230, dot_y, 2, Colors.GOLD)
    draw_hint(t("menu_hint"))
    draw_status_bar()

def draw_answer_book(value=None):
    Display.clear(Colors.BG)
    draw_card_border()
    draw_title(t("answer_title"))
    if value is None:
        draw_centered_text(t("answer_prompt"), Config.CONTENT_Y, color=Colors.GRAY_LIGHT)
        draw_hint(t("game_hint_idle"))
    else:
        draw_centered_text(t("answer_subtitle"), 30, color=Colors.GRAY_MID)
        draw_centered_text(get_answers()[value], Config.CONTENT_Y, color=Colors.GOLD)
        draw_hint(t("game_hint_result"))
    draw_status_bar()

def draw_coin(value=None):
    Display.clear(Colors.BG)
    draw_card_border()
    draw_title(t("coin_title"))
    cx = Config.CENTER_X
    cy = 64
    r = 36
    if value is None:
        inner_color = Colors.GOLD
        text = "?"
        text_color = Colors.BG
    else:
        text = get_coin_values()[value]
        if value == 0:
            inner_color = Colors.GOLD_LIGHT
            text_color = Colors.BG
        else:
            inner_color = Colors.GRAY_MID
            text_color = Colors.WHITE
    Display.fillCircle(cx, cy, r, Colors.GOLD)
    Display.fillCircle(cx, cy, r - 4, inner_color)
    draw_centered_text(text, cy - 10, color=text_color)
    draw_hint(t("game_hint_result") if value is not None else t("game_hint_idle"))
    draw_status_bar()

def draw_dice(value=None):
    Display.clear(Colors.BG)
    draw_card_border()
    draw_title(t("dice_title"))
    x = Config.CENTER_X - 20
    y = Config.CONTENT_Y - 10
    Display.drawRoundRect(x, y, 40, 40, 4, Colors.GRAY_LIGHT)
    if value is not None:
        draw_dice_dots(value, x + 20, y + 20, 16)
    draw_hint(t("game_hint_result") if value is not None else t("game_hint_idle"))
    draw_status_bar()

def draw_dice_dots(value, cx, cy, spacing):
    positions = [
        (-1, -1), (0, -1), (1, -1),
        (-1, 0), (0, 0), (1, 0),
        (-1, 1), (0, 1), (1, 1),
    ]
    dot_map = {
        1: [4],
        2: [0, 8],
        3: [0, 4, 8],
        4: [0, 2, 6, 8],
        5: [0, 2, 4, 6, 8],
        6: [0, 2, 3, 5, 6, 8],
    }
    r = 4
    for i in dot_map[value]:
        dx, dy = positions[i]
        Display.fillCircle(cx + dx * spacing, cy + dy * spacing, r, Colors.GOLD)

def draw_fortune(value=None):
    Display.clear(Colors.BG)
    draw_card_border()
    draw_title(t("fortune_title"))
    if value is None:
        draw_centered_text("?", Config.CONTENT_Y, color=Colors.GRAY_MID)
    else:
        text, color = get_fortunes()[value]
        draw_centered_text(text, Config.CONTENT_Y, color=color)
    draw_hint(t("game_hint_result") if value is not None else t("game_hint_idle"))
    draw_status_bar()

def draw_number(value=None):
    Display.clear(Colors.BG)
    draw_card_border()
    draw_title(t("number_title"))
    if value is None:
        text = "?"
        color = Colors.GRAY_MID
    else:
        text = str(value)
        color = Colors.GOLD
    draw_centered_text(text, Config.CONTENT_Y, color=color)
    draw_hint(t("game_hint_result") if value is not None else t("game_hint_idle"))
    draw_status_bar()

def draw_current_mode(value=None):
    mode = state.current_mode
    if mode == ModeType.ANSWER_BOOK:
        draw_answer_book(value)
    elif mode == ModeType.COIN:
        draw_coin(value)
    elif mode == ModeType.DICE:
        draw_dice(value)
    elif mode == ModeType.FORTUNE:
        draw_fortune(value)
    elif mode == ModeType.NUMBER:
        draw_number(value)

def anim_boot_fade_tick(now):
    if time.ticks_diff(now, state.anim_last_ms) < Config.BOOT_FADE_DELAY_MS:
        return
    step = state.anim_step
    if step >= Config.BOOT_FADE_STEPS:
        draw_menu()
        state.anim_phase = AnimPhase.NONE
        return
    half = Config.BOOT_FADE_STEPS // 2
    if step < half:
        Display.fillRect(0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Colors.WHITE)
    else:
        ratio = (step - half) / half
        color = interpolate_color(Colors.WHITE, Colors.BG, ratio)
        Display.fillRect(0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, color)
    state.anim_step += 1
    state.anim_last_ms = now

def anim_shuffle_tick(now):
    if time.ticks_diff(now, state.anim_last_ms) < Config.SHUFFLE_DELAY_MS:
        return
    step = state.anim_step
    if step >= len(state.shuffle_values):
        state.result_value = state.shuffle_values[-1]
        state.anim_phase = AnimPhase.NONE
        draw_current_mode(state.result_value)
        return
    draw_current_mode(state.shuffle_values[step])
    state.anim_step += 1
    state.anim_last_ms = now

def animate_tick(now):
    phase = state.anim_phase
    if phase == AnimPhase.BOOT_FADE:
        anim_boot_fade_tick(now)
    elif phase == AnimPhase.SHUFFLE:
        anim_shuffle_tick(now)

def generate_shuffle_values():
    mode = state.current_mode
    if mode == ModeType.ANSWER_BOOK:
        count = len(get_answers())
        result = random.randint(0, count - 1)
        values = [random.randint(0, count - 1) for _ in range(Config.SHUFFLE_COUNT)]
        values.append(result)
        return values
    elif mode == ModeType.COIN:
        result = random.randint(0, 1)
        values = [random.randint(0, 1) for _ in range(Config.SHUFFLE_COUNT)]
        values.append(result)
        return values
    elif mode == ModeType.DICE:
        result = random.randint(1, 6)
        values = [random.randint(1, 6) for _ in range(Config.SHUFFLE_COUNT)]
        values.append(result)
        return values
    elif mode == ModeType.FORTUNE:
        count = len(get_fortunes())
        result = random.randint(0, count - 1)
        values = [random.randint(0, count - 1) for _ in range(Config.SHUFFLE_COUNT)]
        values.append(result)
        return values
    elif mode == ModeType.NUMBER:
        result = random.randint(1, 100)
        values = [random.randint(1, 100) for _ in range(Config.SHUFFLE_COUNT)]
        values.append(result)
        return values

def play_current_mode():
    if state.anim_phase != AnimPhase.NONE:
        return
    state.shuffle_values = generate_shuffle_values()
    state.start_anim(AnimPhase.SHUFFLE)

def enter_mode():
    state.current_page = PageType.GAME
    state.result_value = None
    draw_current_mode(None)

def back_to_menu():
    state.current_page = PageType.MENU
    state.result_value = None
    state.reset_click()
    draw_menu()

def toggle_language():
    state.lang = Lang.EN if state.lang == Lang.ZH else Lang.ZH
    state.anim_phase = AnimPhase.NONE
    if state.current_page == PageType.MENU:
        draw_menu()
    else:
        draw_current_mode(state.result_value)

def on_single_click():
    if state.current_page == PageType.MENU:
        next_menu_item()
    else:
        play_current_mode()

def on_double_click():
    if state.current_page == PageType.MENU:
        state.current_mode = state.menu_index
        enter_mode()
    else:
        back_to_menu()

def on_triple_click():
    toggle_language()

def next_menu_item():
    state.menu_index = (state.menu_index + 1) % len(ModeNames)
    draw_menu()

def handle_input(now):
    if M5.BtnA.wasPressed():
        if state.click_count == 0:
            state.first_click_ms = now
        state.click_count += 1

    if state.click_count > 0 and time.ticks_diff(now, state.first_click_ms) > Config.MULTI_CLICK_MS:
        count = state.click_count
        state.click_count = 0
        if count == 1:
            on_single_click()
        elif count == 2:
            on_double_click()
        else:
            on_triple_click()

def setup():
    M5.begin()
    Display.setRotation(1)
    Display.setFont(M5.Lcd.FONTS.EFontCN24)
    state.reset_click()
    Display.fillRect(0, 0, Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT, Colors.WHITE)
    state.start_anim(AnimPhase.BOOT_FADE)

def loop():
    M5.update()
    now = time.ticks_ms()
    animate_tick(now)
    handle_input(now)

setup()
while True:
    loop()
    time.sleep_ms(10)
