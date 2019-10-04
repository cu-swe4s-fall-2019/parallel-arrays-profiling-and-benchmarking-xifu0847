# parallel-arrays-profiling-and-benchmarking
Parallel Arrays, Profiling, and Benchmarking

Files:
- https://github.com/swe4s/lectures/blob/master/data_integration/gtex/GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz?raw=true
- https://storage.googleapis.com/gtex_analysis_v8/annotations/GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt

# Usage:

## General usage:
``shell
python plot_gtex.py --gene_reads=${GENE_READS_FILE} --sample_attributes=${SAMPLE_ATTRIBUTES_FILE}\
--gene_name=${GENE_NAME} --group_type=${GROUP_TYPE} --output_file=${FIGURE_NAME} --search_algorithm=${ALGORITHM} --verbose=${VERBOSE}
``

## Profiling usage:
``shell
python -m cProfile -s tottime plot_gtex.py --gene_reads=${GENE_READS_FILE} --sample_attributes=${SAMPLE_ATTRIBUTES_FILE}\
--gene_name=${GENE_NAME} --group_type=${GROUP_TYPE} --output_file=${FIGURE_NAME} --search_algorithm=${ALGORITHM} --verbose=${VERBOSE}\
> ${REPORT_NAME}
``

## Benchmarking usage:
``shell
python plot_gtex.py --gene_reads=${GENE_READS_FILE} --sample_attributes=${SAMPLE_ATTRIBUTES_FILE}\
--gene_name=${GENE_NAME} --group_type=${GROUP_TYPE} --output_file=${FIGURE_NAME} --search_algorithm=${ALGORITHM} --verbose=True > ${REPORT_NAME}
``

## Arguments:
GENE_READS_FILE: name of gene reads file. e.g. GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz\
SAMPLE_ATTRIBUTES_FILE: name of sample attributes file. e.g. GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt\
GENE_NAME: name of gene for searching. e.g. ACTA2\
GROUP_TYPE: either SMTS or SMTSD\
FIGURE_NAME: the name of result figure.\
ALGORITHM: either binary or linear.\
VERBOSE: True of False. Enable or disable benchmarking\
REPORT_NAME: the output report name.\

# Profiling summary:

## linear search:
1014025 function calls (999899 primitive calls) in 28.933 seconds\
45904 calls of linear_search with cum_time as 26.949 seconds\
## binary search:
1058972 function calls (1044521 primitive calls) in 2.263 seconds\
22951 calls of binary_search with cum_time as 0.113 seconds\

## Conclusion:
Binary is much way better than linear search!

# Benchmarking summary:

## linear search:
Searching time spent: 16.152998447418213 sec\
Main func time spent: 17.629664182662964 sec\


## binary search:
Sorting time spent: 0.002223968505859375 sec
Searching time spent: 0.1941835880279541 sec
Main func time spent: 1.1933798789978027 sec

## Conclusion:
The result is reasonable since sorting method takes similar time while binary search beats linear search in searching time.



