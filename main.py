# Assegnamento 2  aa 2021-22 622AA modulo programmazione 9 crediti
# Gruppo:
# Martina Leocata 
# Elena Scaglione 
from rubrica import Rubrica
from Produttore import Produttore
from Consumatore import Consumatore
import tkinter as tk
import logging


def scriviMessaggio(testo):
    """Fornisce feedback sullo stato del programma all'utente tramite una label"""
    global label
    label.destroy()  # pulisce il campo di testo, eliminando un'eventuale label precedente
    label = tk.Label(mainFrame, text=testo)
    label.grid(row=2, column=0, columnspan=2, padx=100, pady=10)
    root.update()  # aggiorna l'interfaccia, senza aspettare la conclusione dei thread


def avvia_SimpleTest():
    """Avvia un thread Produttore e un thread Consumatore"""

    logging.info('User ha avviato il simple test')
    scriviMessaggio('Simple Test avviato')

    rubrica = Rubrica()
    produttore = Produttore(rubrica, 1)
    consumatore = Consumatore(rubrica, 1)
    produttore.start()
    consumatore.start()
    produttore.join()
    consumatore.join()

    scriviMessaggio('Simple Test concluso')


def avvia_TestMultithreading():
    """Avvia n thread Produttore e Consumatore secondo l'input dell'utente"""
    listaThreads_produttori = list()
    listaThreads_consumatori = list()
    num_threads = entry.get()  # otteniamo l'user input

    # proteggiamo il programma da interruzioni con un try-except, nel caso l'utente non inserisca un numero
    try:
        num_threads = int(entry.get())
    except ValueError:
        logging.error('User ha inserito un valore non corretto')
        scriviMessaggio('Per favore inserire un numero')
    else:
        if num_threads > 1:
            logging.info("User ha inserito un valore numerico > 1. Avvio il test multithreading")
            scriviMessaggio(f"Test Multithreading avviato. Numero di thread avviati {int(entry.get()) * 2}")

            for n in range(num_threads):
                rubrica = Rubrica()
                produttore = Produttore(rubrica, n + 1)
                consumatore = Consumatore(rubrica, n + 1)
                produttore.start()
                consumatore.start()
                listaThreads_produttori.append(produttore)
                listaThreads_consumatori.append(consumatore)
            for thread_prod in listaThreads_produttori:
                thread_prod.join()
            for thread_cons in listaThreads_consumatori:
                thread_cons.join()
            scriviMessaggio(f'Test Multithreading concluso. Numero di thread avviati {int(entry.get()) * 2}')

        elif num_threads == 1:
            avvia_SimpleTest()
        else:
            logging.info("User ha inserito un valore negativo")
            scriviMessaggio('Per favore inserire un numero > 0')


def ottieni_NumeroThreads(event):
    """avvia il test appropriato in base al numero di thread inserito dall'utente"""

    logging.info("User ha inserito un valore e premuto <invio>")

    # proteggiamo il programma da interruzioni con un try-except, nel caso l'utente non inserisca un numero
    try:
        n_threads = int(entry.get())
    except ValueError:
        logging.error("User ha inserito un valore non numerico")
        scriviMessaggio('Per favore inserire un numero')
    else:
        logging.info("User ha inserito un valore numerico")
        if n_threads == 1:
            avvia_SimpleTest()
        elif n_threads > 1:
            avvia_TestMultithreading()
        else:
            logging.error('User ha inserito un numero negativo')
            scriviMessaggio('Per favore inserire un numero > 0')


def inserisciNumeroThreads(event):
    """gestisce l'User input"""
    logging.info("User ha posto il focus sull'entry")
    if entry.get() == default_entry:
        entry.delete(0, tk.END)
    entry.config(fg='black')
    entry.bind('<Return>', ottieni_NumeroThreads)


if __name__ == '__main__':
    # configurazione del logger
    log_format = '%(levelname)s %(asctime)s %(threadName)s - %(message)s'
    logging.basicConfig(filename='Log_file.log', filemode='w', format=log_format, level=logging.DEBUG)
    logger = logging.getLogger()
    file_handler = logging.FileHandler('Log_file.log')
    logger.addHandler(file_handler)
    logging.info('Mi preparo alla creazione del root')

    # configurazione dell'interfaccia grafica
    root = tk.Tk()
    root.geometry('650x150')
    mainFrame = tk.Frame()
    root.title('Rubrica')
    mainFrame.grid_columnconfigure(0, weight=1, minsize=125)
    mainFrame.grid_columnconfigure(1, weight=1, minsize=125)

    # configurazione degli elementi dell'interfaccia
    label = tk.Label(mainFrame, text='')

    entry = tk.Entry(mainFrame, width=200)
    default_entry = 'Inserisci numero di threads o avvia il simple test'
    entry.insert(0, default_entry)
    entry.config(fg='grey')
    entry.configure(justify=tk.CENTER)
    entry.bind('<Button-1>', inserisciNumeroThreads)

    bottone1 = tk.Button(mainFrame, text='Simple Test', command=avvia_SimpleTest, width=50, padx=5, pady=15)
    bottone2 = tk.Button(mainFrame, text='Test Multithreading', command=avvia_TestMultithreading, width=50, padx=5,
                         pady=15)

    # inseriamo gli elementi nell'interfaccia, specificando la posizione
    entry.grid(row=0, column=0, columnspan=2, padx=150, pady=10)
    bottone1.grid(row=1, column=0)
    bottone2.grid(row=1, column=1)
    mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()