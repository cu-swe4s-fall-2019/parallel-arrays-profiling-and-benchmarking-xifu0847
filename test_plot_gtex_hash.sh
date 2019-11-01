#!/bin/bash
test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

echo -e "\n\033[31m[Test] Functional test \033[0m\n"
run Func_test_bad_gene_reads python plot_gtex_hash.py --gene_reads=Bad.gz --sample_attributes=GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name=ACTA2 --group_type=SMTS --output_file=ACTA2.png 
assert_in_stderr 'gene_reads file not found'

run Func_test_bad_sample_attr python plot_gtex_hash.py --gene_reads=GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes=Bad.txt --gene_name=ACTA2 --group_type=SMTS --output_file=ACTA2.png
assert_in_stderr 'sample_attributes file not found'

run Func_test_bad_group_type python plot_gtex_hash.py --gene_reads=GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes=GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name=ACTA2 --group_type=Bad --output_file=ACTA2.png
assert_in_stderr 'group_type should be either SMTS or SMTSD'

rm ACTA2.png
run Func_test_good_test python plot_gtex_hash.py --gene_reads=GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes=GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name=ACTA2 --group_type=SMTS --output_file=ACTA2.png
assert_exit_code 0

run Func_test_figure_exists python plot_gtex_hash.py --gene_reads=GTEx_Analysis_2017-06-05_v8_RNASeQCv1.1.9_gene_reads.acmg_59.gct.gz --sample_attributes=GTEx_Analysis_v8_Annotations_SampleAttributesDS.txt --gene_name=ACTA2 --group_type=SMTS --output_file=ACTA2.png
assert_in_stderr 'File already exists.'