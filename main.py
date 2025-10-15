import graphviz  # Para visualização - INSTALE: pip install graphviz

class Grafo:
    def __init__(self):
        self.direcionado = False
        self.lista_adj = {}
        self.vertices = []
    
    def carregar_arquivo(self, nome_arquivo):
        """Carrega grafo a partir de arquivo"""
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                # Primeira linha: D ou ND
                primeira_linha = arquivo.readline().strip().upper()
                self.direcionado = (primeira_linha == "D")
                
                # Lê arestas
                for linha in arquivo:
                    linha = linha.strip()
                    if linha:
                        partes = linha.split()
                        if len(partes) >= 2:
                            v1, v2 = partes[0].upper(), partes[1].upper()
                            self._adicionar_aresta(v1, v2)
            
            print(f"Grafo carregado: {len(self.vertices)} vértices")
            return True
            
        except FileNotFoundError:
            print(f"Arquivo '{nome_arquivo}' não encontrado!")
            return False
        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return False
    
    def _adicionar_vertice(self, v):
        """Adiciona vértice se não existir"""
        if v not in self.lista_adj:
            self.lista_adj[v] = []
            self.vertices.append(v)
    
    def _adicionar_aresta(self, v1, v2):
        """Adiciona aresta ao grafo"""
        self._adicionar_vertice(v1)
        self._adicionar_vertice(v2)
        self.lista_adj[v1].append(v2)
    
    # === FUNÇÃO 1: VERIFICAR ADJACÊNCIA ===
    def verificar_adjacencia(self, v1, v2):
        """Receber dois vértices vX e vY e informar se eles são adjacentes"""
        v1, v2 = v1.upper(), v2.upper()
        
        if v1 not in self.lista_adj or v2 not in self.lista_adj:
            return False
        
        # Para grafo dirigido: verifica se v1 -> v2
        if self.direcionado:
            return v2 in self.lista_adj[v1]
        else:
            # Para não-dirigido: verifica ambas direções
            return (v2 in self.lista_adj[v1]) or (v1 in self.lista_adj[v2])
    
    # === FUNÇÃO 2: CALCULAR GRAU ===
    def calcular_grau(self, vertice):
        """Receber um vértice e calcular o seu grau"""
        vertice = vertice.upper()
        
        if vertice not in self.lista_adj:
            return None
        
        if not self.direcionado:
            # Grau para não-dirigido
            return len(self.lista_adj[vertice])
        else:
            # Para dirigidos: grau de entrada e saída
            grau_saida = len(self.lista_adj[vertice])
            
            grau_entrada = 0
            for v in self.lista_adj:
                if vertice in self.lista_adj[v]:
                    grau_entrada += 1
            
            return grau_saida, grau_entrada
    
    # === FUNÇÃO 3: LISTAR VIZINHOS ===
    def listar_vizinhos(self, vertice):
        """Receber um vértice e exibir todos os seus vizinhos"""
        vertice = vertice.upper()
        
        if vertice not in self.lista_adj:
            return None
        
        if not self.direcionado:
            # Para não-dirigido: todos os vizinhos
            return self.lista_adj[vertice]
        else:
            # Para dirigido: sucessores (saída) e predecessores (entrada)
            sucessores = self.lista_adj[vertice]
            predecessores = []
            for v in self.lista_adj:
                if vertice in self.lista_adj[v]:
                    predecessores.append(v)
            
            return sucessores, predecessores
    
    # === FUNÇÃO 4: LISTAR ARESTAS ===
    def listar_arestas(self):
        """Exibir todas as arestas do grafo no formato (v1, v2)"""
        arestas = []
        
        if not self.direcionado:
            # Para não-dirigido: evita duplicatas
            visitadas = set()
            for v1 in self.lista_adj:
                for v2 in self.lista_adj[v1]:
                    aresta = tuple(sorted([v1, v2]))
                    if aresta not in visitadas:
                        arestas.append(f"({v1}, {v2})")
                        visitadas.add(aresta)
        else:
            # Para dirigido: todas as arestas
            for v1 in self.lista_adj:
                for v2 in self.lista_adj[v1]:
                    arestas.append(f"({v1}, {v2})")
        
        return arestas
    
    # === FUNÇÃO 6: DETECTAR CICLOS EM DEPENDÊNCIAS ===
    def detectar_ciclos(self):
        """
        Detecta ciclos em grafos dirigidos (dependências)
        Retorna: (tem_ciclo, ciclo_encontrado)
        """
        if not self.direcionado:
            print("AVISO: Esta função é para grafos dirigidos!")
            return False, []
        
        visitado = set()
        pilha_recursao = set()
        pai = {}  # Para rastrear o caminho do ciclo
        
        def dfs_detectar_ciclo(vertice):
            visitado.add(vertice)
            pilha_recursao.add(vertice)
            
            for vizinho in self.lista_adj.get(vertice, []):
                if vizinho not in visitado:
                    pai[vizinho] = vertice
                    ciclo = dfs_detectar_ciclo(vizinho)
                    if ciclo:
                        return ciclo
                elif vizinho in pilha_recursao:
                    # Ciclo detectado! Reconstruir o ciclo
                    ciclo = []
                    atual = vertice
                    # Reconstruir o ciclo do fim para o início
                    while atual != vizinho:
                        ciclo.append(atual)
                        atual = pai.get(atual)
                    ciclo.append(vizinho)
                    ciclo.append(vertice)  # Fechar o ciclo
                    ciclo.reverse()
                    return ciclo
            
            pilha_recursao.remove(vertice)
            return None
        
        # Verificar todos os vértices (para grafos não conexos)
        for vertice in self.vertices:
            if vertice not in visitado:
                pai[vertice] = None
                ciclo = dfs_detectar_ciclo(vertice)
                if ciclo:
                    return True, ciclo
        
        return False, []
    
    def verificar_dependencias(self):
        """
        Verifica se a estrutura de dependências é válida
        Informa se há dependências circulares e lista os módulos do ciclo
        """
        if not self.direcionado:
            print("AVISO: Esta verificação é para grafos dirigidos de dependências!")
            return
        
        tem_ciclo, ciclo = self.detectar_ciclos()
        
        print("\n" + "="*60)
        print("VERIFICAÇÃO DE DEPENDÊNCIAS")
        print("="*60)
        
        if tem_ciclo:
            print("❌ DEPENDÊNCIA CIRCULAR DETECTADA!")
            print(f"🔁 Ciclo encontrado: {' -> '.join(ciclo)}")
            print("\nMódulos envolvidos no ciclo:")
            for i, modulo in enumerate(ciclo[:-1]):
                print(f"  {modulo} -> {ciclo[i+1]}")
        else:
            print("✅ ESTRUTURA DE DEPENDÊNCIAS VÁLIDA!")
            print("Não foram encontradas dependências circulares")
        
        print("="*60)
    
    # === FUNÇÃO 5: VISUALIZAÇÃO GRÁFICA ===
    def visualizar_grafo(self, nome_arquivo="grafo", formato="png"):
        """Gerar visualização gráfica do grafo - arquivo de imagem .png"""
        try:
            if self.direcionado:
                dot = graphviz.Digraph(comment='Grafo Dirigido')
            else:
                dot = graphviz.Graph(comment='Grafo Não-Dirigido')
            
            # Adiciona vértices
            for vertice in self.vertices:
                dot.node(vertice, vertice)
            
            # Adiciona arestas
            if not self.direcionado:
                # Para não-dirigido: evita duplicatas
                visitadas = set()
                for v1 in self.lista_adj:
                    for v2 in self.lista_adj[v1]:
                        aresta = tuple(sorted([v1, v2]))
                        if aresta not in visitadas:
                            dot.edge(v1, v2)
                            visitadas.add(aresta)
            else:
                # Para dirigido: todas as arestas
                for v1 in self.lista_adj:
                    for v2 in self.lista_adj[v1]:
                        dot.edge(v1, v2)
            
            # Salva arquivo de imagem
            dot.render(nome_arquivo, format=formato, cleanup=True)
            print(f"Visualização salva como '{nome_arquivo}.{formato}'")
            return True
            
        except Exception as e:
            print(f"Erro ao gerar visualização: {e}")
            print("Instale: pip install graphviz")
            return False

