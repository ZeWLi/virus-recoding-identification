import os,sys
from Bio import SeqIO


def calculate_gc_content_and_length(fasta_file):
    record = next(SeqIO.parse(fasta_file, "fasta"))
    seq = record.seq
    length = len(seq)
    gc_count = seq.count("G") + seq.count("C")
    gc_content = (gc_count / length) * 100 if length > 0 else 0

    if length > 10000 and gc_content < 50:
        return 1
    else:
        return 0


def main():
    list_virus = os.listdir(sys.argv[1])
    pwd = os.getcwd()

    os.mkdir(sys.argv[2])
    abs_path = os.path.abspath(sys.argv[2])

    os.chdir(sys.argv[1])
    for file in list_virus:
        flag = calculate_gc_content_and_length(file)
        if flag == 1:
            os.system(f'cp {file} {abs_path}')

    os.chdir(pwd)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python select_gc_and_length_cutoff_seq.py <path/to/dir> <output_dir>')
        exit()

    main()
