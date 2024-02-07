from subprocess import run
import os
import argparse


class Args:
    def __init__(self, 
                 name_A, in_fasta_A, in_db_A, 
                 name_B, in_fasta_B, in_db_B,
                 type, out_dir, n_threads):

        self.name_A = name_A
        self.in_fasta_A = in_fasta_A
        self.in_db_A = in_db_A

        self.name_B = name_B
        self.in_fasta_B = in_fasta_B
        self.in_db_B = in_db_B

        self.type = type
        self.out_dir = out_dir
        self.n_threads = n_threads

        self.check()

    def check(self):
        fasta_extension_A = self.in_fasta_A.split(".")[-1]
        if fasta_extension_A not in ["fasta", "fa"]:
            raise ValueError(f"Input fasta file must fasta file.")
        
        fasta_extension_B = self.in_fasta_B.split(".")[-1]
        if fasta_extension_B not in ["fasta", "fa"]:
            raise ValueError(f"Input fasta file must fasta file.")
   
        if not os.path.exists(self.in_db_A + ".nhr"):
            raise ValueError(f"Input blast database does not exist.")

        if not os.path.exists(self.in_db_B + ".nhr"):
            raise ValueError(f"Input blast database does not exist.")

        if self.type not in ["nucl", "prot"]:
            raise ValueError(f"Type must be nucl or prot.")


def get_args():
    parser = argparse.ArgumentParser(
        description="Calculate nucleotide diversity based on Akama et al. 2014"
    )
    parser.add_argument("--name_A", type=str, required=True,
                        help="name of species A")
    parser.add_argument("--in_fasta_A", type=str, required=True, 
                        help="path to the fasta files for species A")
    parser.add_argument("--in_db_A", type=str, required=True,
                        help="path to the blast database for species A")
    parser.add_argument("--name_B", type=str, required=True,
                        help="name of species B")
    parser.add_argument("--in_fasta_B", type=str, required=True,
                        help="path to the fasta files for species B")
    parser.add_argument("--in_db_B", type=str, required=True,
                        help="path to the blast database for species B")
    parser.add_argument("--out_dir", type=str, required=True,
                        help="path to the output directory")
    parser.add_argument("--type", type=str, required=True,
                        help="comparison level (nucleotide or amino acid)")
    parser.add_argument("--n_threads", type=int, default=1,
                        help="number of threads for blast")
    args = parser.parse_args()

    return Args(name_A=args.name_A,
                in_fasta_A=args.in_fasta_A,
                in_db_A=args.in_db_A,
                name_B=args.name_B,
                in_fasta_B=args.in_fasta_B,
                in_db_B=args.in_db_B,
                type=args.type,
                out_dir=args.out_dir,
                n_threads=args.n_threads)


def tblastx(in_fasta: str, in_db: str, out: str, n_threads: int) -> None:
    """
    Run tblastx.
    in_fasta: str
    in_db: str
    """
    with open(out, "w") as f:
        _ = run(["tblastx",
                 "-query", in_fasta,
                 "-db", in_db,
                 "-out", out,
                 "-num_threads", f"{n_threads}",
                 "-outfmt", "6",
                 "-evalue", "1e-5",
                 "-max_target_seqs", "1"],
                 text=True, stdout=f)
    return None


def blastn(in_fasta: str, in_db: str, out: str, n_threads: int) -> None:
    """
    Run blastn.
    in_fasta: str
    in_db: str
    """
    with open(out, "w") as f:
        _ = run(["blastn", 
                 "-query", in_fasta,
                 "-db", in_db,
                 "-out", out,
                 "-num_threads", f"{n_threads}",
                 "-outfmt", "6",
                 "-evalue", "1e-5",
                 "-max_target_seqs", "1"],
                 text=True, stdout=f)
    return None


def main():
    args = get_args()

    print(f"Running reciprocal blast for {args.name_A} and {args.name_B} at {args.type} level.")

    if args.type == "nucl":
        blast = blastn
    elif args.type == "prot":
        blast = tblastx

    print(f"Running blast for {args.in_fasta_A} vs {args.in_db_B}")
    out_ab_file = os.path.join(args.out_dir,
                               f"{args.name_A}_vs_{args.name_B}_{args.type}.txt")
    
    blast(in_fasta=args.in_fasta_A,
          in_db=args.in_db_B,
          out=out_ab_file,
          n_threads=args.n_threads)

    print(f"Running blast for {args.in_fasta_B} vs {args.in_db_A}")
    out_ba_file = os.path.join(args.out_dir,
                               f"{args.name_B}_vs_{args.name_A}_{args.type}.txt")
    blast(in_fasta=args.in_fasta_B,
          in_db=args.in_db_A,
          out=out_ba_file,
          n_threads=args.n_threads)

    print('Done!')


if __name__ == '__main__':
    main()