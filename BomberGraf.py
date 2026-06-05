import networkx as nx
import random
import os

class JuegoGrafos:
    def __init__(self):
        self.jugador = (0, 0)
        self.llave = (4, 4)
        self.salida = (9, 9)
        self.generar_laberinto_con_alternativas()
        self.spawn_enemigos(cantidad=6)
        
        self.tiene_llave = False
        self.objetivo_actual = self.llave
        self.juego_activo = True

        # Colores ANSI para terminal
        self.C_BLANCO = "\033[1;97m"
        self.C_VERDE = "\033[1;92m"
        self.C_AMARILLO = "\033[1;93m"
        self.C_GRIS = "\033[90m"
        self.C_RESET = "\033[0m"

    def tiene_caminos_alternativos(self, grafo, inicio, fin):
        try:
            camino_principal = nx.shortest_path(grafo, inicio, fin)
            if len(camino_principal) <= 2:
                return True 
            grafo_prueba = grafo.copy()
            nodo_critico = camino_principal[len(camino_principal) // 2]
            grafo_prueba.remove_node(nodo_critico)
            return nx.has_path(grafo_prueba, inicio, fin)
        except nx.NetworkXNoPath:
            return False

    def generar_laberinto_con_alternativas(self):
        laberinto_valido = False
        intentos = 0 
        while not laberinto_valido:
            intentos += 1
            self.grafo_base = nx.grid_2d_graph(10, 10)
            self.muros = []
            probabilidad = 0.25 if intentos < 50 else 0.15
            
            for x in range(10):
                for y in range(10):
                    nodo = (x, y)
                    if nodo not in [self.jugador, self.llave, self.salida]:
                        if random.random() < probabilidad:
                            self.muros.append(nodo)
                            
            for muro in self.muros:
                self.grafo_base.remove_node(muro)
                
            if intentos > 100:
                if nx.has_path(self.grafo_base, self.jugador, self.llave) and nx.has_path(self.grafo_base, self.llave, self.salida):
                    laberinto_valido = True
            else:
                caminos_llave = self.tiene_caminos_alternativos(self.grafo_base, self.jugador, self.llave)
                caminos_salida = self.tiene_caminos_alternativos(self.grafo_base, self.llave, self.salida)
                if caminos_llave and caminos_salida:
                    laberinto_valido = True

    def spawn_enemigos(self, cantidad):
        nodos_disponibles = list(self.grafo_base.nodes())
        nodos_protegidos = [self.jugador, self.llave, self.salida]
        vecinos_jugador = list(self.grafo_base.neighbors(self.jugador))
        nodos_protegidos.extend(vecinos_jugador)
        nodos_validos = [n for n in nodos_disponibles if n not in nodos_protegidos]
        self.enemigos = random.sample(nodos_validos, cantidad)

    def coord_a_vertice(self, nodo):
        x, y = nodo
        numero = (y * 10) + x + 1
        return f"V{numero}"

    def calcular_caminos_ponderados(self):
        grafo_temp = self.grafo_base.copy()
        for enemigo in self.enemigos:
            if enemigo in grafo_temp:
                grafo_temp.remove_node(enemigo)
        
        if self.objetivo_actual not in grafo_temp or self.jugador not in grafo_temp:
            return []

        grafo_dir = grafo_temp.to_directed()
        for u, v in grafo_dir.edges():
            enemigos_cerca = 0
            vecinos_v = list(self.grafo_base.neighbors(v))
            for vecino in vecinos_v:
                if vecino in self.enemigos:
                    enemigos_cerca += 1
            grafo_dir[u][v]['peso'] = 1 + enemigos_cerca

        try:
            generador_caminos = nx.shortest_simple_paths(grafo_dir, self.jugador, self.objetivo_actual, weight='peso')
            top_caminos = []
            iteraciones_seguridad = 0
            
            w1 = -1
            w2 = -1
            
            for camino in generador_caminos:
                iteraciones_seguridad += 1
                
                # Límite amplio para permitir encontrar el salto de +5 pesos
                if iteraciones_seguridad > 15000:
                    break
                    
                peso_total = sum(grafo_dir[n1][n2]['peso'] for n1, n2 in zip(camino[:-1], camino[1:]))
                
                # Regla estricta de selección de pesos
                if len(top_caminos) == 0:
                    top_caminos.append((camino, peso_total))
                    w1 = peso_total
                elif len(top_caminos) == 1:
                    if peso_total > w1:
                        top_caminos.append((camino, peso_total))
                        w2 = peso_total
                elif len(top_caminos) == 2:
                    if peso_total >= w2 + 5:
                        top_caminos.append((camino, peso_total))
                        break
                
            return top_caminos
        except nx.NetworkXNoPath:
            return []

    def mover_enemigos(self):
        nuevos_enemigos = []
        for enemigo in self.enemigos:
            if random.randint(0, 100) <= 70:
                vecinos = list(self.grafo_base.neighbors(enemigo))
                vecinos_validos = [v for v in vecinos if v not in nuevos_enemigos and v not in self.enemigos]
                if vecinos_validos:
                    nuevos_enemigos.append(random.choice(vecinos_validos))
                else:
                    nuevos_enemigos.append(enemigo)
            else:
                nuevos_enemigos.append(enemigo)
        self.enemigos = nuevos_enemigos

    def imprimir_analisis_matematico(self, top_caminos):
        os.system('cls' if os.name == 'nt' else 'clear')

        if not top_caminos:
            return
            
        print("\n" + "="*55)
        print(" 🧠 ANÁLISIS MATEMÁTICO: MATRICES Y DIJKSTRA")
        print("="*55)
        
        grafo_dir = self.grafo_base.to_directed()
        for u, v in grafo_dir.edges():
            enemigos_cerca = 0
            for vecino in self.grafo_base.neighbors(v):
                if vecino in self.enemigos:
                    enemigos_cerca += 1
            grafo_dir[u][v]['peso'] = 1 + enemigos_cerca

        colores = [self.C_BLANCO, self.C_VERDE, self.C_AMARILLO]
        titulos = ["⭐ RUTA ÓPTIMA", "🟢 ALTERNATIVA 2", "🟡 ALTERNATIVA 3"]

        for idx, (ruta, peso_total) in enumerate(top_caminos):
            color = colores[idx]
            titulo = titulos[idx]
            
            print(f"\n{color}{'-'*55}")
            print(f" {titulo} (Costo Final: {peso_total})")
            print(f"{'-'*55}{self.C_RESET}")
            
            print(f"{color}[1] SUB-MATRIZ DE ADYACENCIA PONDERADA:{self.C_RESET}")
            header = "      " + "".join([f"{self.coord_a_vertice(n):<6}" for n in ruta])
            print(f"{color}{header}{self.C_RESET}")
            
            for u in ruta:
                fila = f"{self.coord_a_vertice(u):<5} "
                for v in ruta:
                    if grafo_dir.has_edge(u, v):
                        fila += f"{grafo_dir[u][v]['peso']:<6}"
                    elif u == v:
                        fila += "0     "
                    else:
                        fila += "∞     "
                print(f"{color}{fila}{self.C_RESET}")

            print(f"\n{color}[2] RASTREO DE DIJKSTRA (Relajación de Aristas):{self.C_RESET}")
            peso_acumulado = 0
            for i in range(len(ruta) - 1):
                u = ruta[i]
                v = ruta[i+1]
                costo_uv = grafo_dir[u][v]['peso']
                nom_u = self.coord_a_vertice(u)
                nom_v = self.coord_a_vertice(v)
                
                print(f"{color}Paso {i+1}: Arista ({nom_u} -> {nom_v}) | Peso: {costo_uv}")
                print(f"        Cálculo: d({nom_v}) = min(∞, {peso_acumulado} + {costo_uv}) = {peso_acumulado + costo_uv}{self.C_RESET}")
                peso_acumulado += costo_uv
                
            print(f"{color}✅ Costo total comprobado = {peso_acumulado}{self.C_RESET}")

    def imprimir_tablero(self, top_caminos):
        print("\n" + "="*55)
        print("                 MAPA DEL GRAFO")
        print("="*55)
        
        for y in range(10):
            fila = ""
            for x in range(10):
                nodo = (x, y)
                nombre = self.coord_a_vertice(nodo)
                
                if nodo in self.muros:
                    fila += "🧱   "
                elif nodo == self.jugador:
                    fila += "🏃   "
                elif nodo in self.enemigos:
                    fila += "👾   "
                elif nodo == self.llave and not self.tiene_llave:
                    fila += "🔑   "
                elif nodo == self.salida and self.tiene_llave:
                    fila += "🚪   "
                elif nodo == self.salida and not self.tiene_llave:
                    fila += "🔒   "
                else:
                    en_camino = False
                    if top_caminos:
                        for i, (ruta, _) in enumerate(top_caminos):
                            if nodo in ruta:
                                if i == 0:
                                    fila += f"{self.C_BLANCO}{nombre:<4}{self.C_RESET} "
                                elif i == 1:
                                    fila += f"{self.C_VERDE}{nombre:<4}{self.C_RESET} "
                                elif i == 2:
                                    fila += f"{self.C_AMARILLO}{nombre:<4}{self.C_RESET} "
                                en_camino = True
                                break 
                    if not en_camino:
                        fila += f"{self.C_GRIS}{nombre:<4}{self.C_RESET} "
            print(fila)
        
        print("="*55)
        if top_caminos:
            print("\n📊 ANÁLISIS DE RUTAS (Equilibrio Distancia/Riesgo):")
            for i, (ruta, peso) in enumerate(top_caminos):
                ruta_texto = " -> ".join([self.coord_a_vertice(n) for n in ruta])
                pasos_fisicos = len(ruta) - 1 
                if i == 0:
                    print(f"{self.C_BLANCO}⭐ ÓPTIMA (Peso {peso} | {pasos_fisicos} pasos):{self.C_RESET} {ruta_texto}")
                elif i == 1:
                    print(f"{self.C_VERDE}   Opción 2 (Peso {peso} | {pasos_fisicos} pasos):{self.C_RESET} {ruta_texto}")
                elif i == 2:
                    print(f"{self.C_AMARILLO}   Opción 3 (Peso {peso} | {pasos_fisicos} pasos):{self.C_RESET} {ruta_texto}")
            print("") 
        else:
            print("\nRuta óptima: [BLOQUEADA TEMPORALMENTE POR ENEMIGOS]\n")

    def jugar_turno(self, direccion):
        x, y = self.jugador
        nuevo_x, nuevo_y = x, y

        if direccion == "w": nuevo_y -= 1
        elif direccion == "s": nuevo_y += 1
        elif direccion == "a": nuevo_x -= 1
        elif direccion == "d": nuevo_x += 1

        nuevo_nodo = (nuevo_x, nuevo_y)

        if nuevo_nodo in self.grafo_base:
            self.jugador = nuevo_nodo
        else:
            print("¡Movimiento inválido hacia muro o límite del mapa!")
            return

        if self.jugador in self.enemigos:
            print("¡Un enemigo te ha atrapado! ☠️ FIN DEL JUEGO.")
            self.juego_activo = False
            return

        if self.jugador == self.llave and not self.tiene_llave:
            self.tiene_llave = True
            self.objetivo_actual = self.salida
            print("\n¡Llave conseguida! 🔑 Recalculando grafo hacia la SALIDA 🚪...")

        if self.jugador == self.salida and self.tiene_llave:
            print("\n¡Felicidades! Lograste escapar del grafo exitosamente. 🎉")
            self.juego_activo = False
            return

        self.mover_enemigos()

        if self.jugador in self.enemigos:
            print("¡Un enemigo te atrapó! ☠️ FIN DEL JUEGO.")
            self.juego_activo = False


if __name__ == "__main__":
    os.system('color') 
    juego = JuegoGrafos()
    
    print("OBJETIVOS: Consigue la Llave 🔑 y escapa por la Salida 🚪")
    print("CONTROLES: 'w' (arriba), 's' (abajo), 'a' (izquierda), 'd' (derecha), 'q' (salir)")
    input("\nPresiona ENTER para comenzar el análisis matemático del grafo...")
    
    while juego.juego_activo:
        top_caminos = juego.calcular_caminos_ponderados()
        
        juego.imprimir_analisis_matematico(top_caminos)
        juego.imprimir_tablero(top_caminos)
        
        movimiento = input("Ingresa tu movimiento (w/a/s/d) o 'q' para salir: ").lower()
        if movimiento == 'q':
            print("Juego cancelado.")
            break
        elif movimiento in ['w', 'a', 's', 'd']:
            juego.jugar_turno(movimiento)
        else:
            print("Tecla no válida. Usa w, a, s o d.")