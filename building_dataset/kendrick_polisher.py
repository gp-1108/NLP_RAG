import os
import sys
import json
import multiprocessing as mp
import re
import argparse

def clean_filename(webpage_name):
    """
    Cleans a given webpage name to create a valid filename.
    
    Parameters:
    webpage_name (str): The name of the webpage.
    
    Returns:
    str: A cleaned filename.
    """
    # Replace non-alphanumeric characters with underscores
    clean_name = re.sub(r"[^a-zA-Z0-9]+", "_", webpage_name)
    # Remove leading and trailing underscores
    clean_name = clean_name.strip("_")
    # Ensure the filename is not empty
    if not clean_name:
        clean_name = "unnamed_page"
    return clean_name

def process_file(file_path):
    """
    Processes a single file to extract JSON objects containing specific keywords.
    
    Parameters:
    file_path (str): The path to the file to be processed.
    
    Returns:
    list: A list of JSON objects that contain the keywords 'kendrick' and 'lamar'.
    """
    json_objects = []
    with open(file_path, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                text = data.get('text', '').lower()
                # Check for the presence of the words 'kendrick' and 'lamar'
                if text.count("kendrick") >= 1 and text.count("lamar") >= 1:
                    json_objects.append(data)
            except json.JSONDecodeError:
                pass
    return json_objects

def process_folder(folder_path, output_dir, batch_size):
    """
    Processes all files in a folder, extracting relevant JSON objects and writing them to the output directory.
    
    Parameters:
    folder_path (str): The path to the folder containing the files.
    output_dir (str): The path to the output directory.
    batch_size (int): The number of files to process in each batch.
    """
    files = []
    # Collect all file paths in the folder
    for subdir, dirs, file_list in os.walk(folder_path):
        for file in file_list:
            file_path = os.path.join(subdir, file)
            if os.path.isfile(file_path):
                files.append(file_path)
    
    counter = 0
    pool = mp.Pool()
    all_jsons = []
    # Process files in batches
    while counter < len(files):
        end_index = min(counter + batch_size, len(files))
        jsons = pool.map(process_file, files[counter:end_index])
        jsons = [item for sublist in jsons for item in sublist]  # Flatten the list
        all_jsons.extend(jsons)
        counter = end_index
        print(f"Ended batch {int(counter / batch_size)}, processed {counter/len(files)*100:.1f}%")
    
    print("Gathered all data, writing to files")
    # Write extracted JSON objects to files
    for json_obj in all_jsons:
        title = clean_filename(json_obj["title"])
        id = json_obj["id"]
        text = json_obj["text"]
        with open(f"{output_dir}/{title}_{id}.txt", "w") as f:
            f.write(text)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a folder of JSON files and extract relevant data.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing JSON files.')
    parser.add_argument('output_dir', type=str, help='Directory where output files will be saved.')
    parser.add_argument('batch_size', type=int, help='Number of files to process in each batch. 500 is a good starting point.')

    args = parser.parse_args()

    # Validate folder path
    if not os.path.isdir(args.folder_path):
        print("Invalid folder path.")
        sys.exit(1)

    # Ensure output directory exists
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    # Validate batch size
    if args.batch_size <= 0:
        print("batch_size must be a positive integer.")
        sys.exit(1)

    # Process the folder with the provided arguments
    process_folder(args.folder_path, args.output_dir, args.batch_size)
