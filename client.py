#!/usr/bin/env python3
import customtkinter as ctk
import socket
import threading
import random
import time
from PIL import Image, ImageTk
import pygame  # Para reprodução de som

# ===============================
# Configurações Iniciais
# ===============================
ctk.set_appearance_mode("System")  # Outras opções: "Light", "Dark"
ctk.set_default_color_theme("blue")

# Inicializa o mixer do pygame para som
pygame.mixer.init()
try:
    coin_sound = pygame.mixer.Sound("coin_drop.mp3")
except Exception as e:
    print("Erro ao carregar o som coin_drop.mp3:", e)
    coin_sound = None

# Variáveis globais para comunicação e controle
client_socket = None
receive_thread = None
local_balance = 100  # Saldo inicial
symbols = ["🍒", "🍋", "🍊", "🍇", "⭐", "7"]

# Tenta carregar a imagem da alavanca (opcional)
try:
    lever_img = Image.open("lever.png")
    bg_img = lever_img.resize((350, 350), Image.Resampling.LANCZOS)
    lever_ctk = ctk.CTkImage(light_image=lever_img, size=(100, 150))
except Exception as e:
    print("Erro ao carregar a imagem da alavanca:", e)
    lever_ctk = None

# ===============================
# Funções de Lógica e Atualização
# ===============================
def update_balance_label():
    balance_label.configure(text=f"Saldo: {local_balance} reais")

def update_slot_labels(new_symbols):
    reel1_label.configure(text=new_symbols[0])
    reel2_label.configure(text=new_symbols[1])
    reel3_label.configure(text=new_symbols[2])
    root.update()

def animate_slots():
    spin_cycles = 10
    for _ in range(spin_cycles):
        new_symbols = [random.choice(symbols) for _ in range(3)]
        update_slot_labels(new_symbols)
        time.sleep(0.1)
    final_symbols = [random.choice(symbols) for _ in range(3)]
    update_slot_labels(final_symbols)

def spin():
    global local_balance
    if local_balance < 10:
        balance_label.configure(text="Saldo insuficiente!")
        return
    spin_button.configure(state="disabled")
    local_balance -= 10  # Desconta 10 reais por giro
    update_balance_label()
    anim_thread = threading.Thread(target=run_spin, daemon=True)
    anim_thread.start()

def run_spin():
    animate_slots()
    try:
        if client_socket:
            client_socket.sendall("play".encode())
    except Exception as e:
        print("Erro ao enviar comando 'play':", e)
    spin_button.configure(state="normal")

def deposit_money():
    global local_balance
    amount_str = deposit_entry.get()
    if not amount_str:
        return
    try:
        amount = int(amount_str)
    except ValueError:
        balance_label.configure(text="Valor de depósito inválido!")
        deposit_entry.delete(0, ctk.END)
        return
    local_balance += amount
    update_balance_label()
    if coin_sound:
        coin_sound.play()
    try:
        if client_socket:
            client_socket.sendall(f"deposit {amount}".encode())
    except Exception as e:
        print("Erro ao enviar comando de depósito:", e)
    deposit_entry.delete(0, ctk.END)

def desistir():
    global client_socket
    try:
        if client_socket:
            client_socket.sendall("quit".encode())
            client_socket.close()
    except Exception:
        pass
    show_desist_frame()

def show_desist_frame():
    # Esconde a interface de jogo e exibe a tela de desistência
    game_frame.pack_forget()
    desist_frame.pack(fill="both", expand=True)
    try:
        img = Image.open("desistir.jpg")
        img = img.resize((350, 400), Image.Resampling.LANCZOS)
        desist_img = ctk.CTkImage(light_image=img, size=(800, 350))
        desist_img_label.configure(image=desist_img, text="")
        desist_img_label.image = desist_img  # Mantém referência
    except Exception as e:
        desist_img_label.configure(text=f"Erro ao carregar imagem: {e}")

def continue_game():
    global local_balance
    desist_frame.pack_forget()
    local_balance = 100  # Reinicia o saldo
    update_balance_label()
    connection_frame.pack(fill="both", expand=True)

def close_app():
    try:
        if client_socket:
            client_socket.sendall("quit".encode())
            client_socket.close()
    except Exception:
        pass
    root.destroy()

def connect_to_server():
    global client_socket, receive_thread
    host = host_entry.get()
    port_str = port_entry.get()
    try:
        port = int(port_str)
    except ValueError:
        conn_status_label.configure(text="Porta inválida!")
        return
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
    except Exception as e:
        conn_status_label.configure(text=f"Não foi possível conectar: {e}")
        return
    connection_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)
    receive_thread = threading.Thread(target=receive_messages, daemon=True)
    receive_thread.start()

def receive_messages():
    global client_socket
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Servidor desconectado.")
                break
            message = data.decode()
            print("Servidor:", message)
        except Exception as e:
            print("Erro na recepção:", e)
            break

# ===============================
# Criação da Janela e Layout (CustomTkinter)
# ===============================
root = ctk.CTk()
root.title("Jogo do Tigrinho - Cassino")
root.geometry("800x600")

# ----- Frame de Conexão -----
connection_frame = ctk.CTkFrame(root)
connection_frame.pack(fill="both", expand=True)

# Na tela de conexão, os campos ficam à esquerda e a imagem (logo_free_background.png) à direita
conn_left_frame = ctk.CTkFrame(connection_frame, width=350)
conn_left_frame.pack(side="left", fill="y", padx=20, pady=20)
conn_right_frame = ctk.CTkFrame(connection_frame, width=350)
conn_right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)

host_label = ctk.CTkLabel(conn_left_frame, text="Host:")
host_label.pack(pady=(100,5))
host_entry = ctk.CTkEntry(conn_left_frame, width=200)
host_entry.pack(pady=5)
host_entry.insert(0, "127.0.0.1")

