# Polyploid review

## Calculate nucleotide divergence between C.amara and C.rivlaris

#### Data
* C.amara and C.rivularis genome sequence (FASTA)
* C.amara and C.rivularis genome annotation file (GFF)
    * These data shared from Sun. See [his github page](https://github.com/jsun/suppl/tree/master/10.3389/fgene.2020.567262)
    * See https://www.frontiersin.org/journals/genetics/articles/10.3389/fgene.2020.567262/full for the assembly method.

#### Strategy
1. Extract CDS sequence from FASTA and GFF files using gffread and make CDS only multi fasta file.

2. Make blast database and execute blastn (nucleotide level) of CDS multi fasta file aganist blast database.
    * blast search for both direction
        * C.amara CDS fasta -> C.rivularis CDS blast database
        * C.rivularis CDS fasta -> C.amara CDS blast database
    * **consider only best hit**

3. Calculate sequence identity (sequence divergence) based on blast output (both nucleotide and amino acido sequence level comparison can be calculated.)
    1. average of all blast best hit of both direction blast search (based on [Akama et al., 2014](https://academic.oup.com/nar/article/42/6/e46/2437554))

    2. average of identity scores of only **reciprocal blast hit**.