import argparse
import time
import string
import matplotlib.pyplot as plt

def process_file(filename):
    start_time = time.time()

    letters_dict = {char : 0 for char in string.ascii_lowercase}      # prende da un elenco di tutte le lettere minuscole

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            for char in line.lower():       # non mi interessa maiuscolo/minuscolo
                try:
                    letters_dict[char] += 1
                except KeyError:
                    pass

    # Normalisation
    tot_letters = sum(letters_dict.values())
    for char in letters_dict:
        letters_dict[char] /= tot_letters
    
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    return letters_dict

# Genera e Salva in .png un istogramma di frequenze relative
def generate_histogram(dictionary, nome_cose_contate, xticks=True, xlog=False, ylog=False):
    plt.bar(dictionary.keys(), dictionary.values(), log=xlog)
    plt.ylim(min(dictionary.values()) * 0.5, max(dictionary.values()) * 1.1)     # Imposta il limite superiore dell'asse y leggermente sopra il massimo valore
    if xlog:
        plt.xscale("log")
    plt.xlabel(nome_cose_contate)
    plt.ylabel('Relative Frequency')
    plt.title(f'{nome_cose_contate} Frequency Histogram')

    if not xticks:
        plt.xticks([])

    plt.savefig(f"{nome_cose_contate}_histogram.png")
    plt.close()

def calculate_statistics(filename):

    words_dict = {}

    with open(filename, "r", encoding="utf-8") as file:
        num_lines = 0
        num_words = 0
        num_characters = 0

        for line in file:
            num_lines += 1
            clean_line = line.lower().translate(str.maketrans("", "", string.punctuation))      # rimuovo la punteggiatura e metto in minuscolo
            parole = clean_line.split()        # splitto la riga in parole

            for parola in parole:
                if parola in words_dict:
                    words_dict[parola] += 1
                else:
                    words_dict[parola] = 1
                   
                num_words += len(parole)
                num_characters += len(line)

    print(f"Number of lines: {num_lines}")
    print(f"Number of words: {num_words}")
    print(f"Number of characters: {num_characters}")
    # Ordino il dizionario delle parole in base alla frequenza
    words_dict = dict(
        sorted(words_dict.items(), key=lambda item: item[1], reverse=True)
    )
    if args.histw:
        generate_histogram(words_dict, "Words", xticks=False, xlog=True, ylog=True)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "This program counts the relative frequencies of letters and words and some others statistics in a .txt file."
    )
    parser.add_argument(
        '-i', '--input',
        type = str,
        help = 'Path to the input .txt file',
        dest = 'filepath',
    )
    parser.add_argument(
        '--histl',
        action = 'store_true',
        help = 'Generate an histogram of the letters frequencies'
    )
    parser.add_argument(
        '-s','--stats',
        action = 'store_true',
        help = 'Print the number of letters, words and lines of the input file',
    )
    parser.add_argument(
        '--histw',
        action = 'store_true',
        help = 'Generate an histogram of the words frequencies. Requires --stats to be active.'
    )
    
    args = parser.parse_args()

    # CONTROLLI LOGICI
    if args.filepath is None:
        parser.error("Nessun percorso di file fornito.")
    if args.histw and not args.stats:
        parser.error("L'opzione --histw richiede che sia attiva anche l'opzione --stats.")

    letters_dict = process_file(args.filepath)

    if args.histl:
        generate_histogram(letters_dict, "Letters")

    if args.stats:
        calculate_statistics(args.filepath)