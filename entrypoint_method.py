import argparse
import os
import subprocess

def run_method(output_dir, name, input_file, parameters):

    bam_file = input_file[0]
    ctrl_fastq_pos = input_file[1]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f'{name}.log.txt')

    # Run bamtofastq
    anon_fastq_pos = f"{output_dir}/anon_fastqs"
    bamtofastq_command = f"bamtofastq --nthreads=16 {bam_file} {anon_fastq_pos}"
    content = f"Bamtofastq command:\n{bamtofastq_command}\n"
    # a = subprocess.run(bamtofastq_command.split(),capture_output=True,text=True)
    # content += f"Bamtofastq output:\n{a.stdout}\n\n"

    # Find name of bamtofastq folder
    # a = subprocess.run(f"ls {anon_fastq_pos}".split(),capture_output=True,text=True)
    # content += f"fastq foldername object: {a.stdout}\n"
    # fastq_foldername = a.stdout[:-1]
    # content += f"fastq foldername: {fastq_foldername}\n\n"

    # Create dummy bamtofastq files
    a = subprocess.run(f"mkdir {anon_fastq_pos}".split(),capture_output=True,text=True)
    a = subprocess.run(f"mkdir {anon_fastq_pos}/H_tmp".split(),capture_output=True,text=True)
    a = subprocess.run(f"touch {anon_fastq_pos}/H_tmp/test.fastq".split(),capture_output=True,text=True)

    # Run Cellranger case
    ref_dir = f"01_references/{parameters[0]}"
    cr_outdir = f"{output_dir}/cellranger_out"
    os.makedirs(cr_outdir, exist_ok=True)
    cr_command = f"cellranger count --id {name}_second_align --fastqs {anon_fastq_pos}"
    cr_command += f" --output-dir {cr_outdir} --transcriptome {ref_dir}"
    cr_command += f" --create-bam true --expect-cells 15000 --localcores 24 --localmem 100"
    content += f"This is the anonymous cellranger command\n{cr_command}\n\n"

    # a = subprocess.run(cr_command.split(),capture_output=True,text=True)
    # content += f"Cellranger output:\n"
    # content += a.stdout
    # content += "\n\n"

    # Create dummy anon cellranger files
    os.makedirs(f"{cr_outdir}/outs",exist_ok=True) # dummy creation
    os.makedirs(f"{cr_outdir}/outs/filtered_feature_bc_matrix",exist_ok=True) # dummy creation
    subprocess.run(f"touch {cr_outdir}/outs/filtered_feature_bc_matrix/test1.txt".split(),capture_output=True,text=True)
    subprocess.run(f"touch {cr_outdir}/outs/filtered_feature_bc_matrix/test2.txt".split(),capture_output=True,text=True)

    # Run Cellranger ctrl
    cr_outdir_ctrl = f"ctrl_expr_mats/{name}/M1/{parameters[0]}"
    os.makedirs(cr_outdir_ctrl, exist_ok=True)
    cr_command = f"cellranger count --id {name}_ctrl --fastqs {ctrl_fastq_pos}"
    cr_command += f" --output-dir {cr_outdir_ctrl} --transcriptome {ref_dir}"
    cr_command += f" --create-bam true --expect-cells 15000 --localcores 24 --localmem 100"
    content += f"This is the control cellranger command\n{cr_command}\n\n"

    # a = subprocess.run(cr_command.split(),capture_output=True,text=True)
    # content += f"Cellranger output:\n"
    # content += a.stdout
    # content += "\n\n"

    # Create dummy ctrl cellranger files
    os.makedirs(f"{cr_outdir_ctrl}/outs",exist_ok=True) # dummy creation
    os.makedirs(f"{cr_outdir_ctrl}/outs/filtered_feature_bc_matrix",exist_ok=True) # dummy creation
    subprocess.run(f"touch {cr_outdir_ctrl}/outs/filtered_feature_bc_matrix/test1.txt".split(),capture_output=True,text=True)
    subprocess.run(f"touch {cr_outdir_ctrl}/outs/filtered_feature_bc_matrix/test2.txt".split(),capture_output=True,text=True)

    # Copy expression matrix to output folder
    # cp_matrix_command = f"cp -r {cr_outdir}/outs/filtered_feature_bc_matrix {output_dir}/."
    # a = subprocess.run(cp_matrix_command.split(),capture_output=True,text=True)

    # Cleanup unnecessary cellranger files
    # cleanup_command = f"rm -rf {cr_outdir}"
    # a = subprocess.run(cleanup_command.split(),capture_output=True,text=True)

    with open(log_file, 'w') as file:
        file.write(content)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--init_bam',type=str, help='anonymized_bam_file')
    parser.add_argument('--R1.counts',type=str, help='raw reads R1')
    parser.add_argument('--R2.counts',type=str, help='raw reads R2')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    bam_file = getattr(args, 'init_bam')
    R1_pos = getattr(args, 'R1.counts')
    R2_pos = getattr(args, 'R2.counts')
    ctrl_fastq_pos = os.path.dirname(R1_pos) + f"/"

    # run_method(args.output_dir, args.name, input_files, extra_arguments)
    run_method(args.output_dir, args.name, [bam_file,ctrl_fastq_pos], extra_arguments)


if __name__ == "__main__":
    main()
