import argparse
import data_viz
import gzip
import os
import time
import sys
sys.path.append("hash_tables_xifu0847")
from hash_functions import *
from hash_tables import *


def linear_search(key, L):
    hit = -1
    for i in range(len(L)):
        curr = L[i]
        if key == curr:
            return i
    return -1


def binary_search(key, D):
    lo = -1
    hi = len(D)
    while (hi - lo > 1):
        mid = (hi + lo) // 2

        if key == D[mid][0]:
            return D[mid][1]

        if (key < D[mid][0]):
            hi = mid
        else:
            lo = mid

    return -1


def get_parser():
    parser = argparse.ArgumentParser(description='Data visualization')

    parser.add_argument('--gene_reads', type=str, default='',
                        help='gene_reads file path')
    parser.add_argument('--sample_attributes', type=str, default='',
                        help='sample_attributes file path')
    parser.add_argument('--gene_name', type=str, default='',
                        help='gene name')
    parser.add_argument('--group_type', type=str, default='',
                        help='group similar genes, either SMTS or SMTSD')
    parser.add_argument('--output_file', type=str, default='Untitled.png',
                        help='output file as a picture')
    parser.add_argument('--verbose', type=bool, default=False,
                        help='if write benchmarking result to a txt file')
    parser.add_argument('--search_algorithm', type=str, default='binary',
                        help='Either binary or linear')

    args = parser.parse_args()
    return args


def main():
    # load args and check if they are valid
    args = get_parser()
    if args.verbose:
        main_start = time.time()

    if not os.path.exists(args.gene_reads):
        raise FileNotFoundError('gene_reads file not found')
    if not os.path.exists(args.sample_attributes):
        raise FileNotFoundError('sample_attributes file not found')
    if args.group_type not in ['SMTS', 'SMTSD']:
        raise ValueError('group_type should be either SMTS or SMTSD')
    if args.search_algorithm not in ['binary', 'linear']:
        raise ValueError('search_algorithm should be either binary or linear')

    sample_id_col_name = 'SAMPID'
    samples = []
    sample_info_header = None
    for l in open(args.sample_attributes):
        if sample_info_header is None:
            sample_info_header = l.rstrip().split('\t')
        else:
            samples.append(l.rstrip().split('\t'))

    group_col_idx = linear_search(args.group_type, sample_info_header)
    sample_id_col_idx = linear_search(sample_id_col_name, sample_info_header)

    groups = []
    sample_attributes_table = ChainedHash(100000, h_rolling)

    for sample in samples:
        sample_name = sample[sample_id_col_idx]
        curr_group = sample[group_col_idx]

        curr_group_idx = linear_search(curr_group, groups)

        if curr_group_idx == -1:
            curr_group_idx = len(groups)
            groups.append(curr_group)
            # members.append([])

        result = sample_attributes_table.search(curr_group)
        if result is None:
            sample_attributes_table.add(curr_group, [sample_name])
        else:
            result.append(sample_name)

    version = None
    dim = None
    data_header = None

    gene_name_col = 1
    times = 0
    group_counts = [[] for i in range(len(groups))]
    header_mapping_table = ChainedHash(20000, h_rolling)

    if args.verbose:
        hash_and_search_start = time.time()
    for l in gzip.open(args.gene_reads, 'rt'):
        if version is None:
            version = l
            continue

        if dim is None:
            dim = [int(x) for x in l.rstrip().split()]
            continue

        if data_header is None:
            i = 0
            for field in l.rstrip().split('\t'):
                header_mapping_table.add(field, i)
                i += 1
            data_header = 'Done'

        A = l.rstrip().split('\t')

        if A[gene_name_col] == args.gene_name:
            for group_idx in range(len(groups)):
                member_list = sample_attributes_table.search(groups[group_idx])
                for member in member_list:
                    index = header_mapping_table.search(member)

                    if index is not None:
                        group_counts[group_idx].append(int(A[index]))
            break
    if args.verbose:
        hash_and_search_end = time.time()
        print('hash and search time spent: {}'.format(
            hash_and_search_end - hash_and_search_start))
    data_viz.boxplot(group_counts, args.output_file, groups,
                     args.group_type, 'value', args.gene_name)

    if args.verbose:
        main_end = time.time()
        print('Main func time spent: {} sec'.format(main_end - main_start))


if __name__ == '__main__':
    main()
