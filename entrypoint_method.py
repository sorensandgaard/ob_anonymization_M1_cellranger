import argparse
import os
import subprocess

def run_method(output_dir, name, input_file, parameters):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f'{name}.log.txt')

    # Run bamtofastq
    anon_fastq_pos = f"{output_dir}/anon_fastqs"
    bamtofastq_command = f"bamtofastq --nthreads=16 {input_file} {anon_fastq_pos}"
    content += f"Bamtofastq command:\n{bamtofastq_command}\n"
    # a = subprocess.run(bamtofastq_command.split(),capture_output=True,text=True)
    # content += f"Bamtofastq output:\n{a.stdout}\n\n"

    # Create dummy bamtofastq files
    a = subprocess.run(f"mkdir {anon_fastq_pos}".split(),capture_output=True,text=True)
    a = subprocess.run(f"mkdir {anon_fastq_pos}/H_tmp".split(),capture_output=True,text=True)
    a = subprocess.run(f"touch {anon_fastq_pos}/H_tmp/test.fastq".split(),capture_output=True,text=True)

    # Run Cellranger ctrl
    ref_dir = f"01_references/{parameters[0]}"
    cr_outdir = f"{output_dir}/cellranger_out"
    os.makedirs(cr_outdir, exist_ok=True)
    cr_command = f"cellranger count --id testing --fastqs {anon_fastq_pos}"
    cr_command += f" --output-dir {cr_outdir} --transcriptome {ref_dir}"
    cr_command += f" --create-bam true --expect-cells 15000 --localcores 16 --localmem 56"
    content = f"This is the cellranger command\n{cr_command}\n\n"

    #a = subprocess.run(cr_command_1.split(),capture_output=True,text=True)
    content += f"Cellranger output:\n"
    #content += a.stdout
    content += "\n\n"

    # Create dummy cellranger files
    os.makedirs(f"{cr_outdir}/outs",exist_ok=True) # dummy creation
    os.makedirs(f"{cr_outdir}/outs/filtered_feature_bc_matrix",exist_ok=True) # dummy creation
    subprocess.run(f"cp {log_file} {cr_outdir}/outs/possorted_genome_bam.bam".split(),capture_output=True,text=True)
    subprocess.run(f"touch {cr_outdir}/outs/filtered_feature_bc_matrix/test1.txt".split(),capture_output=True,text=True)
    subprocess.run(f"touch {cr_outdir}/outs/filtered_feature_bc_matrix/test2.txt".split(),capture_output=True,text=True)

    with open(log_file, 'w') as file:
        file.write(content)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--init_bam',type=str, help='anonymized_bam_file')
#    parser.add_argument('--process.filtered', type=str, help='optional input file #1.', required=False)
#    parser.add_argument('--data.counts', type=str, help='optional input file #1.', required=False)
#    parser.add_argument('--data.meta', type=str, help='input file #2.')
#    parser.add_argument('--data.data_specific_params', type=str, help='input file #3.')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    bam_file = getattr(args, 'init_bam')

#    process_filtered_input = getattr(args, 'process.filtered')
#    data_counts_input = getattr(args, 'data.counts')
#    data_meta_input = getattr(args, 'data.meta')
#    data_params_input = getattr(args, 'data.data_specific_params')

#    assert process_filtered_input is not None or data_counts_input is not None, "At least one of the values must not be None"
#    data_counts_input = process_filtered_input if process_filtered_input else data_counts_input

    # run_method(args.output_dir, args.name, input_files, extra_arguments)
    run_method(args.output_dir, args.name, bam_file, extra_arguments)


if __name__ == "__main__":
    main()
