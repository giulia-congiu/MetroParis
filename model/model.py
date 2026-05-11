
from database.DAO import DAO
import networkx as nx
from datetime import datetime
import geopy.distance

'''lo scrivo fuori perchè è un metodo statico, non fa parte della classe!!'''
def getPesoPercorrenza(u, v, vel):
    dist = geopy.distance.distance((u.coordX, u.coordY),
                                   (v.coordX, v.coordY)).km
    #gli do due coordinate, inserite come due tuple, e lui mi dà la distanza tra loro
    #io poi posso sceliere in che distanza prendere il risultato
    time = dist/vel * 60 #minuti
    return time


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate() #leggo tutte le fermate dal DAO
        self._grafo = nx.DiGraph() #istanzio un grafo semplice e orientato
        '''Creo un idMap perchè mi serve passare dalla connessione alla fermata:
        creo un dizionario che posso interrogare con la chiave di uno dei valori di connessione (idArrivo in questo caso)
        e mi ritorna il valore corrispondente dell'altra dataclass, la fermata
        (in questo caso posso farlo nell'init ma non sempre)'''
        self._idMapFermate= {}
        for f in self._fermate:
            self._idMapFermate[f.id_fermata] = f
            #dato l'id della fermata (chiave primaria della dataclasss (uso quasi sempre quellA)),
            # ritorno l'oggetto fermata corrispondente

    def getShortestPath(self, u, v):
        return nx.single_source_dijkstra(self._grafo, u, v)

    '''VERSIONE 2 CON GRAFO PESATO PER TENER CONTO DEI PERCORSI DOPPI'''
    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        #self.addEdgesPesati() #Cambia solo come vado ad aggiungere gli archi
        self.addEdgesPesatiTempi()

    def addEdgesPesati(self):
        # versione 1: riutilizzare il principio di funzionamento del metodo addEdges3,
        # ma contando quante volte provo ad aggiungere l'arco
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]

            if self._grafo.has_edge(u, v):
                self._grafo[u][v]["weight"] += 1 #sfrutto il fatto che il grafo sia un dict
            else:
                self._grafo.add_edge(u, v, weight=1)

    def addEdgesPesatiV2(self):
        # Delega il calcolo del peso alla query sql nel dao, per semplificarci la vita in python
        #pensa sempre se è meglio complicare la query  e semplificare python o viceversa
        self._grafo.clear_edges()
        allEdgesWPeso = DAO.getAllEdgesPesati()
        # LISTA di tuple = [(id_stazP, id_stazA, peso), ..]

        for e in allEdgesWPeso:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = e[2]

            self._grafo.add_edge(u, v, weight=peso)

    def getArchiPesoMaggiore(self):
        #mi rida gli archi che hanno peso maggiogiore di 1
        #ovvero qle fermate collegate da più di 1 percorso
        edges = self._grafo.edges(data=True) #edges è un metodo di grafo che riceve data
        #data = true vuol dire che in edges mi salverò tutti gli archi con tutti i loro attributi compreso il loro peso
        #se data = false in edeges salva tutti gli archi ma SENZA GLI ATTRIBUTI, quindi senza peso

        edgesMaggiori = [] #seleziono quello con peso > 1
        for e in edges:
            if self._grafo.get_edge_data(e[0], e[1])["weight"] > 1: #gli passo un arco come coppia di nodi e chiedo l'attributo
                # self._grafo[e[0]][e[1]]["weight"]
                edgesMaggiori.append(e)
        return edgesMaggiori

    '''4 ESPLORAZIONI DEL GRAFO UGUALI A COPPIE, CAMBIA SOLO IL MODO IN CUI MI VIENE RIDATO L'OUTPUT
    IN UN CASO VIENE RESTITUITO a RAPPR A ARCHI IN UNO A RAPPR AD ALBERO'''

    def getBFSNodesFromEdges(self, source):
        archi = nx.bfs_edges(self._grafo, source) #iterable di tuple
        nodiBFS = []
        for u, v in archi: #u è il nodo da cui parto (l'ho già visto)
            nodiBFS.append(v)
        return nodiBFS

    def getBFSNodesFromTree(self, source):
        tree = nx.bfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi #dovrei escludere il nodo source

    def getDFSNodesFromEdges(self, source):
        archi = nx.dfs_edges(self._grafo, source)  # iterable di tuple
        nodiDFS = []
        for u, v in archi:  # u è il nodo da cui parto (l'ho già visto)
            nodiDFS.append(v)
        return nodiDFS

    def getDFSNodesFromTree(self, source):
        tree = nx.dfs_tree(self._grafo, source)
        archi = list(tree.edges())
        nodi = list(tree.nodes())
        return nodi


    def buildGraph(self):
        #voglio popolare il grafo con la lista di oggetti (fermate).
        #voglio quindi aggiungere nodi (le fermate) e archi (collegamenti tra fermate)
        #è bene assicurarsi che all'inizio il grafo sia vuoto altrimenti aggiungo nodi a uno esistente
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)

        #per verifiacare se l'ho costruito bene creo "testModel"
        # tic = datetime.now()
        # self.addedges()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 1: ", toc - tic)
        #
        # tic = datetime.now()
        # self.addedges2()
        # toc = datetime.now()
        # print("Tempo impiegato da modo 2: ", toc - tic)

        tic = datetime.now()
        self.addedges3()
        toc = datetime.now()
        print("Tempo impiegato da modo 3: ", toc-tic)

    '''SCRIVO 3 METODI DIVERSI PER RIEMPIRE IL GRAFO CHE DIFFRISCONO PER COME ?'''
    def addedges(self ):
        #ciclo su tutte le coppie di nodi e verifico col dao se tra quella coppia c'è una connessione,
        # se c'è aggiungo arco. Se ho un grafo di pochi nodi, ha senso utilizzare questo primo metodo.
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate: #questo doppio ciclo for è un po troppo lungo e fa perdere tempo
                if DAO.hasconn(u, v): #SE ritorna true:
                    self._grafo.add_edge(u, v) #posso aggiungere al grafo la coppia di nodi

    #siccome quesTO addedges1 è lento, penso a un altra soluzione
    def addedges2(self):
        #prendo tutti i nodi connessi a quella fermata e ??
        self._grafo.clear_edges()
        for u in self._fermate:
            for connessione in DAO.getvicini(u): #voglio l'elenco dei vicini del nodo
                v= self._idMapFermate[connessione.id_stazA]
                self._grafo.add_edge(u, v)
                
    '''posso fare ancora meglio di addedges2: posso pensare a un modo di costruire
    gli edge senza fare un ciclo for, ma solo leggendo la tabella connessioni: due nodi sono collegati
    solo se c'è una connessione tra loro, se leggo tutte le connessioni che ho nel dao ho fatto'''
    def addedges3(self): #funzione che mi tira fuori tutti gli archi.
        #in questo caso posso aggiungerli tutti in altri casi devo fare dei controlli.
        #questa funzione vede gli archi e se non stanno nel grafo li aggiunge
        self._grafo.clear_edges()
        alledges = DAO.getAllEdges()
        for conn in alledges:
            u = self._idMapFermate[conn.id_stazP]
            v = self._idMapFermate[conn.id_stazA]
            self._grafo.add_edge(u, v)

    '''adesso i pesi degli archi non sono più i numeri di linee che collegano due nodi'''

    def addEdgesPesatiTempi(self):
        '''Questo metodo crea degli archi, in cui il peso è pari al tempo di percorrenza di quell'arco,
        ottenuto come rapporto fra la distanza fra due stazioni e la velocità di percorrenza'''
        self._grafo.clear_edges()
        allEdgesVel = DAO.getAllEdgesVel()
        for e in allEdgesVel:
            u = self._idMapFermate[e[0]]
            v = self._idMapFermate[e[1]]
            peso = getPesoPercorrenza(u, v, e[2])
            self._grafo.add_edge(u, v, weight=peso)

    def get_numnodi(self):
        return len(self._grafo.nodes())

    def get_numarchi(self):
        return len(self._grafo.edges())

    @property
    def fermate(self):
        return self._fermate

