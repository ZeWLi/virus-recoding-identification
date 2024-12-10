import sys,os
from Bio import SeqIO


def parse_gff_file(file):
    with open(file) as f:
        total = 0
        for line in f:
            if not line.startswith('#'):
                split = line.split('\t')
                total += eval(split[5])

    return total


def prodigal_pipeline(outdir,file):
    os.system(f"mkdir -p {outdir}/{file}")
    genetic_code = [11,4,25,15,6]

    record = next(SeqIO.parse(file, "fasta"))
    length = len(record.seq)

    if length > 20000:
        for code in genetic_code:
            os.system(f'prodigal -i {file} -o {outdir}/{file}/{code}.gff -f gff -g {code} -p single')

    else:
        os.system(f'cat {file} {file} > temp.fa')
        for code in genetic_code:
            os.system(f'prodigal -i temp.fa -o {outdir}/{file}/{code}.gff -f gff -g {code} -p single')

        os.system('rm temp.fa')


def main():
    lis_recoding = os.listdir(sys.argv[1])
    pwd = os.getcwd()

    os.mkdir(sys.argv[2])
    abs_path = os.path.abspath(sys.argv[2])

    os.chdir(sys.argv[1])
    for file in lis_recoding:
        prodigal_pipeline(abs_path,file)

    os.chdir(abs_path)
    lis_gff = os.listdir('.')
    out = {}

    for dir in lis_gff:
        lis = os.listdir(dir)
        os.chdir(dir)
        out_gff = {}

        for file in lis:
            out_gff[file] = parse_gff_file(file)

            # identify recoding
            sorted_gff = sorted(out_gff.items(), key=lambda item: float(item[1]), reverse = True)  # sort by value
            if sorted_gff[0][1] >= 1.1 * out_gff['11.gff']:
                out_gff['final_recoding'] = sorted_gff[0][0].split('.')[0]
            else:
                out_gff['final_recoding'] = 11

        out[dir] = out_gff

        os.chdir('..')

    os.chdir(pwd)

    with open(sys.argv[3],'w') as f:
        f.write('file\tstandard\t4\t15\t25\t6\tfinal_recoding\n')
        for i in out:
            f.write(f'{i}\t{out[i]["11.gff"]}\t{out[i]["4.gff"]}\t{out[i]["15.gff"]}\t{out[i]["25.gff"]}\t{out[i]["6.gff"]}\t{out[i]["final_recoding"]}\n')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: python batch_run_gff_output_genetic_code.py <path/to/dir> <outdir> <outfile>')
        exit()

    main()
