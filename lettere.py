import argparse
import time
import string
import matplotlib.pyplot as plt

def process_file(filename):
    start_time = time.time()

    count_dict = {char : 0 for char in string.ascii_lowercase}      # prende da un elenco di tutte le lettere minuscole

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

                for char in line.lower():       # non mi interessa maiuscolo/minuscolo
                    try:
                        count_dict[char] += 1
                    except KeyError:
                        pass
        else:
            for line in file:
                for char in line.lower():
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
    if args.stats:
        print(f"Number of lines: {num_lines}")
        print(f"Number of words: {num_words}")
        print(f"Number of characters: {num_characters}")
    return count_dict


def generate_histogram(count_dict):
    plt.bar(count_dict.keys(), count_dict.values())
    plt.xlabel('Letters')
    plt.ylabel('Relative Frequency')
    plt.title('Letter Frequency Histogram')
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "This program counts the relative frequencies of letters in a .txt file."
    )
    parser.add_argument(
        '-i', '--input',
        type = str,
        help = 'Path to the input .txt file',
        dest = 'filepath',
    )
    parser.add_argument(
        '--hist',
        type = bool,
        help = 'If True, an histogram of the letter frequencies will be generated',
    )
    parser.add_argument(
        '-s','--stats',
        type = bool,
        help = 'If True, the program will print the number of letters, words and lines of the input file',
    )
    args = parser.parse_args()
    count_dict = process_file(args.filepath)
    if args.hist:
        generate_histogram(count_dict)