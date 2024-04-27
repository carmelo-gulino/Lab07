import flet as ft
from time import time
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese!")
        else:
            output = {}
            for localita in self._model.situazioni.keys():
                somma = 0
                n = 0
                for situazione in self._model.situazioni[localita][self._mese]:
                    somma += situazione.umidita
                    n += 1
                output[localita] = somma / n
            self._view.print_umidita_media(output)

    def handle_sequenza(self, e):
        self._model.trova_sequenza(self._mese)

    def read_mese(self, e):
        self._mese = int(e.control.value)
