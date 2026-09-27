import argparse
import time
import string
import matplotlib.pyplot as plt

def process_file(filename):
    start_time = time.time()

    count_dict = {char : 0 for char in string.ascii_lowercase}      # prende da un elenco di tutte le lettere minuscole

    with open(filename, "r", encoding="utf-8") as file:
        if args.stats:
            for line in file:
                for char in line.lower():       # non mi interessa maiuscolo/minuscolo
                    try:
                        count_dict[char] += 1
                    except KeyError:
                        pass

    # Normalisation
    tot_letters = sum(count_dict.values())
    for char in count_dict:
        count_dict[char] /= tot_letters
    
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    return count_dict


def generate_histogram(count_dict):
    plt.bar(count_dict.keys(), count_dict.values())
    plt.xlabel('Letters')
    plt.ylabel('Relative Frequency')
    plt.title('Letter Frequency Histogram')
    plt.show()


def calculate_statistics(filename):

    dict_words = {}

    with open(filename, "r", encoding="utf-8") as file:
            if args.stats:
                num_lines = 0
                num_words = 0
                num_characters = 0
                for line in file:
                    num_lines += 1
                    parole = line.split()        # splitto la riga in parole

                    num_words += len(parole)
                    num_characters += len(line)


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
        type = bool,
        help = 'If True, an histogram of the letter frequencies will be generated'
    )
    parser.add_argument(
        '-s','--stats',
        type = bool,
        help = 'If True, the program will print the number of letters, words and lines of the input file',
    )
    parser.add_argument(
            '--histw',
            type = bool,
            help = 'If True, an histogram of the words frequencies will be generated. Requires --stats to be True as well.'
        )
    
    args = parser.parse_args()
    if args.histw and not args.stats:
        parser.error("L'opzione --histw richiede che sia attiva anche l'opzione --stats.")

    count_dict = process_file(args.filepath)

    if args.histl:
        generate_histogram(count_dict)

    if args.stats:
        calculate_statistics(args.filepath)