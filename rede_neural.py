class RedeNeural:
    '''
        A estrutura vai ser entrada -> camada oculta -> saída (0=não pular  ou 1=pular)

        Entradas:
        -> distancia até o cacto
        -> largura do cacto
        -> velocidade do cacto
        -> gravidade atual
        -> altura do dino
    '''

    def __init__(self, np):
        self.np = np 

        self.w1 = np.random.randn(5,10) * 0.1 # 5 features e 10 neuronios na camda oculta
        self.b1 = np.random.rand(1, 10) * 0.1 # Um bias pra cada neurônio da camada oculta
        self.w2 = np.random.randn(10,1) * 0.1 # 10 neuronos na camada oculta e 1 de saída
        self.b2 = np.random.rand(1, 1)  * 0.1 # um peso pro neuronio de saída

    def sigmoide(self, x):
        return 1 / (1 + self.np.exp(-x))

    def relu(self, x):
        return self.np.maximum(0,x)

    def forward(self, x):
        z1 = x @ self.w1 + self.b1
        ativ = self.relu(z1)
        z2 = ativ @ self.w2 + self.b2
        pred = self.sigmoide(z2)
        return pred
    
    def mutar(self, quantidade, taxa=0.6):
        redes_filhas = []
        for _ in range(quantidade):
            nova_rede = RedeNeural(self.np)

            nova_rede.w1 = self.w1 + self.np.random.randn(*self.w1.shape) * taxa 
            nova_rede.b1 = self.b1 + self.np.random.randn(*self.b1.shape) * taxa 
            nova_rede.w2 = self.w2 + self.np.random.randn(*self.w2.shape) * taxa 
            nova_rede.b2 = self.b2 + self.np.random.randn(*self.b2.shape) * taxa 

            redes_filhas.append(nova_rede)

        return redes_filhas
