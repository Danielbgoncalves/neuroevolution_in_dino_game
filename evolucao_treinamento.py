import numpy as np
import time

from rede_neural import RedeNeural
from simulador import Simulador

TAMANHO_POPULACAO = 100
NUM_MAX_FRAMES = 15_000

def criar_geracao1():
    return [RedeNeural(np) for _ in range(TAMANHO_POPULACAO)]

def jogar_jogo(populacao):
    rank = []
    for individuo in populacao:
        simulador = Simulador(np)
        simulador.definir_rede(individuo)
        num_fames_rodados = 0

        while simulador.dino_vivo and num_fames_rodados < NUM_MAX_FRAMES:
            simulador.rede_joga()
            simulador.atualizar_um_frame()
            num_fames_rodados += 1

            #print(f"Score: {simulador.score:.2f}, Input: {simulador.coleta_input()}, Output: {simulador.rede.forward(simulador.coleta_input())}")

        
        rank.append((simulador.score, individuo))

    return rank

def selecionar_melhores(rank, nmr_pais=5):
    nmr_pais = int(TAMANHO_POPULACAO * 0.05)
    rank.sort(reverse=True, key=lambda x: x[0] )
    return [rede for _,rede in rank[:nmr_pais]], rank

def gerar_proxima_geracao(rank):
    qnt_pais = TAMANHO_POPULACAO * 0.05
    qnt_variantes = (TAMANHO_POPULACAO / qnt_pais ) - 1

    qnt_pais = int(qnt_pais)
    qnt_variantes = int(qnt_variantes)

    pais, rank_ordenado = selecionar_melhores(rank)

    nova_populacao = []
    for pai in pais:
        nova_populacao.extend(pai.mutar(quantidade=qnt_variantes))
        nova_populacao.append(pai)

    return nova_populacao, rank_ordenado

def obter_dados(rank):
    scores = [score for score, _ in rank]
    melhor_score = scores[0]
    media_score = sum(scores) / len(scores)

    return melhor_score, media_score, rank[0][1]

""" A partir daqui começa a evolução """

#sim = Simulador(np)
populacao = criar_geracao1()
evoluindo = True
geracao = 0
inicio = time.time()
while evoluindo:
    print(f"----- Geração: {geracao} -----")
    geracao += 1
    
    rank = jogar_jogo(populacao)
    populacao, rank_ordenado = gerar_proxima_geracao(rank)
    melhor_score, media_score, melhor_rede = obter_dados(rank_ordenado)

    
    print(f"Melhor score: {melhor_score:.2f}")
    print(f"Score médio: {media_score:.2f}")

    if melhor_score > 800:
        np.savez(
                    "rede_pontuadora_800_vel_18_2.npz", 
                    w1=melhor_rede.w1, 
                    w2=melhor_rede.w2,
                    b1=melhor_rede.b1,
                    b2=melhor_rede.b2
                )
        evoluindo = False
        
    
fim = time.time()   
print("-"*20)
print(f"Tempo de evolução: {fim - inicio:.2f} segundos")