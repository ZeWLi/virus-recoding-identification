import os,sys
from Bio import SeqIO

def parse_final_recoding(file):
    with open(file) as f:
        a = f.readlines()[1:]

    result = {}

    for line in a:
        split = line.strip().split('\t')
        result[f'{split[0]}'] = split[-1]

    return result

## deal with sequences less than 20k
def remove_duplicates(input_fasta, output_fasta):
    """
    Remove duplicate sequences from a FASTA file and save the unique sequences to a new file.

    Args:
        input_fasta (str): Path to the input FASTA file.
        output_fasta (str): Path to the output FASTA file where unique sequences will be saved.
    """
    unique_sequences = {}
    for record in SeqIO.parse(input_fasta, "fasta"):
        seq_str = str(record.seq)
        if seq_str not in unique_sequences:
            unique_sequences[seq_str] = record

    # Write unique sequences to the output file
    with open(output_fasta, "w") as output_handle:
        SeqIO.write(unique_sequences.values(), output_handle, "fasta")



def main():
    lis_all = os.listdir(sys.argv[1])
    abs_path_recoding = os.path.abspath(sys.argv[1])
    pwd = os.getcwd()

    result = parse_final_recoding(sys.argv[2])

    lis_not_recoding = list(set(lis_all) - set(result.keys()))
    for i in lis_not_recoding:
        result[i] = 11

    os.mkdir(sys.argv[3])
    abs_path = os.path.abspath(sys.argv[3])

    redo = []

    for file in result:
        name = os.path.splitext(file)[0]
        os.system(f'mkdir -p {abs_path}/{name}')

        ## deal with sequences less than 20k
        record = next(SeqIO.parse(f'{sys.argv[1]}/{file}', "fasta"))
        length = len(record.seq)

        if length > 20000:
            # use -single is fine
            os.system(f'prodigal -a {abs_path}/{name}/{name}.pro.fa -d {abs_path}/{name}/{name}.gene.fa -i {sys.argv[1]}/{file} -f gff -p single -g {result[file]} -q -m')

        elif result[file] != 11:
            # sequences length less than 20k and recoding
            redo.append(name)
            os.system(f'cat {abs_path_recoding}/{file} {abs_path_recoding}/{file} > temp.fa')
            os.system(f'prodigal -a {abs_path}/{name}/{name}.pro.fa -d {abs_path}/{name}/{name}.gene.fa -i temp.fa -f gff -p single -g {result[file]} -q -m')

            os.system('rm temp.fa')

        else:
            # sequences length less than 20k and use default genetic code
            os.system(f'prodigal -a {abs_path}/{name}/{name}.pro.fa -d {abs_path}/{name}/{name}.gene.fa -i temp.fa -f gff -p meta -g {result[file]} -q -m')

    os.chdir(abs_path)

    if redo != []:
        for name in redo:
            os.chdir(name)
            remove_duplicates(f'{name}.pro.fa', f'{name}.pro.fa')
            remove_duplicates(f'{name}.gene.fa', f'{name}.gene.fa')
            os.chdir('..')

    os.chdir(pwd)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python batch_run_prodigal_with_recoding.py <input_dir> <output_dir>')
        exit()

    main()