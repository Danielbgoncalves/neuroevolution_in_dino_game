import numpy as np

# Rede neural
from rede_neural import RedeNeural

# Objetos para jogar com tela
from JogoComVisual.JogadorHumano import JogadorHumano
from JogoComVisual.JogadorRede import JogadorRede

"""
    Para poder jogar o jogo no modo usuario ou no modo com a rede neural 

    Quem vai jogar o jogo?
    1 - Jogador humano
    2 - Jogador com rede neural
    
    => defina na variável ESCOLHA
"""

ESCOLHA = 2


if ESCOLHA == 1:
    jogador_humano = JogadorHumano()
else:
    rede = RedeNeural(np)
    dados = np.load("RedesJaTreinadas/rede5.npz")
    rede.setar_pesos_bias(
        dados["w1"], 
        dados["b1"], 
        dados["w2"], 
        dados["b2"]
    )
    velocidade_maxima_cacto = dados["velocidade_maxima_cacto"]
    taxa_gravidade = dados["taxa_de_gravidade"]

    jogador_rede = JogadorRede(rede, taxa_gravidade, velocidade_maxima_cacto)
    #jogador_rede.set_velocidade_maxima_cacto(dados["velocidade_maxima_cacto"])
   