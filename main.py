#geração de instâncias aleatórias.
import matplotlib.pyplot as plt
import numpy as np
import random
import time

#definição de parâmetros para a geração de instâncias.

Numero_De_Casos = 5 #quantas instâncias serão geradas para cada número de jogadores.
Valor_De_Orcamento_Minimo = 10000000
Valor_De_Orcamento_Maximo = 50000000
Numero_De_Jogadores_Minimo = 3
Numero_De_Jogadores_Maximo = 25
Valor_De_Jogador_Minimo = 100000
Valor_De_Jogador_Maximo = 30000000
Porcentagem_De_Melhoria_Minimo = 2  #um valor entre 0 a 100 por se tratar de porcentagem.
Porcentagem_De_Melhoria_Maximo = 17 #um valor entre 0 a 100 por se tratar de porcentagem.

#geração de instâncias.
Instancias = []
Instancia_Especifica = []
Orcamento = 0
Valor_De_Jogador = 0
Porcentagem_De_Melhoria = 0

for x in range(Numero_De_Jogadores_Minimo,Numero_De_Jogadores_Maximo + 1):
  for y in range(Numero_De_Casos):
    Instancia_Especifica = list([])
    Orcamento = random.randint(Valor_De_Orcamento_Minimo,Valor_De_Orcamento_Maximo)
    Instancia_Especifica.append(Orcamento)

    for z in range(x):
      Valor_De_Jogador = random.randint(Valor_De_Jogador_Minimo,Valor_De_Jogador_Maximo)
      Porcentagem_De_Melhoria = random.randint(Porcentagem_De_Melhoria_Minimo,Porcentagem_De_Melhoria_Maximo)
      Instancia_Especifica.append((Valor_De_Jogador,Porcentagem_De_Melhoria))

    Instancias.append(Instancia_Especifica)

#utilizando heurística
#função auxiliar para a ordenação do vetor de densidades.
def getDensidade(tupla):
  return tupla[1]

#aplicação do algoritmo com heurística para resolução das instâncias propostas.
Index = 0
Orcamento = 0
Numero_De_Jogadores = 0
Referencia_De_Jogador = 0
Densidades_Dos_Jogadores = []
Jogadores_Selecionados = []

Index_Otimo = 0
Custo_Atual = 0
Melhoria_Atual = 0

Custo_Vetor = 0
Melhoria_Vetor = 0

multiplicador = 10000

temposDeExecucaoHeuristica = []
quantidadeDeJogadoresHeuristica = []

#separar o vetor de instâncias pelo número de jogadores.
for x in range(Numero_De_Jogadores_Maximo - Numero_De_Jogadores_Minimo + 1):
  Index = x*Numero_De_Casos
  Numero_De_Jogadores = len(Instancias[Index]) - 1

  somaTempos = 0

  #separar o vetor de instâncias pelo número de casos.
  for y in range(Numero_De_Casos):
    tempoInicial = time.time()

    Densidades_Dos_Jogadores = []
    Jogadores_Selecionados = []
    Orcamento = Instancias[Index][0]
    Custo_Atual = Orcamento
    Melhoria_Atual = 0

    #calcular a densidade melhoria/custo de cada jogador.
    for jogador in range(1,Numero_De_Jogadores + 1):
      Densidades_Dos_Jogadores.append((jogador,Instancias[Index][jogador][1]*multiplicador/Instancias[Index][jogador][0]))

    #ordenar as densidades calculadas da maior para a menor.
    Densidades_Dos_Jogadores.sort(key = getDensidade, reverse = True)

    #selecionar, conforme o limite de custo, os jogadores que mais irão contribuir para maximizar a melhoria do time com o menor custo possível dentro do orçamento.
    for indice in range(Numero_De_Jogadores):
      if(Custo_Atual >= Instancias[Index][Densidades_Dos_Jogadores[indice][0]][0]):
        Jogadores_Selecionados.append(Densidades_Dos_Jogadores[indice][0])
        Custo_Atual = Custo_Atual - Instancias[Index][Densidades_Dos_Jogadores[indice][0]][0]
        Melhoria_Atual = Melhoria_Atual + Instancias[Index][Densidades_Dos_Jogadores[indice][0]][1]

      if( int(Custo_Atual) == 0):
        break

    tempoFinal = time.time()
    somaTempos = somaTempos + (tempoFinal - tempoInicial)

    Index += 1

  quantidadeDeJogadoresHeuristica.append(Numero_De_Jogadores)
  temposDeExecucaoHeuristica.append(somaTempos/Numero_De_Casos)

#processamento dos dados coletados para a confecção do gráfico.
valoresDeComparacoesAJDecrescente = {
    "BaseLine": temposDeExecucaoBaseline,
    "Heurística": temposDeExecucaoHeuristica,

}

quantidadeDeMedicoes = np.arange(len(quantidadeDeJogadoresHeuristica))
espesuraDasBarras = 0.2
multiplicador = 0
plt.rcParams['figure.figsize'] = [10,6]
cores = ['purple','green','yellow',"black"]
for grafico in [valoresDeComparacoesAJDecrescente]:
  contador = 0

  for infoAlgoritmo, infoColetada in grafico.items():
      plt.plot(quantidadeDeJogadoresHeuristica,infoColetada,label=infoAlgoritmo,marker="o",markerfacecolor = cores[contador])
      contador += 1

  plt.title("Comparação de Tempos algoritmo Baseline e algoritmo com Heurística")
  plt.xlabel("Número De Jogadores")
  plt.ylabel("Tempo Requerido (S)")
  plt.legend()
  plt.show()