import ccxt
import pandas as pd
import time
import customtkinter as ctk
from tkinter import ttk
from pygame import mixer
import os

# Ініціалізація звукового модуля
mixer.init()

# Шлях до звукового файлу
SOUND_FILE = "cash.mp3"


# Функція для відтворення звуку
def play_sound():
    if sound_enabled.get():
        if os.path.exists(SOUND_FILE):
            mixer.music.load(SOUND_FILE)
            mixer.music.play()
        else:
            print("Файл звуку не знайдено!")


# Функція для отримання даних з біржі
def get_data(symbol, timeframe='1h', limit=100):
    exchange = ccxt.binance()  # Використовуємо Binance для отримання даних
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df


# Функція для розрахунку середнього ковзного
def calculate_moving_average(df, window=20):
    df['MA'] = df['close'].rolling(window=window).mean()
    return df


# Функція для прийняття рішення
def make_decision(df):
    if df['close'].iloc[-1] > df['MA'].iloc[-1]:
        return "Купувати"
    else:
        return "Продавати"


# Основна функція для оновлення даних
def update_data():
    symbol = symbol_combobox.get()
    timeframe = timeframe_combobox.get()
    limit = int(limit_entry.get())

    data = get_data(symbol, timeframe, limit)
    data = calculate_moving_average(data)
    decision = make_decision(data)

    last_price_label.configure(text=f"Остання ціна: {data['close'].iloc[-1]}")
    moving_average_label.configure(text=f"Середній ковзний: {data['MA'].iloc[-1]}")
    decision_label.configure(text=f"Рішення: {decision}")

    # Відтворення звуку, якщо рішення "Продавати"
    if decision == "Продавати":
        play_sound()

    # Оновлення даних кожну годину
    root.after(3600000, update_data)


# Функція для зміни теми
def change_theme(theme):
    ctk.set_appearance_mode(theme)


# Функція для зміни мови
def change_language(lang):
    # Словник для перекладів
    translations = {
        "Українська": {
            "symbol_label": "Виберіть актив:",
            "timeframe_label": "Виберіть таймфрейм:",
            "limit_label": "Кількість свічок:",
            "update_button": "Оновити дані",
            "last_price_label": "Остання ціна: -",
            "moving_average_label": "Середній ковзний: -",
            "decision_label": "Рішення: -",
            "sound_label": "Увімкнути звук",
            "theme_label": "Виберіть тему:",
            "language_label": "Виберіть мову:"
        },
        "English": {
            "symbol_label": "Select asset:",
            "timeframe_label": "Select timeframe:",
            "limit_label": "Number of candles:",
            "update_button": "Update data",
            "last_price_label": "Last price: -",
            "moving_average_label": "Moving average: -",
            "decision_label": "Decision: -",
            "sound_label": "Enable sound",
            "theme_label": "Select theme:",
            "language_label": "Select language:"
        }
    }
    # Оновлення тексту елементів інтерфейсу
    if lang in translations:
        symbol_label.configure(text=translations[lang]["symbol_label"])
        timeframe_label.configure(text=translations[lang]["timeframe_label"])
        limit_label.configure(text=translations[lang]["limit_label"])
        update_button.configure(text=translations[lang]["update_button"])
        last_price_label.configure(text=translations[lang]["last_price_label"])
        moving_average_label.configure(text=translations[lang]["moving_average_label"])
        decision_label.configure(text=translations[lang]["decision_label"])
        sound_label.configure(text=translations[lang]["sound_label"])
        theme_label.configure(text=translations[lang]["theme_label"])
        language_label.configure(text=translations[lang]["language_label"])


# Створення головного вікна
root = ctk.CTk()
root.title("Аналітика ринку")

# Вибір активу
symbol_label = ctk.CTkLabel(root, text="Виберіть актив:")
symbol_label.grid(row=0, column=0, padx=10, pady=10)

symbols = ['BTC/USDT', 'ETH/USDT', 'TON/USDT', 'FPI/USDT', 'BNB/USDT', 'XRP/USDT', 'ADA/USDT', 'DOGE/USDT', 'SOL/USDT',
           'DOT/USDT']
symbol_combobox = ttk.Combobox(root, values=symbols)
symbol_combobox.grid(row=0, column=1, padx=10, pady=10)
symbol_combobox.set('BTC/USDT')

# Вибір таймфрейму
timeframe_label = ctk.CTkLabel(root, text="Виберіть таймфрейм:")
timeframe_label.grid(row=1, column=0, padx=10, pady=10)

timeframes = ['1h', '4h', '1d']
timeframe_combobox = ttk.Combobox(root, values=timeframes)
timeframe_combobox.grid(row=1, column=1, padx=10, pady=10)
timeframe_combobox.set('1h')

# Введення кількості свічок
limit_label = ctk.CTkLabel(root, text="Кількість свічок:")
limit_label.grid(row=2, column=0, padx=10, pady=10)

limit_entry = ctk.CTkEntry(root)
limit_entry.grid(row=2, column=1, padx=10, pady=10)
limit_entry.insert(0, '100')

# Кнопка для оновлення даних
update_button = ctk.CTkButton(root, text="Оновити дані", command=update_data)
update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Відображення останньої ціни
last_price_label = ctk.CTkLabel(root, text="Остання ціна: -")
last_price_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Відображення середнього ковзного
moving_average_label = ctk.CTkLabel(root, text="Середній ковзний: -")
moving_average_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Відображення рішення
decision_label = ctk.CTkLabel(root, text="Рішення: -")
decision_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

# Налаштування звуку
sound_enabled = ctk.BooleanVar(value=True)
sound_label = ctk.CTkLabel(root, text="Увімкнути звук")
sound_label.grid(row=7, column=0, padx=10, pady=10)
sound_checkbox = ctk.CTkCheckBox(root, text="", variable=sound_enabled)
sound_checkbox.grid(row=7, column=1, padx=10, pady=10)

# Вибір теми
theme_label = ctk.CTkLabel(root, text="Виберіть тему:")
theme_label.grid(row=8, column=0, padx=10, pady=10)

themes = ["System", "Dark", "Light"]
theme_combobox = ttk.Combobox(root, values=themes)
theme_combobox.grid(row=8, column=1, padx=10, pady=10)
theme_combobox.set("System")
theme_combobox.bind("<<ComboboxSelected>>", lambda e: change_theme(theme_combobox.get()))

# Вибір мови
language_label = ctk.CTkLabel(root, text="Виберіть мову:")
language_label.grid(row=9, column=0, padx=10, pady=10)

languages = ["Українська", "English"]
language_combobox = ttk.Combobox(root, values=languages)
language_combobox.grid(row=9, column=1, padx=10, pady=10)
language_combobox.set("Українська")
language_combobox.bind("<<ComboboxSelected>>", lambda e: change_language(language_combobox.get()))

# Запуск оновлення даних
update_data()

# Запуск головного циклу
root.mainloop()