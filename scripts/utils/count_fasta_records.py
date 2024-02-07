from Bio import SeqIO
import argparse
import sys


def get_args():
    parser = argparse.ArgumentParser(
        description="Count the number of nucleotide in each record in a fasta file.")
    parser.add_argument("--fasta", type=str, required=True, 
                        help="path to the fasta file")
    return parser.parse_args()


def main():
    args = get_args()

    handle = args.fasta if args.fasta != '-' else sys.stdin

    for record in SeqIO.parse(handle, "fasta"):
        print(f"{record.id}\t{len(record.seq)}")


if __name__ == '__main__':
    main()