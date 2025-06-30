"""import numpy as np
import time

from rede_neural import RedeNeural
from simulador import Simulador

TAMANHO_POPULACAO = 100
NUM_MAX_FRAMES = 50_000

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

### A partir daqui começa a evolução 

populacao = criar_geracao1()
evoluindo = True
geracao = 0
inicio = time.time()
simulador = Simulador(np)
while evoluindo:
    print(f"----- Geração: {geracao} -----")
    geracao += 1
    
    rank = jogar_jogo(simulador, populacao)
    populacao, rank_ordenado = gerar_proxima_geracao(rank)
    melhor_score, media_score, melhor_rede = obter_dados(rank_ordenado)

    
    print(f"Melhor score: {melhor_score:.2f}")
    print(f"Score médio: {media_score:.2f}")

    if melhor_score > 1000: 
        np.savez(
                    "rede5.npz", 
                    w1=melhor_rede.w1, 
                    w2=melhor_rede.w2,
                    b1=melhor_rede.b1,
                    b2=melhor_rede.b2,
                    velocidade_maxima_cacto=simulador.VELOCIDADE_MAXIMA_CACTO,
                    velocidade_maxima_sobreviveido=simulador.cactos_vel,
                    taxa_de_gravidade=simulador.TAXA_GRAVIDADE
                )

        evoluindo = False
        
    
fim = time.time()   
print("-"*30)
print("Velocidade máxima dos cactos no melhor treino:", simulador.VELOCIDADE_MAXIMA_CACTO),
print(f"Tempo de evolução: {fim - inicio:.2f} segundos")"""

# Na dificuldade
# TAXA_GRAVIDADE = 0.051
# VELOCIDADE_MAXIMA_CACTO = 21
# dezenas de gerações tiveram o resultado estagnado em:
# ----- Geração: 64 -----
# Melhor score: 161.56
# Score médio: 15.22

#################################
"   2 formas de evolução, a de cima a variabilidade 'genética' ente pais e filhos é constante"
"   na de baixo, ela é regrada de acordo com a evolução das populações anteriores"
"   Eu esperaria que a de baixo se saisse melhor, mas no geral evoluem de modo parecido"
#################################

import numpy as np
import time

from rede_neural import RedeNeural
from simulador import Simulador

TAMANHO_POPULACAO = 100
NUM_MAX_FRAMES = 50_000

# Parâmetros da taxa adaptativa
TAXA_INICIAL = 0.5
GERACOES_SEM_MELHORIA_LIMITE = 5  
FATOR_AUMENTO = 1.1  
TAXA_MAXIMA = 4  

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
        
        rank.append((simulador.score, individuo))

    return rank

def selecionar_melhores(rank, nmr_pais=5):
    nmr_pais = int(TAMANHO_POPULACAO * 0.05)
    rank.sort(reverse=True, key=lambda x: x[0])
    return [rede for _, rede in rank[:nmr_pais]], rank

def gerar_proxima_geracao(rank, taxa_mutacao):
    qnt_pais = TAMANHO_POPULACAO * 0.05
    qnt_variantes = (TAMANHO_POPULACAO / qnt_pais) - 1

    qnt_pais = int(qnt_pais)
    qnt_variantes = int(qnt_variantes)

    pais, rank_ordenado = selecionar_melhores(rank)

    nova_populacao = []
    for pai in pais:
        nova_populacao.extend(pai.mutar(quantidade=qnt_variantes, taxa=taxa_mutacao))
        nova_populacao.append(pai)

    return nova_populacao, rank_ordenado

def obter_dados(rank):
    scores = [score for score, _ in rank]
    melhor_score = scores[0]
    media_score = sum(scores) / len(scores)

    return melhor_score, media_score, rank[0][1]

### A partir daqui começa a evolução 

populacao = criar_geracao1()
evoluindo = True
geracao = 0
inicio = time.time()
simulador = Simulador(np)

# Variáveis simples para controle da taxa
taxa_mutacao = TAXA_INICIAL
melhor_score_anterior = 0
geracoes_sem_melhoria = 0

while evoluindo:
    print(f"----- Geração: {geracao} -----")
    geracao += 1
    
    rank = jogar_jogo(simulador, populacao)
    populacao, rank_ordenado = gerar_proxima_geracao(rank, taxa_mutacao)
    melhor_score, media_score, melhor_rede = obter_dados(rank_ordenado)

    # Lógica simples: se não melhorou por várias gerações, aumenta um pouco a taxa
    if melhor_score <= melhor_score_anterior:
        geracoes_sem_melhoria += 1
    else:
        geracoes_sem_melhoria = 0
        melhor_score_anterior = melhor_score
        # Quando melhora, volta para taxa normal
        taxa_mutacao = TAXA_INICIAL

    # Se estagnado por muito tempo, aumenta suavemente a taxa
    if geracoes_sem_melhoria >= GERACOES_SEM_MELHORIA_LIMITE:
        taxa_mutacao = min(taxa_mutacao * FATOR_AUMENTO, TAXA_MAXIMA)
        geracoes_sem_melhoria = 0  # Reset
        print(f"Taxa de mutação ajustada para: {taxa_mutacao:.3f}")

    print(f"Melhor score: {melhor_score:.2f}")
    print(f"Score médio: {media_score:.2f}")
    print(f"Taxa atual: {taxa_mutacao:.3f}")

    if melhor_score > 120:
        np.savez(
            "rede_pontuadora_150.npz", 
            w1=melhor_rede.w1, 
            w2=melhor_rede.w2,
            b1=melhor_rede.b1,
            b2=melhor_rede.b2,
            velocidade_maxima_cacto=simulador.VELOCIDADE_MAXIMA_CACTO,
            velocidade_maxima_sobreviveido=simulador.cactos_vel,
            taxa_de_gravidade=simulador.TAXA_GRAVIDADE
        )
        evoluindo = False

fim = time.time()   
print("-"*30)
print("Velocidade máxima dos cactos no melhor treino:", simulador.VELOCIDADE_MAXIMA_CACTO)
print(f"Tempo de evolução: {fim - inicio:.2f} segundos")
print(f"Taxa final de mutação: {taxa_mutacao:.3f}")