def esperar(mensagem="Pressione qualquer tecla para continuar..."):
    try:
        import msvcrt
        print(mensagem, end='', flush=True)
        msvcrt.getch()  # espera qualquer tecla (não precisa Enter)
        print()
    except Exception:
        # fallback multiplataforma (requere Enter)
        input(mensagem)

def main():

    grafo = Grafo()
    
    print("\nProjeto de EDA - Detecção de ciclos em grafos")
    print("Autores: Paulo Vitor Fontes do Nascimento e João Vitor Costa Leite Virginio da Silva\n")

    nome_arquivo = input("Digite o nome do arquivo .txt do grafo: ").strip()
    
    # Carrega arquivo
    if not grafo.carregar_arquivo(nome_arquivo):
        return
    
    print("Grafo dirigido?", "Sim" if grafo.direcionado else "Não")
    
    print("\n" + "="*50)
    
    
    # Menu
    while True:  # loop do menu
        print("\n_______MENU_______")

        print("1-Verificar adjascencia")
        print("2-Verificar grau de um vértice")
        print("3-Listar Vizinhos de um vértice")
        print("4-Listar arestas")
        print("5-Exportar grafo em png")
        print("6-Verificar dependências circulares")
        print("7-Sair\n")

        escolha = input("escolha uma opção: ").strip()

        if escolha == '1':
            v1 = input("digite o vértice 1: ").strip().upper()
            v2 = input("digite o vértice 2: ").strip().upper()

            if grafo.verificar_adjacencia(v1, v2):
                print(f"\nos vértices {v1} e {v2} são adjascentes.")
            else:
                print(f"\nos vértices {v1} e {v2} não são adjascentes.")
            esperar()

        elif escolha == '2':
            
            vertice = input("digite o vertice: ").strip().upper()
            resultado_grau = grafo.calcular_grau(vertice)
            if grafo.direcionado and isinstance(resultado_grau, tuple):
                print(f"Grau de {vertice} - Saída:", resultado_grau[0], "Entrada:", resultado_grau[1])
            else:
                print(f"Grau de {vertice}:", resultado_grau)
            print()
            esperar()

        elif escolha == '3':
            vertice = input("digite o vertice: ").strip().upper()
            vizinhos = grafo.listar_vizinhos(vertice)
            if grafo.direcionado and isinstance(vizinhos, tuple):
                print(f"Vizinhos de {vertice} - Sucessores:", vizinhos[0])
                print(f"Vizinhos de {vertice} - Predecessores:", vizinhos[1])
            else:
                print(f"Vizinhos de {vertice}:", vizinhos)
            print()
            esperar()

        elif escolha == '4':
            print("ARESTAS do grafo:")
            arestas = grafo.listar_arestas()
            for aresta in arestas:
                print(aresta)
            print()
            esperar()

        elif escolha == '5':
            print("5. VISUALIZAÇÃO GRÁFICA")
            if grafo.visualizar_grafo():
                print("✓ Visualização gerada com sucesso!")
            else:
                print("✗ Erro na geração da visualização")
            print()

        elif escolha == '6':
            print("6. VERIFICAÇÃO DE DEPENDÊNCIAS CIRCULARES")
            grafo.verificar_dependencias()
            esperar()

        elif escolha == '7':
            print("saindo...")
            break

        else:
            print("opcao invalida, tente novamente.")
            esperar()

if __name__ == "__main__":
    main()