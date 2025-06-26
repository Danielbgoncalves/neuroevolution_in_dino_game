class Simulador:
    def __init__(self, np):

        self.rede = None
        self.np = np

        # ----- O canva -----
        self.LARGURA = 600
        self.ALTURA = 400

        # ----- O dino -----
        self.movimento_y = 0
        self.dino_vivo = True
        self.dino_x = 50
        self.dino_y = 300

        # ----- Score -----
        self.score = 1

        # ----- Cactos -----
        # cacto1
        self.cacto1 = {
            "id": 1, # era canvas aqui mas tiramos a parte vizual
            "w": 20,
            "h": 30,
            "pos_x": 275
        }

        self.cacto2 = {
            "id": 2,
            "w": 50,
            "h": 30,
            "pos_x": 600
        }

        self.cactos_vel = 8
        self.cactos = [self.cacto1, self.cacto2]
    
    def definir_rede(self, rede):
        self.rede = rede
        self.movimento_y = 0
        self.dino_vivo = True
        self.dino_x = 50
        self.dino_y = 300

        self.score = 1

        self.cacto1["pos_x"] = 275  
        self.cacto2["pos_x"] = 600   
        self.cactos_vel = 8
         
    def atualizar_um_frame(self):
        for cacto in self.cactos:
            cacto["pos_x"] -= self.cactos_vel

            if cacto["pos_x"] < - 60:
                cacto["pos_x"] = self.LARGURA + 60

                if self.cactos_vel < 18: 
                    self.cactos_vel += 0.15
        
        self.score += 0.09

        self.atualizar_dino()
        self.detectar_colisao()
        
    def atualizar_dino(self):
        #x, y = canvas.coords(dino)
        self.dino_y += self.movimento_y
        #canvas.coords(dino, x, y + movimento_y)
        y = self.dino_y
        if y < 300:
            self.movimento_y += min(1.5, 0.75 + (self.cactos_vel - 5) * 0.05)
        if y > 300:
            self.movimento_y = 0
            self.dino_y = 300
            #canvas.coords(dino, x, 300)
    
    def detectar_colisao(self):
        dino_x, dino_y = self.dino_x, self.dino_y
        dino_w, dino_h = 35, 35
        dino_y_topo = dino_y - dino_h

        for cacto in self.cactos:
            cacto_x, cacto_y = cacto["pos_x"], 300 
            cacto_w, cacto_h = cacto["w"], cacto["h"]
            cacto_y_topo = cacto_y - cacto_h

            if (
                dino_x < cacto_x + cacto_w and
                dino_x + dino_w > cacto_x and
                dino_y_topo < cacto_y and
                dino_y > cacto_y_topo
            ):
                #print("Testando colisão!")
                self.game_over()
    
    def game_over(self):
        self.dino_vivo = False

    def coleta_input(self):
        distancias = [(c["pos_x"] - self.dino_x, i) for i, c in enumerate(self.cactos) if c["pos_x"] - self.dino_x > 0]
        min_dist, idx = min(distancias)
        cacto_w = self.cactos[idx]["w"]

        return self.np.array([
            min_dist / (self.LARGURA / 2),
            cacto_w / 60, # porque esse é o maior cacto
            self.cactos_vel / 18,
            self.movimento_y / 1.5,
            (300 - self.dino_y) / (300 - 241.5)
        ])

    def rede_joga(self):
        dados = self.coleta_input() 
        pula = self.rede.forward(dados) > 0.5 
        #print("pulou: ", pula)

        if pula and self.movimento_y == 0:
            self.movimento_y = -9

        
        






