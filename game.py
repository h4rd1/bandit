import random

class SlotMachine:
    def __init__(self):
        self.balance = 100
        self.bet = 10
        # Соответствие индексов и названий символов
        self.symbols = [
            "apple",
            "banana",
            "cherry",
            "lemon",
            "orange",
            "seven",
            "star"
        ]

    def spin(self):
        """
        Выполняет спин барабанов и возвращает результат.
        Возвращает:
            dict: с ключами:
                - "results": [int, int, int] — индексы выпавших символов
                - "symbols": [str, str, str] — названия символов
                - "win": int — выигранная сумма
                - "message": str — текстовое сообщение
                - "balance": int — текущий баланс
        Или None, если недостаточно средств.
        """
        if self.balance < self.bet:
            return None

        # Списываем ставку
        self.balance -= self.bet

        # Генерируем 3 случайных индекса (0–6)
        indices = [random.randint(0, 6) for _ in range(3)]
        symbols = [self.symbols[i] for i in indices]


        win = 0
        message = ""

        # Проверяем комбинации
        if indices[0] == indices[1] == indices[2]:
            # Три одинаковых символа — джекпот
            win = 999
            message = f"ДЖЕКПОТ! Три {symbols[0].upper()}. +{win} монет!"
            self.balance += win
        elif indices[0] == indices[1] or indices[1] == indices[2] or indices[0] == indices[2]:
            # Две одинаковых — малый выигрыш
            # Находим пару
            if indices[0] == indices[1]:
                pair_symbol = symbols[0]
            elif indices[1] == indices[2]:
                pair_symbol = symbols[1]
            else:
                pair_symbol = symbols[0]
            
            win = 20
            message = f"Два {pair_symbol.upper()}! +{win} монет!"
            self.balance += win
        else:
            # Нет совпадений
            message = "Нет совпадений. Проигрыш."


        return {
            "results": indices,
            "symbols": symbols,
            "win": win,
            "message": message,
            "balance": self.balance
        }
