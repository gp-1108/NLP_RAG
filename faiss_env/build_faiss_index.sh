#!/bin/bash

#SBATCH --job-name faiss_index_build
#SBATCH --mail-user <insert_email_here>
#SBATCH --mail-type ALL
#SBATCH --error error_%j.txt
#SBATCH --output output_%j.txt
#SBATCH --time 02-00:00
#SBATCH --ntasks 1
#SBATCH --partition allgroups
#SBATCH --mem 12G

working_dir="<insert_working_dir_here>"
dataset_name="extract_kendrick"
dataset_path="/ext/${dataset_name}"
archive_name="${dataset_name}.tar.gz"
archive_path="/ext/${archive_name}"
sif_image_path="/ext/faiss_env.sif"
faiss_build_path="/ext/faiss_build"

# Removing any old data
rm -rf $dataset_path
rm -rf $archive_path
rm -rf $faiss_build_path

# Adding local python packages
echo "$(whoami)"
export PATH="$PATH:$(python3 -m site --user-base)/bin"

cd $working_dir

gdown 1Tz-YocAJuOm8poZbCSlhLmw2nHcpmD6I -O $archive_path
gdown 1zbJm29VxqwqHQGSU3WsSbs86BqbsGj2n -O $sif_image_path

cd /ext
tar -xzf $archive_name

cd $working_dir

singularity exec --bind /ext:/ext $sif_image_path python3 build_faiss_index.py $dataset_path $faiss_build_path

# Change directory to the parent directory of faiss_build_path
cd "$(dirname "$faiss_build_path")"

# Create the tar archive without the leading directory
tar -czvf faiss_index.tar.gz "$(basename "$faiss_build_path")"

# Move the tar archive back to the working directory
mv faiss_index.tar.gz $working_dir