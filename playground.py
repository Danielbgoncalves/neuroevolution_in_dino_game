import numpy as np

# Rede neural
from rede_neural import RedeNeural

# Objetos para jogar com tela
from JogoComVisual.JogadorHumano import JogadorHumano
from JogoComVisual.JogadorRede import JogadorRede, JogadorRedeTurbo

"""
    Para poder jogar o jogo no modo usuario ou no modo com a rede neural 

    Quem vai jogar o jogo?
    1 - Jogador humano
    2 - Jogador com rede neural em velocidade normal
    3 - Jogador com rede neural em velocidade turbo


    => defina na variável ESCOLHA
"""

ESCOLHA = 3


if ESCOLHA == 1:
    jogador_humano = JogadorHumano()

elif ESCOLHA == 2:
    rede = RedeNeural(np)
    dados = np.load("RedesJaTreinadas/rede_pontuadora_120.npz")
    rede.setar_pesos_bias(
        dados["w1"], 
        dados["b1"], 
        dados["w2"], 
        dados["b2"]
    )
    velocidade_maxima_cacto = dados["velocidade_maxima_cacto"]
    taxa_gravidade = dados["taxa_de_gravidade"]

    jogador_rede = JogadorRede(rede, taxa_gravidade, velocidade_maxima_cacto)
   
else:
    rede = RedeNeural(np)
    dados = np.load("RedesJaTreinadas/rede_pontuadora_120.npz")
    rede.setar_pesos_bias(
        dados["w1"], 
        dados["b1"], 
        dados["w2"], 
        dados["b2"]
    )
    velocidade_maxima_cacto = dados["velocidade_maxima_cacto"]
    taxa_gravidade = dados["taxa_de_gravidade"]

    jogador_rede = JogadorRedeTurbo(rede, taxa_gravidade, velocidade_maxima_cacto)
    #jogador_rede.set_velocidade_maxima_cacto(dados["velocidade_maxima_cacto"])
   