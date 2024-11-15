import argparse
import os
import subprocess

def concatenate_input_content(input_files):
    concatenated_content = ""  # Initialize an empty string to hold the concatenated content

    # Iterate over each input file
    for input_file in input_files:
        # Open each input file in read mode and read its content
        with open(input_file, 'r') as file:
            # Read the content of the input file and append it to the concatenated_content string
            concatenated_content += file.read()
            # Optionally, you can add a newline between the content of each file
            concatenated_content += '\n'

    return concatenated_content


def run_method(output_dir, name, input_files, parameters):
    # Create the output directory if it doesn't exist
    output_dir += "/cellranger_out"
    os.makedirs(output_dir, exist_ok=True)

    # Run Cellranger ctrl
    # Figure out how to extract reference genome: /data/refdata-gex-GRCh38-2024-A"

    cr_command_1 = f"cellranger count --id testing --fastqs {input_files}"
    cr_command_1 += f" --output-dir {output_dir} --transcriptome 01_references/refdata-gex-GRCh38-2024-A"
    cr_command_1 += f" --create-bam true --expect-cells 15000 --localcores 4 --localmem 4"

    # orig_fastq_path="/home/projects/dtu_00062/people/sorsan/test1/short_data/"
    # orig_out="/home/projects/dtu_00062/people/sorsan/test1/short_orig_processed_hg38-2024-A"

    # cellranger count --id short_sample_orig --fastqs $orig_fastq_path --output-dir $orig_out
    # --transcriptome $transcriptome_ref --create-bam true --expect-cells 15000 --localcores 28 --localmem 128

    # Run Cellranger case 1
    subprocess.run(cr_command_1)

    # Run Bamboozle case

    # Run Bamtofastq case

    # Run Cellranger case 2

    content = f"This is the command to run cellranger on the first reference genome\n"
    content += cr_command_1
    content += "\n\n"

#    content = concatenate_input_content(input_files)

    method_mapping_file = os.path.join(output_dir, f'{name}.model.out.txt')
    content += f"Input files:\n\t"
    content += input_files
    content += f"\nOutput directory:\n\t"
    content += output_dir

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
