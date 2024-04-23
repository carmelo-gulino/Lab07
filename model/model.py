from collections import defaultdict

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.situazioni = {}
        self.initialize()

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

    def sequenza_ricorsiva(self, mese, gg):
        # CASO BANALE: se sono all'ultimo giorno, scelgo il costo minimo tra le umidità
        if gg == 0:
            min = 10000
            l = None
            for localita in self.situazioni.keys():
                for s in self.situazioni[localita][mese]:
                    if s.umidita < min:
                        min = s.umidita  #umidita minima
                        l = localita  #localita in cui c'è umidita minima
            min += 100  #aggiungo 100 perché è il primo spostamento
