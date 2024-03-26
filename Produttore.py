import threading
import time

import rubrica


class Produttore(threading.Thread):

    def __init__(self, rub, i):
        super().__init__(name="Produttore"+str(i))
        self.c = rub

    def run(self):
        print(self.c)
        self.c.inserisci("gigi", "rossi", 3456789)
        self.c.inserisci("Gigi", "rossi", 3456789)
        self.c.inserisci("mario", "rossi", 3478999)
        time.sleep(2)

        self.c.inserisci("mario romualdo", "rossi", 3475599)
        self.c.inserisci("Alberto", "Alberti", 3475599)
        self.c.inserisci("Carlo", "Carli", 3475591)
        self.c.inserisci("Ubaldo", "Ubaldi", 3475511)

        time.sleep(2)
        print(self.c)

        time.sleep(5)
        print(self.c)

        items_produced = 0
        while items_produced < 10:

            self.c.suggerisci("Ubaldo_"+str(items_produced), "Ubaldi")

            items_produced +=1
        time.sleep(2)
        print("==========> Produttore: Cerca Ubaldo Ubaldi")
        if(self.c.cerca("Ubaldo", "Ubaldi") == None):
            print("==========> Produttore: Nome non trovato")
        else:
            print("==========> Produttore: TROVATO Ubaldo Ubaldi")
            self.c.cancella("Ubaldo", "Ubaldi")

        time.sleep(2)
        print(self.c)
