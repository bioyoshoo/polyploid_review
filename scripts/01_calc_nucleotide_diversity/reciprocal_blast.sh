#!/bin/bash


DATA_DIR="../../data"
GE_DIR="${DATA_DIR}/genome"

for type in "nucl" "prot"
do
    # Reciprocal blast at protein level
    python reciprocal_blast.py --name_A "camara" \
                               --name_B "crivularis" \
                               --in_fasta_A "${GE_DIR}/camara/camara_genome.cds.fa" \
                               --in_db_A "${GE_DIR}/camara/db/camara.cds.db" \
                               --in_fasta_B "${GE_DIR}/crivularis/crivularis_genome.cds.fa" \
                               --in_db_B "${GE_DIR}/crivularis/db/crivularis.cds.db" \
                               --out_dir "${DATA_DIR}/blast_result" \
                               --type "$type" \
                               --n_threads 16
done