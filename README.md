# Simulazione Protocollo di Routing Distance Vector

Questo progetto implementa una simulazione del protocollo Distance Vector Routing in Python. Il progetto dimostra i concetti fondamentali del routing distribuito e come i router calcolano i percorsi più brevi verso le destinazioni.

## Descrizione

Il programma simula una rete di router che utilizzano il protocollo Distance Vector Routing per:
- Mantenere tabelle di routing locali
- Scambiare informazioni di routing con i vicini
- Calcolare i percorsi più brevi verso tutte le destinazioni
- Implementare l'algoritmo di Bellman-Ford distribuito

## Struttura del Progetto

- `distance_vector_routing.py`: File principale contenente l'implementazione della simulazione
- `README.md`: Documentazione del progetto
- `requirements.txt`: Dipendenze del progetto

## Come Eseguire

1. Creare e attivare l'ambiente virtuale:
```bash
# Creare l'ambiente virtuale
python -m venv venv

# Attivare l'ambiente virtuale
# Su macOS/Linux:
source venv/bin/activate
# Su Windows:
# venv\Scripts\activate
```

2. Installare le dipendenze:
```bash
pip install -r requirements.txt
```

3. Eseguire il programma:
```bash
python distance_vector_routing.py
```

## Output

Il programma mostrerà:
1. La topologia iniziale della rete (versione grafica)
Dopo aver chiuso la finestra mostrerà nel terminale:
2. Le tabelle di routing per ogni router ad ogni iterazione
3. Il processo di convergenza del protocollo
4. Le tabelle di routing finali dopo la convergenza

## Implementazione

Il progetto implementa:
- Classe Router per rappresentare i nodi della rete
- Tabelle di routing con distanze e next-hop
- Logica di aggiornamento delle tabelle di routing
- Simulazione dello scambio di informazioni tra router
- Visualizzazione delle tabelle di routing

## Autore
Daniele Merighi
