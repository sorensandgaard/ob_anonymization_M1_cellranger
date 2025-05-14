import argparse
import os
import requests
import subprocess

def create_file(out_filename,in_url):
    r = requests.get(in_url, allow_redirects=True)
    open(out_filename, 'wb').write(r.content)


def run_method(output_dir, name, input_file, parameters):

    anon_fastq_pos = input_file[0]
    ctrl_fastq_pos = input_file[1]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    log_file = os.path.join(output_dir, f'{name}.log.txt')

    # Load R script to create seurat objects
    R_script_url = "https://raw.githubusercontent.com/sorensandgaard/ob_anonymization_M1_cellranger/main/initialize_seurat_object.R"
    script_R_file = os.path.join(output_dir, f'initialize_seurat_object.R')
    create_file(script_R_file,R_script_url)

    # Find name of bamtofastq folder
    # a = subprocess.run(f"ls {anon_fastq_pos}".split(),capture_output=True,text=True)
    # content += f"fastq foldername object: {a.stdout}\n"
    # fastq_foldername = a.stdout[:-1]
    # content += f"fastq foldername: {fastq_foldername}\n\n"

    # Run Cellranger case
    ref_dir = f"01_references/{parameters[0]}"
    cr_outdir = f"{output_dir}/cellranger_out"
    os.makedirs(cr_outdir, exist_ok=True)
    cr_command = f"cellranger count --id {name}_second_align --fastqs {anon_fastq_pos}"
    cr_command += f" --output-dir {cr_outdir} --transcriptome {ref_dir}"
    cr_command += f" --create-bam true --expect-cells 15000 --localcores 24 --localmem 100"
    content = f"This is the anonymous cellranger command\n{cr_command}\n\n"

    a = subprocess.run(cr_command.split(),capture_output=True,text=True)
    content += f"Cellranger output:\n"
    content += a.stdout
    content += "\n\n"

    # Convert cellranger case output to seurat object
    filtered_expr_pos = f"{cr_outdir}/outs/filtered_feature_bc_matrix"
    outfile_pos = f"{output_dir}/{name}_case.rds"
    R_command = f"Rscript {script_R_file} {outfile_pos} {filtered_expr_pos}"
    a = subprocess.run(R_command.split(),capture_output=True,text=True)
    content += f"R command:\n{R_command}\n"

    # Cleanup unnecessary cellranger files
    cleanup_command = f"rm -rf {cr_outdir}"
    a = subprocess.run(cleanup_command.split(),capture_output=True,text=True)

    # Create dummy anon cellranger files
    # os.makedirs(f"{cr_outdir}/outs",exist_ok=True) # dummy creation
    # os.makedirs(f"{cr_outdir}/outs/filtered_feature_bc_matrix",exist_ok=True) # dummy creation
    # subprocess.run(f"touch {cr_outdir}/outs/filtered_feature_bc_matrix/test1.txt".split(),capture_output=True,text=True)
    # subprocess.run(f"touch {cr_outdir}/outs/filtered_feature_bc_matrix/test2.txt".split(),capture_output=True,text=True)

    # Run Cellranger ctrl
    # If cellranger file doesn't already exist: #########
    ctrl_dir = f"ctrl_expr_mats/{name}/M1/{parameters[0]}"
    if not os.path.isdir(ctrl_dir):
#    if not os.path.isfile(f"{ctrl_dir}/{name}_ctrl.rds"):
        cr_outdir_ctrl = f"{ctrl_dir}/cellranger"
        os.makedirs(cr_outdir_ctrl, exist_ok=True)
        cr_command = f"cellranger count --id {name}_ctrl --fastqs {ctrl_fastq_pos}"
        cr_command += f" --output-dir {cr_outdir_ctrl} --transcriptome {ref_dir}"
        cr_command += f" --create-bam true --expect-cells 15000 --localcores 24 --localmem 100"
        content += f"This is the control cellranger command\n{cr_command}\n\n"

        a = subprocess.run(cr_command.split(),capture_output=True,text=True)
        content += f"Cellranger output:\n"
        content += a.stdout
        content += "\n\n"

        # Convert ctrl cellranger output to seurat object
        filtered_expr_pos = f"{cr_outdir_ctrl}/outs/filtered_feature_bc_matrix"
        outfile_pos = f"{ctrl_dir}/{name}_ctrl.rds"
        R_command = f"Rscript {script_R_file} {outfile_pos} {filtered_expr_pos}"
        a = subprocess.run(R_command.split(),capture_output=True,text=True)
        content += f"R command:\n{R_command}\n"

        # Cleanup unnecessary cellranger files
        cleanup_command = f"rm -rf {cr_outdir_ctrl}"
        a = subprocess.run(cleanup_command.split(),capture_output=True,text=True)

    # Copy cellranger ctrl file to output folder
    cp_ctrl_command = f"cp {ctrl_dir}/{name}_ctrl.rds {output_dir}/."
    a = subprocess.run(cp_ctrl_command.split(), capture_output=True,text=True)

    # Create dummy ctrl cellranger files
    # os.makedirs(f"{cr_outdir_ctrl}/outs",exist_ok=True) # dummy creation
    # os.makedirs(f"{cr_outdir_ctrl}/outs/filtered_feature_bc_matrix",exist_ok=True) # dummy creation
    # subprocess.run(f"touch {cr_outdir_ctrl}/outs/filtered_feature_bc_matrix/test1.txt".split(),capture_output=True,text=True)
    # subprocess.run(f"touch {cr_outdir_ctrl}/outs/filtered_feature_bc_matrix/test2.txt".split(),capture_output=True,text=True)

    with open(log_file, 'w') as file:
        file.write(content)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Run method on files.')

    # Add arguments
    parser.add_argument('--output_dir', type=str, help='output directory where method will store results.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    parser.add_argument('--anon.R1.counts',type=str, help='anonymous reads R1')
    parser.add_argument('--anon.R2.counts',type=str, help='anonymous reads R2')
    parser.add_argument('--R1.counts',type=str, help='raw reads R1')
    parser.add_argument('--R2.counts',type=str, help='raw reads R2')

    # Parse arguments
    args, extra_arguments = parser.parse_known_args()

    anon_R1_pos = getattr(args, 'anon.R1.counts')
    anon_R2_pos = getattr(args, 'anon.R2.counts')
    R1_pos = getattr(args, 'R1.counts')
    R2_pos = getattr(args, 'R2.counts')
    ctrl_fastq_pos = os.path.dirname(R1_pos) + f"/"
    anon_fastq_pos = os.path.dirname(anon_R1_pos) + f"/"

    # run_method(args.output_dir, args.name, input_files, extra_arguments)
    run_method(args.output_dir, args.name, [anon_fastq_pos,ctrl_fastq_pos], extra_arguments)


if __name__ == "__main__":
    main()
