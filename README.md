Some viruses use genetic codes other than standard genetic code. These scripts could work on Linux server with Biopython (python) and Prodigal (worked for v2.6.3)
Sequences with length > 10k and GC content 50 % are selected as candidate sequences.

# Usage
```
python /data/lizw/script/genetic_code/select_gc_and_length_cutoff_seq.py all_virus_seq_split recoding
```
all_virus_seq_split is a directory containing fasta files of single viral sequences
recoding is a directory generated to store candidate sequences to use an alternative genetic code

```
python /data/lizw/script/genetic_code/batch_run_gff_output_genetic_code.py recoding recoding_file genetic_code_rating.txt
```
recoding is mentioned aboved
recoding_file is a output directory containing prodigal gff files 
genetic_code_rating.txt is a file to summarize the scores of alternative genetic codes and the selection of genetic codes

```
python /data/lizw/script/genetic_code/batch_run_prodigal_with_recoding.py all_virus_seq_split recoding_rating_out.txt prodigal_out
```
all_virus_seq_split is above-mentioned
recoding_rating_out.txt is above-mentioned 
prodigal_out is going to be generated, storing the prodigal protein/gene files

Prodigal didn't work for sequences less than 20k with -p single option, however, it is needed for changing the genetic codes in Prodigal. 
In the second and the third scripts, I doubled the sequences less than 20k, this doesn't change the codon usage of sequences and Prodigal worked for it.
When Prodigal predicts these doubled sequences, the output is the same set of proteins/genes, then I remove the duplicated part of files.

