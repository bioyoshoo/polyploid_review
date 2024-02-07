#!/bin/bash


DATA_DIR="../../data/genome"


for species in "camara" "crivularis"
do  
    echo "Processing $species"

    fasta_bzip="${DATA_DIR}/${species}/${species}_genome.fa.bz2"
    gff_bzip="${DATA_DIR}/${species}/${species}_genome.modified.gff.bz2"

    in_fasta="${fasta_bzip%.bz2}"
    in_gff="${gff_bzip%.bz2}"
    out_db="$(dirname $in_fasta)/db/${species}.cds.db"

    # extract bzip2 compression
    bzip2 -cd $fasta_bzip > $in_fasta
    bzip2 -cd $gff_bzip > $in_gff

    # extract cds sequence from the fasta file and cds only gff file
    # make a blast database
    python preprocess.py --in_fasta $in_fasta --in_gff $in_gff --out_db $out_db

    # remove the uncompressed fasta and gff files
    rm $in_fasta
    rm $in_gff
done