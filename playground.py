import numpy as np

# Rede neural
from rede_neural import RedeNeural

# Objetos para jogar com tela
from JogoComVisual.JogadorHumano import JogadorHumano
from JogoComVisual.JogadorRede import JogadorRede

"""
    Para poder jogar o jogo no modo usuario ou no modo com a rede neural 
"""

print("Quem vai jogar ?")
print("1 Jogador humano")
print("2 Rede Treinada")
#escolha = int(input("=> "))
escolha = 2
if escolha == 1:
    jogador_humano = JogadorHumano()
else:
    rede = RedeNeural(np)
    dados = np.load("RedesJaTreinadas/rede_pontuadora_800.npz")
    rede.setar_pesos_bias(
        dados["w1"], 
        dados["b1"], 
        dados["w2"], 
        dados["b2"]
    )
    jogador_rede = JogadorRede(rede)