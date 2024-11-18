import argparse
import os
import subprocess

def run_method(output_dir, name, input_files, parameters):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    method_mapping_file = os.path.join(output_dir, f'{name}.model.out.txt')

    # Run Cellranger ctrl
    ref_dir = f"01_references/refdata-gex-GRCh38-2024-A"
    cr_outdir = f"{output_dir}/cellranger_out"
    os.makedirs(cr_outdir, exist_ok=True)

    cr_command_1 = f"cellranger count --id testing --fastqs {input_files}"
    #cr_command_1 += f" --output-dir {output_dir} --transcriptome 01_references/refdata-gex-GRCh38-2024-A"
    cr_command_1 += f" --output-dir {cr_outdir} --transcriptome {ref_dir}"
    cr_command_1 += f" --create-bam true --expect-cells 15000 --localcores 16 --localmem 56"

    content = f"This is the cellranger command\n{cr_command_1}\n\n"
    with open(method_mapping_file, 'w') as file:
        file.write(content)

    #a = subprocess.run(cr_command_1.split(),capture_output=True,text=True)
    content += f"Cellranger output:\n"
    #content += a.stdout
    content += "\n\n"

    with open(method_mapping_file, 'w') as file:
        file.write(content)

    # Run Bamboozle case
    bam_pos = f"{cr_outdir}/outs/possorted_genome_bam.bam"
    ref_pos = f"{ref_dir}/fasta/genome.fa"
    anon_bam_pos = f"{cr_outdir}/outs/bamboozled.bam"
    bamboozle_command = f"BAMboozle --bam {bam_pos} --out {anon_bam_pos} --fa {ref_pos}"
    content += f"Bamboozle command:\n{bamboozle_command}\n"
    a = subprocess.run(bamboozle_command.split(),capture_output=True,text=True)
    content += f"Bamboozle output:\n{a.stdout}\n\n"

    with open(method_mapping_file, 'w') as file:
        file.write(content)

    # Run Bamtofastq case
    anon_fastq_pos = f"{output_dir}/anon_fastqs"
    bamtofastq_command = f"bamtofastq --nthreads=16 {anon_bam_pos} {anon_fastq_pos}"
    content += f"Bamtofastq command:\n{bamtofastq_command}\n"
    a = subprocess.run(bamtofastq_command.split(),capture_output=True,text=True)
    content += f"Bamtofastq output:\n{a.stdout}\n\n"

    # Run Cellranger case 2

#    content += f"This is the command to run cellranger on the first reference genome\n"
#    content += cr_command_1
#    content += "\n\n"

#    content = concatenate_input_content(input_files)

    with open(method_mapping_file, 'w') as file:
        file.write(content)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--R1.counts',type=str, help='input file #1')
    parser.add_argument('--R2.counts',type=str, help='input file #1')
#    parser.add_argument('--process.filtered', type=str, help='optional input file #1.', required=False)
#    parser.add_argument('--data.counts', type=str, help='optional input file #1.', required=False)
#    parser.add_argument('--data.meta', type=str, help='input file #2.')
#    parser.add_argument('--data.data_specific_params', type=str, help='input file #3.')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    R1_input = getattr(args, 'R1.counts')
    R2_input = getattr(args, 'R2.counts')
    fastq_paths = os.path.dirname(R1_input) + f"/"

#    process_filtered_input = getattr(args, 'process.filtered')
#    data_counts_input = getattr(args, 'data.counts')
#    data_meta_input = getattr(args, 'data.meta')
#    data_params_input = getattr(args, 'data.data_specific_params')

#    assert process_filtered_input is not None or data_counts_input is not None, "At least one of the values must not be None"
#    data_counts_input = process_filtered_input if process_filtered_input else data_counts_input

    input_files = [R1_input, R2_input]

    # run_method(args.output_dir, args.name, input_files, extra_arguments)
    run_method(args.output_dir, args.name, fastq_paths, extra_arguments)


if __name__ == "__main__":
    main()
