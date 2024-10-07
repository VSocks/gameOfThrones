import re
import numpy as np
import networkx as nx  # Import networkx for graph operations

#Personagens a procurar
characters = ["Arya", "Bran", "Brienne", "Catelyn", "Cersei", "Daenerys", 
              "Jaime", "Melisandre", "Petyr", "Robert"]

#Cria matriz de adjacência vazia
interaction_matrix = np.zeros((len(characters), len(characters)), dtype=int)

#Procura índice do personagem na matriz
def get_character_index(character):
    if character in characters:
        return characters.index(character)
    return None

#Conta interações
def count_interactions(text, window=50):
    words = re.findall(r'\b\w+\b', text)  #Divide texto em palavras
    last_seen = {char: -1 for char in characters}  #Rastreia índice de última palavra vista para cada personagem
    
    for i, word in enumerate(words):
        if word in characters:
            x_index = get_character_index(word)
            if x_index is not None:
                #Checa por interações com outros personagens em até 50 palavras
                for j in range(i+1, min(i+window+1, len(words))):
                    if words[j] in characters and words[j] != word:
                        y_index = get_character_index(words[j])
                        if y_index is not None:
                            # Increment interaction count
                            interaction_matrix[x_index][y_index] += 1
                            interaction_matrix[y_index][x_index] += 1
                #Reseta índice de última palavra vista para cada personagem
                last_seen[word] = i

#Passo 1: lê arquivo e processa interações
with open('A-Clash-Of-Kings.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    count_interactions(text)

#Passo 2: inverte os pesos do grafp
#Adicionada pequena constante para evitar divisão por 0
interaction_matrix_inverted = np.max(interaction_matrix) - interaction_matrix + 1

#Passo 3: constrói grafo usando matriz invertida
G = nx.Graph()
for i in range(len(characters)):
    for j in range(len(characters)):
        if i != j and interaction_matrix_inverted[i][j] > 0:
            G.add_edge(characters[i], characters[j], weight=interaction_matrix_inverted[i][j])

#Passo 4: aplica algoritmo de Johnson
shortest_paths = dict(nx.johnson(G, weight='weight'))

#Passo 5: calcula o betweeness
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

#Passo 6: encontra personagem com maior betweeness
most_significant_character = max(betweenness_centrality, key=betweenness_centrality.get)
most_significant_value = betweenness_centrality[most_significant_character]

#Passo 7: imprime resultados
print("Character Interaction Adjacency Matrix:")
print("    " + " ".join(f"{char:8}" for char in characters))
for i, row in enumerate(interaction_matrix):
    print(f"{characters[i]:<8} {' '.join(map(str, row))}")

print("\nMost Significant Character by Betweenness Centrality:")
print(f"{most_significant_character} with a centrality value of {most_significant_value:.4f}")