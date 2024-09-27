import tkinter as tk
from tkinter import messagebox

class ChessGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Phong Quân Cờ")
        self.promotion_piece = None

        # Tạo các nút cho từng loại quân
        self.create_buttons()

    def create_buttons(self):
        pieces = {'Q': 'Hậu', 'R': 'Xe', 'B': 'Tượng', 'N': 'Mã'}
        for piece, name in pieces.items():
            button = tk.Button(self.root, text=name, command=lambda p=piece: self.promote(p))
            button.pack(padx=20, pady=10)

        # Thêm nút thoát
        exit_button = tk.Button(self.root, text="Thoát", command=self.root.quit)
        exit_button.pack(pady=20)

    def promote(self, piece):
        self.promotion_piece = piece
        messagebox.showinfo("Phong Quân", f"Bạn đã chọn phong thành: {piece}")
        self.root.quit()

    def prompt_for_promotion_piece(self):
        self.root.mainloop()
        return self.promotion_piece

# Sử dụng lớp
game = ChessGame()
chosen_piece = game.prompt_for_promotion_piece()

