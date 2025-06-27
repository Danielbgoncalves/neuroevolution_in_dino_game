import tkinter as tk
from PIL import Image, ImageTk
from abc import ABC, abstractmethod

class JogoDinoBase(ABC):
    LARGURA = 600
    ALTURA = 400
    FRAME_WIDTH = 40
    FRAME_HEIGHT = 31
    NUM_FRAMES = 6
    FPS = 100

    def __init__(self):
        self.janela = tk.Tk()
        self.janela.title("Dino AI")
        self.canvas = tk.Canvas(self.janela, width=self.LARGURA, height=self.ALTURA)
        self.canvas.pack()

        self.frame_atual = 0
        self.movimento_y = 0
        self.dino_vivo = True
        self.score = 1
        self.dino_alturas = []

        self.dino_frames = self.carregar_sprites("assets/dino_azul_anda2.png")
        self.fundo_img = ImageTk.PhotoImage(Image.open("assets/fundo.png").resize((self.LARGURA, self.ALTURA)))
        self.cacto1_img = ImageTk.PhotoImage(Image.open("assets/cacto1.png"))
        self.cacto2_img = ImageTk.PhotoImage(Image.open("assets/cacto2.png"))

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.fundo_img)
        self.dino = self.canvas.create_image(50, 300, anchor=tk.SW, image=self.dino_frames[self.frame_atual])

        self.cacto1 = {"id": self.canvas.create_image(275, 300, anchor=tk.SW, image=self.cacto1_img), "w": 20, "h": 30}
        self.cacto2 = {"id": self.canvas.create_image(600, 300, anchor=tk.SW, image=self.cacto2_img), "w": 50, "h": 30}
        self.cactos = [self.cacto1, self.cacto2]
        self.cactos_vel = 8

        self.pontuacao_info = self.canvas.create_text(self.LARGURA - 50, 20, text="Score: 0000")
        self.velocidade_info = self.canvas.create_text(self.LARGURA - 120, 20, text="Velocidade: 0000")


        self.janela.after(self.FPS, self.animar_dino)
        self.janela.after(30, self.atualizar)
        self.janela.bind("<Key>", self.tecla_pressionada)
        self.janela.mainloop()

    def carregar_sprites(self, path):
        sprite = Image.open(path)
        frames = []
        for i in range(self.NUM_FRAMES):
            box = (i * self.FRAME_WIDTH, 0, (i + 1) * self.FRAME_WIDTH, self.FRAME_HEIGHT)
            frame = sprite.crop(box).resize((40, 40))
            frames.append(ImageTk.PhotoImage(frame))
        return frames

    def animar_dino(self):
        if not self.dino_vivo: return
        self.frame_atual = (self.frame_atual + 1) % self.NUM_FRAMES
        self.canvas.itemconfig(self.dino, image=self.dino_frames[self.frame_atual])
        self.janela.after(self.FPS, self.animar_dino)

    def atualizar(self):
        if not self.dino_vivo: return

        for cacto in self.cactos:
            self.canvas.move(cacto["id"], -self.cactos_vel, 0)
            x, _ = self.canvas.coords(cacto["id"])
            if x < -60:
                self.canvas.move(cacto["id"], self.LARGURA + 60, 0)
                if self.cactos_vel < 18.2:
                    self.cactos_vel += 0.15

        self.score += 0.09
        self.atualizar_dino()
        self.colidiu_dino()
        self.canvas.itemconfig(self.pontuacao_info, text=f"Score: {int(self.score)}")
        self.canvas.itemconfig(self.velocidade_info, text=f"Velocidade: {int(self.cactos_vel)}")


        if self.acao():
            if self.movimento_y == 0:
                self.movimento_y = -9

        self.janela.after(30, self.atualizar)

    def atualizar_dino(self):
        x, y = self.canvas.coords(self.dino)
        self.canvas.coords(self.dino, x, y + self.movimento_y)
        if y < 300:
            altura = 300 - y
            self.movimento_y += min(2.5, 0.75 + (self.cactos_vel - 5) * 0.05)
            self.score -= 0.002 * altura  
            # a ideia é punir pulos longos (tinha rede aproveitando esse bug pra voar)
        if y > 300:
            self.movimento_y = 0
            self.canvas.coords(self.dino, x, 300)

    def colidiu_dino(self):
        dino_x, dino_y = self.canvas.coords(self.dino)
        dino_w, dino_h = 35, 35
        dino_y_topo = dino_y - dino_h

        for cacto in self.cactos:
            cacto_x, cacto_y = self.canvas.coords(cacto["id"])
            cacto_w, cacto_h = cacto["w"], cacto["h"]
            cacto_y_topo = cacto_y - cacto_h

            if (
                dino_x < cacto_x + cacto_w and
                dino_x + dino_w > cacto_x and
                dino_y_topo < cacto_y and
                dino_y > cacto_y_topo
            ):
                self.game_over()

    def game_over(self):
        self.dino_vivo = False

    def tecla_pressionada(self, event):
        if event.keysym == "space" and self.movimento_y == 0:
            self.movimento_y = -9

    @abstractmethod
    def acao(self):
        pass
