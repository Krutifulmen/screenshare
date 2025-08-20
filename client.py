import socket
import io
from PIL import Image, ImageTk
import tkinter as tk

class ImageClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Screen Viewer")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.bind('<Escape>', lambda e: self.on_closing())
        
        self.canvas = tk.Canvas(master, width=800, height=600)
        self.canvas.pack()
        
        self.running = True
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((ip, 5000))
            self.update_image()
        except ConnectionRefusedError:
            print("Не удалось подключиться к серверу")
            self.running = False
            self.master.after(2000, self.master.destroy)

    def receive_all(self, sock, size):
        data = bytearray()
        while len(data) < size:
            packet = sock.recv(size - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def update_image(self):
        if not self.running:
            return
            
        try:
            size_data = self.sock.recv(4)
            if size_data:
                size = int.from_bytes(size_data, byteorder='big')
                image_data = self.receive_all(self.sock, size)
                if image_data is not None:
                    print(f"Получены данные изображения размером: {len(image_data)} байт")
                    image = Image.open(io.BytesIO(image_data))
                    resized_image = image.resize((800, 600), Image.LANCZOS)
                    
                    self.photo = ImageTk.PhotoImage(resized_image)
                    self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
                    print("Изображение обновлено.")
                
            self.master.after(100, self.update_image)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.on_closing()

    def on_closing(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()

ip = input("Введите IP сервера: ")
root = tk.Tk()
client = ImageClient(root)
root.mainloop()