#!/usr/bin/env python3

"""
Simulazione del Protocollo Distance Vector Routing

Questo script implementa una simulazione del protocollo Distance Vector Routing,
mostrando come i router scambiano informazioni e calcolano i percorsi più brevi.
"""

import time
from typing import Dict, List, Set, Tuple
import copy
import networkx as nx
import matplotlib.pyplot as plt

class Router:
    def __init__(self, name: str):
        """
        Inizializza un router con un nome specifico.
        
        Args:
            name (str): Nome identificativo del router
        """
        self.name = name
        self.neighbors: Dict[str, float] = {}  # Router vicini e costi diretti
        self.routing_table: Dict[str, Tuple[float, str]] = {}  # Destinazione: (Costo, Next Hop)
        
    def add_neighbor(self, neighbor_name: str, cost: float):
        """
        Aggiunge un router vicino con il relativo costo del collegamento.
        
        Args:
            neighbor_name (str): Nome del router vicino
            cost (float): Costo del collegamento
        """
        self.neighbors[neighbor_name] = cost
        # Inizializza la routing table con i vicini diretti
        self.routing_table[neighbor_name] = (cost, neighbor_name)
        # Il router conosce sempre se stesso con costo 0
        self.routing_table[self.name] = (0.0, self.name)

    def get_routing_table(self) -> Dict[str, Tuple[float, str]]:
        """
        Restituisce la tabella di routing corrente.
        
        Returns:
            Dict[str, Tuple[float, str]]: Tabella di routing
        """
        return self.routing_table

    def update_routing_table(self, neighbor_name: str, neighbor_table: Dict[str, Tuple[float, str]]) -> bool:
        """
        Aggiorna la tabella di routing basandosi sulle informazioni ricevute da un vicino.
        Implementa l'equazione di Bellman-Ford.
        
        Args:
            neighbor_name (str): Nome del router vicino
            neighbor_table (Dict[str, Tuple[float, str]]): Tabella di routing del vicino
            
        Returns:
            bool: True se la tabella è stata modificata, False altrimenti
        """
        modified = False
        cost_to_neighbor = self.neighbors[neighbor_name]

        for dest, (dest_cost, _) in neighbor_table.items():
            # Calcola il nuovo costo attraverso questo vicino
            new_cost = cost_to_neighbor + dest_cost
            
            # Se è una nuova destinazione o se abbiamo trovato un percorso migliore
            if (dest not in self.routing_table or 
                new_cost < self.routing_table[dest][0]):
                self.routing_table[dest] = (new_cost, neighbor_name)
                modified = True
                
        return modified

    def display_routing_table(self):
        """Visualizza la tabella di routing in formato leggibile."""
        print(f"\nTabella di routing per il Router {self.name}:")
        print("Destinazione | Costo | Next Hop")
        print("-" * 35)
        for dest, (cost, next_hop) in sorted(self.routing_table.items()):
            print(f"{dest:^11} | {cost:^5} | {next_hop:^8}")

class Network:
    def __init__(self):
        """Inizializza una rete vuota."""
        self.routers: Dict[str, Router] = {}
        self.graph = nx.Graph()

    def add_router(self, name: str):
        """
        Aggiunge un nuovo router alla rete.
        
        Args:
            name (str): Nome del router
        """
        self.routers[name] = Router(name)
        self.graph.add_node(name)

    def add_link(self, router1: str, router2: str, cost: float):
        """
        Aggiunge un collegamento bidirezionale tra due router.
        
        Args:
            router1 (str): Nome del primo router
            router2 (str): Nome del secondo router
            cost (float): Costo del collegamento
        """
        self.routers[router1].add_neighbor(router2, cost)
        self.routers[router2].add_neighbor(router1, cost)
        self.graph.add_edge(router1, router2, weight=cost)

    def visualize_network(self):
        """Visualizza la rete usando networkx e matplotlib."""
        plt.figure(figsize=(12, 8))
        
        # Definisce il layout della rete (posizione dei nodi)
        pos = {
            'A': (-2, 0),
            'B': (0, 2),
            'C': (2, 2),
            'D': (4, 0),
            'E': (2, -1),
            'F': (0, -1)
        }
        
        # Disegna i nodi
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                             node_size=1500, node_shape='s')
        
        # Disegna le etichette dei nodi
        nx.draw_networkx_labels(self.graph, pos)
        
        # Disegna gli archi e i loro pesi
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels)
        nx.draw_networkx_edges(self.graph, pos)
        
        plt.title("Topologia della Rete")
        plt.axis('off')
        plt.show()

    def simulate(self, max_iterations: int = 100):
        """
        Simula il processo di convergenza del protocollo Distance Vector.
        
        Args:
            max_iterations (int): Numero massimo di iterazioni
        """
        iteration = 0
        converged = False
        
        print("\nInizio simulazione Distance Vector Routing")
        print("=" * 50)

        # Visualizza la rete prima di iniziare la simulazione
        self.visualize_network()

        while not converged and iteration < max_iterations:
            iteration += 1
            changes = False
            
            print(f"\nIterazione {iteration}")
            print("-" * 20)

            # Per ogni router
            for router in self.routers.values():
                # Per ogni vicino del router
                for neighbor in router.neighbors:
                    # Il router riceve la tabella di routing dal vicino
                    neighbor_table = copy.deepcopy(self.routers[neighbor].get_routing_table())
                    # Aggiorna la propria tabella in base alle informazioni ricevute
                    if router.update_routing_table(neighbor, neighbor_table):
                        changes = True

            # Mostra le tabelle di routing correnti
            for router in self.routers.values():
                router.display_routing_table()

            if not changes:
                converged = True
                print("\nLa rete è convergente!")
            
            time.sleep(1)  # Pausa per rendere l'output più leggibile

        if not converged:
            print("\nAttenzione: Raggiunto il numero massimo di iterazioni senza convergenza")

def main():
    """Funzione principale che crea e simula una rete di esempio."""
    # Crea una rete di esempio
    network = Network()
    
    # Aggiunge i router
    routers = ['A', 'B', 'C', 'D', 'E', 'F']
    for router in routers:
        network.add_router(router)
    
    # Aggiunge i collegamenti con i costi come mostrato nel diagramma
    network.add_link('A', 'B', 1)  # A-B: 1
    network.add_link('A', 'F', 3)  # A-F: 3
    network.add_link('B', 'C', 3)  # B-C: 3
    network.add_link('B', 'F', 1)  # B-F: 1
    network.add_link('B', 'E', 5)  # B-E: 5
    network.add_link('C', 'D', 2)  # C-D: 2
    network.add_link('D', 'E', 1)  # D-E: 1
    network.add_link('E', 'F', 2)  # E-F: 2
    network.add_link('D', 'F', 6)  # D-F: 6
    
    print("\nCosti dei collegamenti:")
    print("A-B: 1   B-C: 3   C-D: 2")
    print("A-F: 3   B-F: 1   D-E: 1")
    print("B-E: 5   E-F: 2   D-F: 6")
    
    # Avvia la simulazione
    network.simulate()

if __name__ == "__main__":
    main()
