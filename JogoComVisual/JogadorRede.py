import numpy as np
from JogoComVisual.JogoDinoBase import JogoDinoBase
from JogoComVisual.JogoDinoTurbo import JogoDinoTurbo

class JogadorRede(JogoDinoTurbo):
    def __init__(self, rede, taxa_gravidade=0.05, velocidade_maxima_cacto=18):
        self.rede = rede
        super().__init__(taxa_gravidade, velocidade_maxima_cacto)

        

    def acao(self):
        dados = self.recolher_input()
        pula = self.rede.forward(dados) > 0.5
        return pula and self.movimento_y == 0

    def recolher_input(self):
        dino_x, dino_y = self.canvas.coords(self.dino)
        distancias = []

        for i, cacto in enumerate(self.cactos):
            x, _ = self.canvas.coords(cacto["id"])
            if x - dino_x > 0:
                distancias.append((x - dino_x, i))      
        
        min_dist, idx = min(distancias)

        cacto_w = self.cactos[idx]["w"]

        return np.array([
            min_dist / (self.LARGURA / 2),
            cacto_w / 60, 
            self.cactos_vel / 18,
            self.movimento_y / 1.5,
            (300 - dino_y) / (300 - 241.5)
        ])