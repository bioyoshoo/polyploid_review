# Polyploid review

## Calculate nucleotide divergence between C.amara and C.rivlaris

### Data
* C.amara and C.rivularis genome sequence (FASTA)
* C.amara and C.rivularis genome annotation file (GFF)
    * These data shared from Sun. See [his github page](https://github.com/jsun/suppl/tree/master/10.3389/fgene.2020.567262)
    * See https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2020.567262/full for the assembly method.

### Strategy
1. Preprocess
    * Extract CDS sequence from FASTA and GFF files using gffread and make CDS multi fasta file of each species.
    * Make blast database using CDS multi fasta file for each species.
        * See ```scripts/01_calc_nucleotide_diversity/preprocess.py(.sh)```

2. Blast search of CDS multi fasta file aganist blast CDS database.
    * blast search for both direction
        * C.amara CDS fasta -> C.rivularis CDS blast database
        * C.rivularis CDS fasta -> C.amara CDS blast database
    * **consider only best hit**
        * specify ```max_target_seqs = 1``` for blast option
    * both nucleotide and amino acido sequence level comparison can be calculated. (blastn or tblastx)
    * See ```scripts/01_calc_nucleotide_diversity/reciprocal_blast.py(.sh)``` for detail

3. Calculate sequence identity (sequence divergence) based on blast output
    * **Note!!**
        Even if you consider only best hit specifying ```max_target_seqs = 1```, multiple result of the same query are included in the blast output. This is because the different regions in one best hit pair of query and subject sequence are included in the final output.
        * So, only select the record of lowest evalue record for representing each query.
        
            ```
            df_ab = df_ab.sort_values(['qseqid', 'evalue', 'length'], ascending=[True, True, False])
            df_ab = df_ab.drop_duplicates(subset='qseqid', keep='first')
            ```
    * 2 types of identity calculation method
        * both methods are basically match length weighted mean of identity score.
        1. average of all blast best hit of both direction blast search (based on [Akama et al., 2014](https://academic.oup.com/nar/article/42/6/e46/2437554))
        2. average of identity scores of only **reciprocal blast hit**.

### Result
* Nucleotide level comparison
> Mean identity between camara and crivularis:
>  - Average of all best hits: 97.812 -> **divergence 2.188 %**
>  - Average of reciprocal best hits: 97.825 -> **divergence 2.175 %**