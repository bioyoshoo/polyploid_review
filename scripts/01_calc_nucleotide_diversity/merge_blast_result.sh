#!/bin/bash


DATA_DIR="../../data/blast_result"

# nucleotide level comparison
python merge_blast_result.py --name_A "camara" \
                             --name_B "crivularis" \
                             --path_ab "${DATA_DIR}/camara_vs_crivularis_nucl.txt" \
                             --path_ba "${DATA_DIR}/crivularis_vs_camara_nucl.txt" \
                             --out_summary "${DATA_DIR}/divergence_camara_crivularis_nucl.txt" \
                             --out_rec_best_hit "${DATA_DIR}/reciprocal_best_hit_camara_crivularis_nucl.txt"