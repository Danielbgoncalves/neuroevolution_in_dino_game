import tkinter as tk
from PIL import Image, ImageTk

# Criar janela com o Tkinter
LARGURA = 600
ALTURA = 400

janela = tk.Tk()
janela.title = "Dino AI"
canvas = tk.Canvas(janela, width=LARGURA, height=ALTURA)
canvas.pack()

# Configurações do sprite do dino
DINO_PATH = "assets/dino_azul_anda2.png"
FRAME_WIDTH = 40
FRAME_HEIDTH = 31
NUM_FRAMES = 6
FPS = 100
frame_atual = 0
movimento_y = 0
dino_vivo = True

dino_alturas = []

dino_sprite = Image.open(DINO_PATH)
dino_frames = []

for i in range(NUM_FRAMES):
    box = (i * FRAME_WIDTH, 0, (i + 1) * FRAME_WIDTH, FRAME_HEIDTH )
    frame = dino_sprite.crop(box)
    frame = frame.resize((40,40))
    dino_frames.append(ImageTk.PhotoImage(frame))

# Score
score = 1

# Carregar assets
fundo_img = ImageTk.PhotoImage(Image.open("assets/fundo.png").resize((LARGURA, ALTURA)))
cacto1_img = ImageTk.PhotoImage(Image.open("assets/cacto1.png"))
cacto2_img = ImageTk.PhotoImage(Image.open("assets/cacto2.png"))

# Desenha fundo no canva
canvas.create_image(0,0, anchor=tk.NW, image=fundo_img)

# Desenha dino fixo
dino = canvas.create_image(50, 300, anchor=tk.SW, image=dino_frames[frame_atual])

# Dados dos cactos
cacto1 = {
    "id": canvas.create_image(275, 300, anchor=tk.SW, image=cacto1_img),
    "w": 20,
    "h": 30,
}

cacto2 = {
    "id": canvas.create_image(600, 300, anchor=tk.SW, image=cacto2_img),
    "w": 50,
    "h": 30,
}
cactos_vel = 8
cactos = [cacto1, cacto2]

# Texto co score
pontuacao = canvas.create_text(LARGURA - 50, 20, text="Score: 0000")

# Animar o dino
def animar_dino():
    if not dino_vivo: return

    global frame_atual
    frame_atual = (frame_atual + 1) % NUM_FRAMES
    canvas.itemconfig(dino, image=dino_frames[frame_atual])
    janela.after(FPS, animar_dino)


# Tem que atualizar ne
def atualizar():
    if not dino_vivo: return
    global cactos_vel, score

    for cacto in cactos:
        canvas.move(cacto["id"], -cactos_vel, 0)
        x, _ = canvas.coords(cacto["id"])
        if x < - 60:
            canvas.move(cacto["id"], LARGURA + 60, 0)
            if cactos_vel < 18: 
                cactos_vel += 0.15

    score += 0.09

    atualizar_dino(cactos_vel)
    colidiu_dino()
    atualiza_score(score)


    janela.after(30, atualizar)

# Score
def atualiza_score(score):
    canvas.itemconfig(pontuacao, text=f"Score: {int(score)}")

#  Detecção de tecla clicada
def tecla_pressionada(event):
    global movimento_y, dino_vivo

    if event.keysym == "space" and movimento_y == 0:
        movimento_y = -9
    print("velocidade dos cactos: ", cactos_vel)
    print("velocidade do dino: ", movimento_y)

    if event.char == 'a':
        dino_vivo = True

    
def atualizar_dino(velocidade_cacto):
    global movimento_y, dino_alturas
    x, y = canvas.coords(dino)
    canvas.coords(dino, x, y + movimento_y)
    
    if y < 300:
        movimento_y += min(1.5, 0.75 + (velocidade_cacto - 5) * 0.05)
        dino_alturas.append(y)
    if y > 300:
        movimento_y = 0
        canvas.coords(dino, x, 300)


def colidiu_dino():
    global dino_vivo

    dino_x, dino_y = canvas.coords(dino)
    dino_w, dino_h = 35, 35
    dino_y_topo = dino_y - dino_h

    for cacto in cactos:
        cacto_x, cacto_y = canvas.coords(cacto["id"])
        cacto_w, cacto_h = cacto["w"], cacto["h"]
        cacto_y_topo = cacto_y - cacto_h

        if (
            dino_x < cacto_x + cacto_w and
            dino_x + dino_w > cacto_x and
            dino_y_topo < cacto_y and
            dino_y > cacto_y_topo
        ):
            game_over()
            
def game_over():
    global dino_vivo, dino_alturas
    dino_vivo = False
    print(f"Maior altura do dino: {min(dino_alturas)} \nMenor Altura do dino: {max(dino_alturas)}")
    print("colidiu! ")


atualizar()
animar_dino()
janela.bind("<Key>", tecla_pressionada)
janela.mainloop()




