import argparse
import data_viz
import gzip
import os
import time


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
    '''
    main_start = time.time()
    data_file_name='GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz'
    sample_info_file_name='GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt'

    group_col_name = 'SMTS'
    sample_id_col_name = 'SAMPID'
    gene_name = 'ACTA2'
    '''
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
    members = []

    for row_idx in range(len(samples)):
        sample = samples[row_idx]
        sample_name = sample[sample_id_col_idx]
        curr_group = sample[group_col_idx]

        curr_group_idx = linear_search(curr_group, groups)

        if curr_group_idx == -1:
            curr_group_idx = len(groups)
            groups.append(curr_group)
            members.append([])

        members[curr_group_idx].append(sample_name)

    version = None
    dim = None
    data_header = None

    gene_name_col = 1

    group_counts = [[] for i in range(len(groups))]

    if args.verbose:
        search_start = time.time()
    for l in gzip.open(args.gene_reads, 'rt'):
        if version is None:
            version = l
            continue

        if dim is None:
            dim = [int(x) for x in l.rstrip().split()]
            continue

        if data_header is None:
            if args.search_algorithm == 'binary':
                data_header = []
                i = 0
                for field in l.rstrip().split('\t'):
                    data_header.append([field, i])
                    i += 1
                if args.verbose:
                    sort_start = time.time()
                data_header.sort(key=lambda tup: tup[0])
                if args.verbose:
                    sort_end = time.time()
                    print('Sorting time spent: {} sec'.format(
                        sort_end - sort_start))
                continue
            elif args.search_algorithm == 'linear':
                data_header = l.rstrip().split('\t')
                continue

        A = l.rstrip().split('\t')

        if A[gene_name_col] == args.gene_name:
            for group_idx in range(len(groups)):
                for member in members[group_idx]:
                    if args.search_algorithm == 'linear':
                        member_idx = linear_search(member, data_header)
                    elif args.search_algorithm == 'binary':
                        member_idx = binary_search(member, data_header)

                    if member_idx != -1:
                        group_counts[group_idx].append(int(A[member_idx]))
            break
    if args.verbose:
        search_end = time.time()
        if args.search_algorithm == 'binary':
            print('Searching time spent: {} sec'.format(
                search_end - search_start - (sort_end - sort_start)))
        elif args.search_algorithm == 'linear':
            print('Searching time spent: {} sec'.format(
                search_end - search_start))

    data_viz.boxplot(group_counts, args.output_file, groups,
                     args.group_type, 'value', args.gene_name)

    if args.verbose:
        main_end = time.time()
        print('Main func time spent: {} sec'.format(main_end - main_start))


if __name__ == '__main__':
    main()
