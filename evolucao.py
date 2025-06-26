import numpy as np
import time

from rede_neural import RedeNeural
from simulador import Simulador

TAMANHO_POPULACAO = 50
NUM_MAX_FRAMES = 10_000

def criar_geracao1():
    return [RedeNeural(np) for _ in range(TAMANHO_POPULACAO)]

def jogar_jogo(simulador, populacao):
    rank = []
    for individuo in populacao:
        simulador.definir_rede(individuo)
        num_fames_rodados = 0

        while simulador.dino_vivo and num_fames_rodados < NUM_MAX_FRAMES:
            simulador.rede_joga()
            simulador.atualizar_um_frame()
            num_fames_rodados += 1

            #print(f"Score: {simulador.score:.2f} | dino_vivo: {simulador.dino_vivo} ")
            #if 
                #print("rodou 10_000 frames")
                #break

        
        rank.append((simulador.score, individuo))

    return rank

def selecionar_melhores(rank, nmr_pais=5):
    nmr_pais = int(TAMANHO_POPULACAO * 0.05)
    rank.sort(reverse=True, key=lambda x: x[0] )
    return [rede for _,rede in rank[:nmr_pais]]

def gerar_proxima_geracao(rank):
    qnt_pais = TAMANHO_POPULACAO * 0.05
    qnt_variantes = (TAMANHO_POPULACAO / qnt_pais ) - 1

    qnt_pais = int(qnt_pais)
    qnt_variantes = int(qnt_variantes)

    pais = selecionar_melhores(rank)
    nova_populacao = []
    for pai in pais:
        nova_populacao.extend(pai.mutar(quantidade=qnt_variantes))
        nova_populacao.append(pai)

    return nova_populacao


sim = Simulador(np)
populacao = criar_geracao1()
for geracao in range(60):
    print(f"----- Geração: {geracao} -----")
    inicio = time.time()

    rank = jogar_jogo(sim, populacao)

    rank.sort(reverse=True, key=lambda x: x[0])
    scores = [score for score, _ in rank]
    melhor = scores[0]
    media = sum(scores) / len(scores)

    populacao = gerar_proxima_geracao(rank)

    fim = time.time()   
    print(f"Melhor score: {melhor:.2f}")
    print(f"Score médio: {media:.2f}")
    #print(f"Tempo da geração: {fim - inicio:.2f} segundos")