port_label = ctk.CTkLabel(conn_left_frame, text="Porta:")
port_label.pack(pady=5)
port_entry = ctk.CTkEntry(conn_left_frame, width=200)
port_entry.pack(pady=5)
port_entry.insert(0, "5000")

connect_button = ctk.CTkButton(conn_left_frame, text="Conectar", command=connect_to_server)
connect_button.pack(pady=20)
conn_status_label = ctk.CTkLabel(conn_left_frame, text="", fg_color="transparent")
conn_status_label.pack(pady=5)

try:
    bg_img = Image.open("logo_free_background.png")
    bg_img = bg_img.resize((350, 350), Image.Resampling.LANCZOS)
    bg_ctk = ctk.CTkImage(light_image=bg_img, size=(350, 350))
    bg_label = ctk.CTkLabel(conn_right_frame, image=bg_ctk, text="")
    bg_label.pack(expand=True, pady=20)
except Exception as e:
    print("Erro ao carregar imagem de fundo:", e)
    bg_label = ctk.CTkLabel(conn_right_frame, text="Logo não disponível")
    bg_label.pack(expand=True, pady=20)

# ----- Frame de Jogo (Cassino) -----
game_frame = ctk.CTkFrame(root)
# Aqui usamos um layout com dois blocos: uma barra superior e uma área principal dividida em painel central e painel direito.

# Barra superior (top_bar): canto superior esquerdo - botão Desistir; canto superior direito - saldo atual.
top_bar = ctk.CTkFrame(game_frame, height=50)
top_bar.pack(fill="x", side="top", padx=10, pady=10)

desistir_button = ctk.CTkButton(top_bar, text="Desistir", command=desistir, width=100)
desistir_button.pack(side="left", padx=10)
balance_label = ctk.CTkLabel(top_bar, text=f"Saldo: {local_balance} reais", font=("Arial", 16))
balance_label.pack(side="right", padx=10)

# Área principal (main_area) dividida em dois painéis: central e direito.
main_area = ctk.CTkFrame(game_frame)
main_area.pack(fill="both", expand=True, padx=10, pady=10)
main_area.grid_columnconfigure(0, weight=3)  # Painel central (reles e depósito)
main_area.grid_columnconfigure(1, weight=1)  # Painel direito (imagem do logo)

# Painel Central: contém a área de jogo (alavanca, rolos e depósito)
center_frame = ctk.CTkFrame(main_area)
center_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Painel Direito: exibe a imagem de fundo (logo)
logo_frame = ctk.CTkFrame(main_area)
logo_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
try:
    logo_img = Image.open("logo_free_background.png")
    bg_img = bg_img.resize((350, 350), Image.Resampling.LANCZOS)
    logo_ctk = ctk.CTkImage(light_image=logo_img, size=(200, 200))
    logo_label = ctk.CTkLabel(logo_frame, image=logo_ctk, text="")
    logo_label.pack(expand=True)
except Exception as e:
    logo_label = ctk.CTkLabel(logo_frame, text="Logo não disponível")
    logo_label.pack(expand=True)

# No center_frame, usamos um grid para colocar a alavanca (spin_button) à esquerda e os reles no centro.
center_frame.grid_columnconfigure(0, weight=1)
center_frame.grid_columnconfigure(1, weight=3)
center_frame.grid_rowconfigure(0, weight=1)
center_frame.grid_rowconfigure(1, weight=0)

# Alavanca (botão de giro) na coluna 0
if lever_ctk:
    spin_button = ctk.CTkButton(center_frame, text="", image=lever_ctk, command=spin, width=120, height=150)
else:
    spin_button = ctk.CTkButton(center_frame, text="GIRAR", command=spin, width=120)
spin_button.grid(row=0, column=0, padx=20, pady=20, sticky="w")

# Reles do slot machine na coluna 1
reels_frame = ctk.CTkFrame(center_frame)
reels_frame.grid(row=0, column=1, padx=20, pady=20)
reel1_label = ctk.CTkLabel(reels_frame, text="❔", font=("Arial", 48))
reel1_label.pack(side="left", padx=10)
reel2_label = ctk.CTkLabel(reels_frame, text="❔", font=("Arial", 48))
reel2_label.pack(side="left", padx=10)
reel3_label = ctk.CTkLabel(reels_frame, text="❔", font=("Arial", 48))
reel3_label.pack(side="left", padx=10)

# Área de Depósito abaixo dos reles, ocupando toda a largura do center_frame
deposit_frame = ctk.CTkFrame(center_frame)
deposit_frame.grid(row=1, column=0, columnspan=2, pady=20)
deposit_entry = ctk.CTkEntry(deposit_frame, width=150, placeholder_text="Valor")
deposit_entry.pack(side="left", padx=10)
deposit_button = ctk.CTkButton(deposit_frame, text="Depositar", command=deposit_money, width=100)
deposit_button.pack(side="left", padx=10)

# ----- Frame de Desistência -----
desist_frame = ctk.CTkFrame(root)
desist_img_label = ctk.CTkLabel(desist_frame, text="")  # A imagem será exibida aqui
desist_img_label.pack(pady=20)
desist_question = ctk.CTkLabel(desist_frame, text="Deseja continuar?", font=("Arial", 20))
desist_question.pack(pady=10)
sim_button = ctk.CTkButton(desist_frame, text="Sim", command=continue_game, width=100)
sim_button.pack(side="left", padx=20, pady=20)
nao_button = ctk.CTkButton(desist_frame, text="Não", command=close_app, width=100)
nao_button.pack(side="right", padx=20, pady=20)

# Inicialmente, exibe a tela de conexão
connection_frame.pack(fill="both", expand=True)

root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()

