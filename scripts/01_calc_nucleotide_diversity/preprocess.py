from subprocess import run, PIPE
import os
import argparse


class Args:
    def __init__(self, in_fasta, in_gff, out_db):
        self.in_fasta = in_fasta
        self.in_gff = in_gff
        self.out_db = out_db
        self.check()
    
    def check(self):
        fasta_extension = self.in_fasta.split(".")[-1]
        if fasta_extension not in ["fasta", "fa"]:
            raise ValueError(f"Input fasta file must fasta file.")

        gff_extension = self.in_gff.split(".")[-1]
        if gff_extension != "gff":
            raise ValueError(f"Input gff file must be gff file.")
        
        os.makedirs(os.path.dirname(self.out_db), exist_ok=True)


def get_args():
    parser = argparse.ArgumentParser(
        description="Extract the CDS sequences from a fasta file using a gff file.")
    parser.add_argument("--in_fasta", type=str, required=True, 
                        help="path to the fasta files")
    parser.add_argument("--in_gff", type=str, required=True, 
                        help="path to the gff files")
    parser.add_argument("--out_db", type=str, required=True,
                        help="path and basic name for the blast database.")
    args = parser.parse_args()

    return Args(in_fasta=args.in_fasta, 
                in_gff=args.in_gff,
                out_db=args.out_db)


def extract_cds_seq(in_fasta: str, in_gff: str, out_fasta: str) -> None:
    """
    Extract the CDS sequences from a fasta file using a gff file.
    in_fasta: str
    in_gff: str
    out_fasta: str
    """
    with open(out_fasta, "w") as f:
        _ = run(["gffread", in_gff,
                 "-g", in_fasta,
                 "-x", out_fasta], 
                 text=True, stdout=f)
    return None


def make_blastdb(in_fasta: str, out_db: str) -> None:
    """
    Make a blast database from a fasta file.
    in_fasta: str
    dbtype: str
    """
    if not os.path.exists(out_db + ".nhr"):
        _ = run(["makeblastdb",
                 "-in", in_fasta,
                 "-dbtype", "nucl",
                 "-out", out_db,
                 "-hash_index", "-parse_seqids"])
    else:
        print(f"{out_db} already exists. Skipping makeblastdb.")


def main():
    args = get_args()

    in_fasta = args.in_fasta
    cds_fasta = in_fasta.replace(".fa", ".cds.fa")

    extract_cds_seq(in_fasta=in_fasta,
                    in_gff=args.in_gff,
                    out_fasta=cds_fasta)

    make_blastdb(in_fasta=cds_fasta, 
                 out_db=args.out_db)

    print('Done!')

if __name__ == '__main__':
    main()