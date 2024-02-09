#%%
import numpy as np
import pandas as pd
import argparse
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_ab', type=str, required=True,
                        help='Path to blast result file of A against B')
    parser.add_argument('--path_ba', type=str, required=True,
                        help='Path to blast result file of B against A')
    parser.add_argument('--name_A', type=str, required=True,
                        help='Species name of A')
    parser.add_argument('--name_B', type=str, required=True,
                        help='Species name of B')
    parser.add_argument('--out_summary', type=str, required=True,
                        help='Path to output summary file')
    parser.add_argument('--out_rec_best_hit', type=str, required=True,
                        help='Path to output reciprocal best hit file')
    return parser.parse_args()


def read_blast_result_fmt6(path):
    """
    Read blast result in outfmt 6

    Args:
        path: path to blast result file

    Returns:
        df: dataframe of blast result
    """
    df = pd.read_csv(path, sep='\t', header=None)
    blast_fmt6 = ['qseqid', 'sseqid', 'pident', 
                  'length', 'mismatch', 'gapopen',
                  'qstart', 'qend',
                  'sstart', 'send',
                  'evalue', 'bitscore']
    df.columns = blast_fmt6
    return df


def rec_best_hit_df(df_ab, df_ba, name_A, name_B):
    """
    Make best reciprocal results dataframe

    Args:
        df_ab: dataframe of blast result from A aganist B, outfmt 6
        df_ba: dataframe of blast result from B aganist A, outfmt 6
        name_A: species name of A
        name_B: species name of B

    Returns:
        df_merge: merged dataframe of best reciprocal hits
    """
    # a -> b
    dic_ab = pd.Series(df_ab['sseqid'].values,
                   index=df_ab['qseqid'].values).to_dict()
    # b -> a
    dic_ba = pd.Series(df_ba['sseqid'].values,
                    index=df_ba['qseqid'].values).to_dict()

    # search a -> b -> a
    query_a_lis = []
    for query_a in dic_ab.keys():
        # a -> b
        hit_b = dic_ab[query_a]
        # a -> b -> a
        if query_a == dic_ba.get(hit_b, None):
            query_a_lis.append(query_a)

    # filtering
    df_ab = df_ab[df_ab['qseqid'].isin(query_a_lis)]
    df_ba = df_ba[df_ba['sseqid'].isin(query_a_lis)]

    # rename columns to merge
    df_ab.columns = [f"{col}_{name_A}_vs_{name_B}" for col in df_ab.columns]
    df_ba.columns = [f"{col}_{name_B}_vs_{name_A}" for col in df_ba.columns]

    df_merge = pd.merge(df_ab, df_ba,
                        left_on=f'qseqid_{name_A}_vs_{name_B}',
                        right_on=f'sseqid_{name_B}_vs_{name_A}',
                        how='inner')
    return df_merge


def main():
    args = get_args()

    df_ab = read_blast_result_fmt6(args.path_ab)
    df_ba = read_blast_result_fmt6(args.path_ba)

    # select the best identity score for each query
    # even in case of max_target_seqs is set to 1, 
    # multiple results in the same hit cds are included in blast result
    # make sure to select only one best hit for each query
    
    df_ab = df_ab.sort_values(['qseqid', 'evalue', 'length'],
                              ascending=[True, True, False])
    df_ab = df_ab.drop_duplicates(subset='qseqid', keep='first')

    df_ba = df_ba.sort_values(['qseqid', 'evalue', 'length'],
                              ascending=[True, True, False])
    df_ba = df_ba.drop_duplicates(subset='qseqid', keep='first')

    df_concat = pd.concat([df_ab, df_ba], axis=0)
    divergence1 = np.average(df_concat['pident'].values, 
                             weights=df_concat['length'].values).round(3)

    df_merge = rec_best_hit_df(df_ab, df_ba, args.name_A, args.name_B)
    d_ab = np.average(df_merge[f"pident_{args.name_A}_vs_{args.name_B}"],
                    weights=df_merge[f"length_{args.name_A}_vs_{args.name_B}"])
    d_ba = np.average(df_merge[f"pident_{args.name_B}_vs_{args.name_A}"],
                    weights=df_merge[f"length_{args.name_B}_vs_{args.name_A}"])
    divergence2 = np.mean([d_ab, d_ba]).round(3)

    # output result
    with open(args.out_summary, 'w') as f:
        print(f"Mean identity between {args.name_A} and {args.name_B}:", file=f)
        print(f"  - Average of all best hits: {divergence1}", file=f)
        print(f"  - Average of reciprocal best hits: {divergence2}", file=f)

    df_merge.to_csv(args.out_rec_best_hit, sep='\t', index=False)

    print('Done!')


if __name__ == '__main__':
    main()