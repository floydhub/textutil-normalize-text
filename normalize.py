from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import csv
import re

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    return string.strip().lower()

def str2bool(val):
    """
    Helper method to convert string to bool
    """
    if val is None:
        return False
    val = val.lower().strip()
    if val in ['true', 't', 'yes', 'y', '1', 'on']:
        return True
    elif val in ['false', 'f', 'no', 'n', '0', 'off']:
        return False

def main():
    """
    Normalizes the contents of a text file using a simple naive normalization scheme.
    Designed for English
    """

    # Parse command line args
    parser = argparse.ArgumentParser(description='Normalize text in the given columns')

    parser.add_argument(
        '-i', '--input', required=True,
        help='Path to input file')
    parser.add_argument(
        '-c', '--cols', required=True, type=str, default=0, 
        help='Comma separated list of columns indices to normalize')
    parser.add_argument(
        '-d', '--delimiter', required=True, default='\t', 
        help='Column delimiter between row and label')
    parser.add_argument(
        '-header', '--hasheader', required=False, type=str2bool,
        default='False', help='File has header row?')
    parser.add_argument('-o', '--output', required=True, help='Path to output file')

    args = parser.parse_args()
    # Unescape the delimiter
    args.delimiter = args.delimiter.decode('string_escape')
    # Parse cols into list of ints
    args.cols = [int(x) for x in args.cols.split(',')]

    # Convert args to dict
    vargs = vars(args)

    print("\nArguments:")
    for arg in vargs:
        print("{}={}".format(arg, getattr(args, arg)))

    # Read the input file
    with open(args.input, 'r') as inputfile:
        with open(args.output, 'w') as outputfile:
            
            reader = csv.reader(inputfile, delimiter=args.delimiter)
            writer = csv.writer(outputfile, delimiter=args.delimiter)

            # If has header, write it unprocessed
            if args.hasheader:
                headers = next(reader, None)
                if headers:
                    writer.writerow(headers)

            print("\nProcessing input")
            for row in reader:
                row = [clean_str(col) if idx in args.cols else col for idx, col in enumerate(row)]
                writer.writerow(row)

    print("\nDone. Bye!")

if __name__ == '__main__':
    main()