from JogoComVisual.JogoDinoBase import JogoDinoBase

class JogoDinoTurbo(JogoDinoBase):
    def __init__(self, taxa_gravidade=0.05, velocidade_maxima_cacto=18):
        super().__init__(taxa_gravidade, velocidade_maxima_cacto, iniciar_loop=False)
        self.loop_visual_turbo()

    def loop_visual_turbo(self):
        # Roda o jogo o mais rápido possível
        while self.dino_vivo:
            self.atualizar()
            self.animar_dino()
            self.janela.update()  # força o Tkinter a renderizar
