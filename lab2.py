# Buongiorno Professore,
# purtroppo sto affrontando alcune serie difficoltà familiari ed economiche che, al momento,
# mi impediscono di frequentare le lezioni con regolarità e di rispettare le scadenze previste.
# svolgerò comunque tutti gli esercizi.
# La ringrazio di cuore se terrà in considerazione, anche solo in parte, il lavoro svolto

import csv
def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    #scelgo di mettere un dizionario di lista di tuple
    album={}
    try:
       with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader=csv.reader(file)
        #salto intestazione
        next(reader)
        for line in reader:
           codice=line[0]
           titolo=line[1]
           autore=line[2]
           mese=int(line[3])
           anno=int(line[4])
           if anno not in album:
            album[anno]=[]
           foto=(codice,titolo,autore,mese)
           album[anno].append(foto)
        return album
    except FileNotFoundError:
         return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    try:
        # 1. Verifico mese tra 1 e 12
        if not 1 <= int(mese) <= 12:
            return None
        mese = int(mese)
        # 2. verifico codice non già nell'album
        for lista_foto in album.values():
            for foto_esistente in lista_foto:
                if foto_esistente[0] == codice:
                    return None
        # 3. creo tupla
        foto = (codice, titolo, autore, mese)
        # 4. aggiungo foto in fondo a csv
        with open(file_path, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([codice, titolo, autore, mese, anno])
        # 5. creo anno se non presente
        if anno not in album:
            album[anno] = []
        # 6. aggiorno struttura dati
        album[anno].append(foto)
        # 7. restituisco foto
        return foto
    except (OSError, ValueError, csv.Error):
        print("Errore durante l'aggiunta della foto.")
        return None

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for lista_foto in album.values():
        for foto_esistente in lista_foto:
            if foto_esistente[0] == codice:
                return(foto_esistente)
    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    #creo lista di titoli di foto facendo scorrere tutte le liste di un determinato anno
    if anno in album:
     listaordinata=[]
     for lista_foto in album[anno]:
             listaordinata.append(lista_foto[1])
     listaordinata.sort()
     return listaordinata
    else:
      return None


def main():
    album = {}
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()