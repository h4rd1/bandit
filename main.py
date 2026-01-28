
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from game import SlotMachine
import random
import os

class SlotMachineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Однорукий бандит ✯")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")
        
        self.icons = self.load_icons()  # ← Вызов метода
        self.game = SlotMachine()
        self.create_widgets()

    def load_icons(self):  # ← Правильное название и отступ!
        icons = {}
        try:
            for name in ["apple", "banana", "cherry", "lemon", "orange", "seven", "star"]:
                path = os.path.join("assets", f"{name}.png")
                img = Image.open(path)
                target_size = (100, 100)
                img.thumbnail(target_size, Image.LANCZOS)
                square_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
                square_img.paste(
                    img,
                    ((target_size[0] - img.width) // 2,
                     (target_size[1] - img.height) // 2)
                )
                icons[name] = ImageTk.PhotoImage(square_img)
        except Exception as e:
            print(f"Ошибка загрузки иконок: {e}")
            # Заглушки (ваш код)
        return icons

    def create_widgets(self):
        tk.Label(
            self.root,
            text="ОДНОРУКИЙ БАНДИТ",
            font=("Arial", 20, "bold"),
            fg="#f39c12",
            bg="#2c3e50"
        ).pack(pady=20)

        self.balance_label = tk.Label(
            self.root,
            text=f"Баланс: {self.game.balance} монет",
            font=("Arial", 14),
            fg="white",
            bg="#34495e"
        )
        self.balance_label.pack(pady=10)

        reel_frame = tk.Frame(self.root, bg="#34495e", bd=0, relief="flat")
        reel_frame.pack(pady=30)


        self.reel_labels = []
        for i in range(3):
            frame = tk.Frame(reel_frame, width=120, height=120, bg="#1a2530", relief="sunken", bd=3)
            frame.grid(row=0, column=i, padx=10)
            label = tk.Label(frame, image=self.icons["seven"], bg="#1a2530")
            label.place(relx=0.5, rely=0.5, anchor="center")
            self.reel_labels.append(label)

        self.spin_button = tk.Button(
            self.root,
            text="➀ КРУТИТЬ (10 монет)",
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            relief="raised",
            bd=3,
            padx=20,
            pady=10,
            command=self.spin
        )
        self.spin_button.pack(pady=20)

        self.result_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 14),
            fg="#27ae60",
            bg="#2c3e50"
        )
        self.result_label.pack(pady=10)

    def spin(self):
        if self.game.balance < self.game.bet:
            messagebox.showwarning("Ошибка", "Недостаточно монет!")
            return
        self.spin_button.config(state="disabled")
        self.animate_reels()

    def animate_reels(self):  
        for step in range(15):
            for label in self.reel_labels:
                icon_name = random.choice(list(self.icons.keys()))
                label.config(image=self.icons[icon_name])
            self.root.update()
            self.root.after(80 - step * 4)
        self.root.after(1000, self.show_result)


    def show_result(self):
        result = self.game.spin()
        if result is None:
            return

        for i, idx in enumerate(result["results"]):
            symbol = self.game.symbols[idx]
            self.reel_labels[i].config(image=self.icons[symbol])


        self.balance_label.config(text=f"Баланс: {result['balance']} монет")
        self.result_label.config(text=result["message"])


        if result["win"] == 999:
            self.flash_labels("green", 5)
        elif result["win"] > 0:
            self.pulse_labels("yellow", 3)
        else:
            self.shake_labels(3)

        self.spin_button.config(state="normal")

    def flash_labels(self, color, times):
        for _ in range(times):
            for label in self.reel_labels:
                label.config(bg=color)
            self.root.update()
            self.root.after(200)
            for label in self.reel_labels:
                label.config(bg="#1a2530")
            self.root.update()
            self.root.after(200)

    def shake_labels(self, times):
        offsets = [5, -5, 0]
        for _ in range(times):
            for i, label in enumerate(self.reel_labels):
                x = offsets[i % 3]
                y = offsets[(i + 1) % 3]
                label.place_configure(relx=0.5 + x/100, rely=0.5 + y/100)
            self.root.update()
            self.root.after(100)
            for label in self.reel_labels:
                label.place_configure(relx=0.5, rely=0.5)
            self.root.update()
            self.root.after(100)

    def pulse_labels(self, color, times):
        for _ in range(times):
            for label in self.reel_labels:
                label.config(relief="ridge", bd=5, bg=color)
            self.root.update()
            self.root.after(300)
            for label in self.reel_labels:
                label.config(relief="sunken", bd=3, bg="#1a2530")
            self.root.update()
            self.root.after(300)

    def reset_reel_appearance(self):
        for label in self.reel_labels:
            label.config(relief="sunken", bd=3, bg="#1a2530")
            label.place_configure(relx=0.5, rely=0.5)



# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachineApp(root)
    root.mainloop()
