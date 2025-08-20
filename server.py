import socket
import pyautogui
import io
from PIL import Image
import time

SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000

def send_image(conn):
    screenshot = pyautogui.screenshot()
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()

    conn.send(len(img_byte_arr).to_bytes(4, byteorder='big'))
    conn.send(img_byte_arr)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Сервер запущен на {SERVER_HOST}:{SERVER_PORT}. Ожидание подключения...")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"Подключено к {addr}")

            try:
                while True:
                    send_image(conn)
                    print("Изображение отправлено.")
            except (ConnectionResetError, BrokenPipeError):
                print(f"Клиент {addr} отключился")
            except Exception as e:
                print(f"Произошла ошибка: {e}")
            finally:
                conn.close()
                print("Ожидание нового подключения...")
    except KeyboardInterrupt:
        print("Сервер остановлен пользователем")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()