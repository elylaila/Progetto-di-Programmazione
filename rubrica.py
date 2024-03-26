# Assegnamento 2 aa 2021-22 622AA modulo programmazione 9 crediti
# Gruppo:
# Martina Leocata 
# Elena Scaglione 
from threading import Condition
from threading import current_thread
from queue import Queue
import logging
from random import randint


class Rubrica:
    """ Costruttore: crea una rubrica vuota rappresentata come
        dizionario di contatti vuoto """

    def __init__(self):
        """ crea una nuova rubrica vuota """
        self.rub = {}
        self.condition = Condition()
        self.queue = Queue(maxsize=3)

    def __str__(self):
        """ Serializza una rubrica attraverso una stringa
        con opportuna codifica (a scelta dello studente) """

        # identifichiamo la classe di appartenenza dell'oggetto
        riga0 = f'Object class: <{self.__class__.__name__}>\n'

        # stampiamo la lista contatti in ordine alfabetico e il numero di contatti totale
        riga1 = 'Lista contatti:\n'
        riga2 = self.ordina() + '\n'
        riga3 = f'Numero contatti totale: {len(tuple((self.rub.keys())))}\n'
        stringa = riga0 + riga1 + riga2 + riga3
        return stringa

    def __eq__(self, r):
        """ stabilisce se due rubriche contengono
        esattamente le stesse chiavi con gli stessi dati"""
        if isinstance(r, Rubrica):  # controlliamo che l'oggetto 'r' appartenga alla classe 'Rubrica'
            return self.rub == r.get_dict()  # confrontiamo i dizionari associati all'oggetto rubrica
        else:
            logging.info(f'Le rubriche non contengono gli stessi contatti')
            return False

    def __add__(self, r):
        """crea una nuova rubrica unendone due (elimina i duplicati)
        e la restituisce come risultato --
        se ci sono contatti con la stessa chiave nelle due rubriche
        ne riporta uno solo """
        self.condition.acquire()
        r_keys = r.get_keys()
        r_dict = r.get_dict()

        # creiamo una copia del dizionario di self come variabile temporanea di tipo dizionario,
        # dove inserire i contatti di 'r' non presenti in self.rub
        tmp = self.rub.copy()

        for nominativo in r_keys:
            if self.rub.get(nominativo) is None:
                tmp[nominativo] = r_dict[nominativo]

        # creiamo un nuovo oggetto rubrica e inseriamo i dati contenuti nel dizionario tmp
        nuova_rubrica = Rubrica()

        for nominativo, numero in tmp.items():
            nuova_rubrica.inserisci(nominativo[0], nominativo[1], numero)
        self.condition.notify_all()
        self.condition.release()
        return nuova_rubrica

    def get_keys(self):
        """ restituisce il nominativo dei contatti memorizzati in un oggetto Rubrica """
        return self.rub.keys()

    def get_dict(self):
        """ restituisce il dizionario associato a un oggetto rubrica """
        rub_dict = dict(self.rub)
        return rub_dict

    def load(self, nomefile):
        """ carica da file una rubrica eliminando il
        precedente contenuto di self """
        self.condition.acquire()
        # controlliamo che il dizionario associato alla rubrica sia vuoto
        # se non vuoto, cancelliamo il precedente contenuto
        if self.rub:
            self.rub = {}
        # controlliamo che l'apertura del file vada a buon fine
        try:
            rubrica = open(nomefile, 'r')
        except NameError:
            logging.error('Operazione di apertura del file non riuscita')
            return False
        else:
            for contatto in rubrica:
                contatto = contatto.rstrip()  # eliminiamo eventuali spazi alla destra della stringa
                contatto = contatto.split(':')  # splittiamo la stringa nel momento in cui troviamo il carattere ':'
                nome = contatto[0]
                cognome = contatto[1]
                numero = contatto[-1]
                self.inserisci(nome, cognome, numero)
            logging.info(f'Operazione riuscita. {nomefile} caricato correttamente')
            rubrica.close()
            return True
        finally:
            self.condition.notify_all()
            self.condition.release()

    def inserisci(self, nome, cognome, dati):
        """ inserisce un nuovo contatto con chiave (nome,cognome) restituisce "True" se l'inserimento è andato a buon fine e "False" altrimenti (es chiave replicata) -- case insensitive """

        # controllo che il valore inserito sia una stringa
        logging.info(f'Inserisco elemento in rubrica: {nome} {cognome}')
        if isinstance(nome, str) and isinstance(cognome, str):
            nome = nome.lower()
            cognome = cognome.lower()
            dati = int(dati)

            # controllo che i dati inseriti non siano già associati ad un numero
            self.condition.acquire()
            if self.rub.get((nome, cognome)) is None:
                self.rub[(nome, cognome)] = dati
                self.condition.notify_all()
                self.condition.release()
                return True
            else:
                logging.warning(f'Esiste già un numero associato a {nome} {cognome}')
                self.condition.notify_all()
                self.condition.release()
                return False
        else:
            logging.error('Operazione di inserimento dati non riuscita.')
            return False

    def modifica(self, nome, cognome, newdati):
        """ modifica i dati relativi al contatto con chiave (nome,cognome)
        sostituendole con "newdati" -- restituisce "True" se la modifica
        è stata effettuata e "False" altrimenti (es: la chiave non è presente )"""

        # controllo che il valore inserito sia una stringa
        logging.info(f'Modifico elemento "{nome} {cognome}" con nuovi dati {newdati}')
        self.condition.acquire()
        if isinstance(nome, str) and isinstance(cognome, str):
            nome = nome.lower()
            cognome = cognome.lower()
            # controllo che i dati inseriti siano associati ad un numero
            if self.rub.get((nome, cognome)) is None:
                logging.info('Non esiste un numero associato al contatto inserito')
                self.condition.notify_all()
                self.condition.release()
                return False
            else:
                self.rub[(nome, cognome)] = newdati
                self.condition.notify_all()
                self.condition.release()
                return True

    def cancella(self, nome, cognome):
        """ il contatto con chiave (nome,cognome) esiste lo elimina
        insieme ai dati relativi e restituisce True -- altrimenti
        restituisce False """

        # controllo che i dati inseriti siano associati ad un numero
        logging.info(f'Cancello elemento da rubrica: {nome} {cognome}')
        self.condition.acquire()
        if self.rub.get((nome.lower(), cognome.lower())) is not None:
            del self.rub[(nome.lower(), cognome.lower())]
            self.condition.notify_all()
            self.condition.release()
            return True
        else:
            self.condition.notify_all()
            self.condition.release()
            return False

    def cerca(self, nome, cognome):
        """ restitusce i dati del contatto se la chiave e' presente
        nella rubrica e "None" altrimenti -- case insensitive """
        # modifichiamo la funzione cerca restituendo, oltre alla corrspondenza esatta, anche risultati correlati

        logging.info(f'Cerco nominativo: {nome} {cognome}')
        nome = nome.lower()
        cognome = cognome.lower()
        risultato_esatto = self.rub.get((nome, cognome))
        if risultato_esatto != None:
            return risultato_esatto
        else:
            for key in self.rub:
                if nome in key or cognome in key:
                    logging.info('Chiave non presente in rubrica, ma trovati contatti simili')
                    return self.rub.get(key)
                else:
                    logging.info('Contatto non presente in rubrica')
                    return None

    def store(self, nomefile):
        """ salva su file il contenuto della rubrica secondo
        un opportuno formato (a scelta dello studente)"""
        # il formato da me scelto
        # prevede un contatto per linea
        # nome:cognome:telefono\n
        with open(nomefile, 'w') as rubrica:
            for nome, numero in self.rub.items():
                rubrica.write(f'{nome[0]}:{nome[1]}:{numero}\n')
                logging.info(f'Rubrica salvata sul file {nomefile}')

    def ordina(self, crescente=True):
        """ serializza su stringa il contenuto della rubrica come in
            Nannipieri Felice 32255599\n
            Neri Paolo 347555776\n
            Rossi Mario 3478999\n
            Rossi Mario Romualdo 3475599\n
            Tazzini Tazzetti Gianna 33368999\n
            le chiavi ordinate lessicograficamente per Cognome -- Nome
            in modo crescente (True) o decrescente (False)
            Fra nome, cognome e telefono seve essere presente ESATTAMENTE uno spazio
            Restituisce la stringa prodotta """

        logging.info('Metto in ordine')
        lista_ordinata = list()
        for nome, numero in self.rub.items():
            cognome_nome = (nome[1], nome[0])
            lista_ordinata.append((cognome_nome, numero))
            # restituisce lista in ordine in ordine alfabetico (A-Z)
            if crescente:
                lista_ordinata = sorted(lista_ordinata)
            # restituisce lista in ordine in ordine alfabetico inverso (Z-A)
            else:
                lista_ordinata = sorted(lista_ordinata, reverse=True)
        stringa = ''
        for i in lista_ordinata:
            stringa += str(i[0][0]).title() + ' ' + str(i[0][1]).title() + ' ' + str(i[1]) + "\n"
        return stringa

    def suggerisci(self, nome, cognome):
        """Il metodo suggerisci viene invocato da un thread per
        effettuare un suggerimento di un contatto nella rubrica.
        Prende come parametro il nome ed il cognome del contatto e
        lo inserisce in una coda (di lunghezza massima 3).
        Non si puo' inserire un elemento nella coda se la coda e' piena.
        """
        logging.info(f'Avvio il thread {current_thread().getName()} per i suggerimenti')
        self.condition.acquire()
        while self.queue.full():
            self.condition.wait()
        nominativo = (nome + ' ' + cognome)
        self.queue.put(nominativo)
        self.condition.notify_all()
        self.condition.release()

    def suggerimento(self):
        """Il metodo suggerimento viene invocato da un thread per
        ottenere un suggerimento recuperato dalla rubrica.
        Il thread legge gli elementi presenti in una coda
        di lunghezza 3. Se la coda è vuota, attende l'inserimento di
        un elemento, altrimenti prende il primo elemento della
        coda e lo stampa."""
        logging.info(f'Avvio il thread {current_thread().getName()} che accoglie i suggerimenti')
        self.condition.acquire()
        while self.queue.empty():
            self.condition.wait()
        nominativo = self.queue.get()

        # inseriamo i contatti suggeriti dal Produttore, assegnando un numero casuale
        nominativo = nominativo.split()
        nome = nominativo[0]
        cognome = nominativo[1]
        numero = randint(1111111, 9999999)
        logging.info(f"inserisco {nome} {cognome}, numero {numero}")
        self.inserisci(nome, cognome, numero)

        self.queue.task_done()
        self.condition.notify_all()
        self.condition.release()