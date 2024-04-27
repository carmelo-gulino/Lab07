import copy
from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.soluzione = None
        self.situazioni = {}
        self.initialize()
        self.count_localita = {}  #tiene il conto di quante volte ho attraversato una località

    def initialize(self):
        for situazione in MeteoDao.get_all_situazioni():
            try:
                self.situazioni[situazione.localita][situazione.get_mese()].append(situazione)
            except KeyError:
                try:
                    self.situazioni[situazione.localita][situazione.get_mese()] = []
                    self.situazioni[situazione.localita][situazione.get_mese()].append(situazione)
                except KeyError:
                    self.situazioni[situazione.localita] = {}
                    self.situazioni[situazione.localita][situazione.get_mese()] = []
                    self.situazioni[situazione.localita][situazione.get_mese()].append(situazione)

    def trova_sequenza(self, mese):
        self.sequenza_ricorsiva([], mese)

    def sequenza_ricorsiva(self, parziale, mese):
        """
        Questo algoritmo si occupa di trovare soltanto i percorsi possibili e di memorizzarne i costi di umidità
        """
        # CASO BANALE: se ho trovato 15 città, aggiungo alle soluzioni possibili
        if len(parziale) == 3 and self.filtro_costo(parziale):
            self.soluzione = copy.deepcopy(parziale)  # faccio una copia per non modificarla in seguito
            print(self.soluzione)
        # CASO RICORSIVO: per ogni città che esploro, scendo scegliendo il minimo fino ad arrivare in fondo
        else:
            gg_esplorati = len(parziale)
            for localita in self.situazioni.keys():
                if len(parziale) < 3:
                    s = self.situazioni[localita][mese][gg_esplorati]
                    self.aggiungi_localita(localita, parziale, s)  #lo aggiungo preventivamente
                    self.aggiungi_costo_fisso(parziale)
                    if self.filtri_giorni(localita, s, parziale):  #verifico se il percorso aggiornato è ammissibile
                        self.sequenza_ricorsiva(parziale, mese)  #se è ammissibile continuo con l'algoritmo
                        self.count_localita[localita] -= 1  #se lo uso, scalo il conteggio prima del backtracking
                parziale.pop()  #se non è ammissibile lo rimuovo

    def aggiungi_localita(self, localita, parziale, s):
        if len(parziale) == 0:
            parziale.append((localita, s.umidita, s.umidita))
        else:
            parziale.append((localita, s.umidita, parziale[-1][2] + s.umidita))  #aggiungo località, umidità e cumulato

    def check_soluzione(self, parziale):
        if self.soluzione is None:
            return True
        else:
            if self.soluzione[-1][2] < parziale[-1][2]:
                return False
            else:
                return True

    def filtri_giorni(self, localita, s, parziale):
        """
        Funzione contenitore dei due filtri per i giorni
        """
        try:
            if len(parziale) == 1:  #alla prima iterazione aggiungo la città
                self.count_localita[localita] += 1  #aggiorno il conteggio
                return True
            else:
                if self.check_sei_giorni(localita) and self.check_due_giorni(parziale, localita):  #verifico
                    self.count_localita[localita] += 1  #aggiorno il conteggio
                    return True
                else:
                    return False  #se non posso aggiungere restituisco falso
        except KeyError:
            self.count_localita[localita] = 0  # se non ci sono ancora passato, creo la chiave
            self.count_localita[localita] += 1  #inizializzo il conteggio
            return True

    def check_sei_giorni(self, localita):
        """
        Controlla che non sia stato più di 6 giorni nella stessa città
        """
        if self.count_localita[localita] < 2:
            return True
        else:
            return False

    def check_due_giorni(self, parziale, localita):
        '''
        Controlla che ultimo (appena aggiunto), penultimo e terzultimo siano uguali
        '''
        """if len(parziale) == 2 and parziale[-1][0] == parziale[-2][0]:  # se ho una sola tappa, devono essere uguali ultima e penultima
            return True
        elif parziale[-1][0] == parziale[-2][0] and parziale[-2][0] == parziale[-3][0]:
            return True
        else:
            return False"""
        if parziale[-1][0] == parziale[-2][0]:  #PROVVISORIO
            return True
        else:
            return False

    def aggiungi_costo_fisso(self, parziale):
        '''
        Aggiunge il costo fisso di 100 se si è cambiato città, dopo aver aggiunto la nuova tappa
        '''
        if len(parziale) > 1 and parziale[-1][0] != parziale[-2][0]:    #aggiungo 100 solo dalla seconda tappa in poi
            parziale[-1][2] += 100  #aggiungo 100 al valore cumulato

    def filtro_costo(self, parziale):
        '''
        Confronta il valore cumulato della soluzione trovata con quello dell'ultima soluzione registrata, a meno che non
        sia la prima trovata
        '''
        if self.soluzione is None:  #prima soluzione trovata
            return True
        elif parziale[-1][2] <= self.soluzione[-1][2]:  #se nom è la prima soluzione confronto
            return True
