import configparser
import sys
import os
from time import sleep
import file_size_class
import csv


def load_configuration_file():
    config = configparser.ConfigParser()
    json_configuration = {}

    # for sandbox setup configuration
    # complete_executable_path = sys.path[0] + '\configurationFile.ini'

    # for live setup configuration
    complete_executable_path = sys.executable.replace("TPCPP-FolderListingTool.exe", "configurationFile.ini")

    config.read(complete_executable_path)

    default_settings = config['DEFAULT']
    json_configuration['file_extension_filter'] = default_settings['file_extension_filter']
    json_configuration['output_location'] = default_settings['output_location']

    return json_configuration


def gather_file_location_for_listing(file_extensions
                                     , directory_location):
    print(f"Gathering files at '{directory_location}' with extensions '{file_extensions}'")
    if os.path.exists(directory_location):
        valid_file_lists = []

        extensions = file_extensions.split(', ')
        for extension in extensions:
            for dir_path, dir_names, file_names in os.walk(directory_location):
                for file_name in [f for f in file_names if f.endswith(extension)]:
                    valid_file_lists.append(os.path.join(directory_location, file_name))
    else:
        print(f"Path {directory_location} is not valid!")
        exit(0)

    return valid_file_lists


def gather_bytes_from_files_location(complete_files_location):
    complete_files_data = []
    if len(complete_files_location) > 0:
        print(f"Processing {len(complete_files_location)} files for bytes gathering! ")
        count = 1
        for file in complete_files_location:
            complete_files_data.append(file_size_class.FileSizeDetails(count
                                                                       ,os.path.basename(file)
                                                                       ,os.path.getsize(file)))
            count = count + 1
    return complete_files_data


def save_to_csv_file(complete_files, output_location):
    with open(os.path.join(output_location, 'output.csv') , 'w', newline='') as result_file:
        field_names = ['counter', 'file_name', 'file_size']
        wr = csv.DictWriter(result_file, fieldnames=field_names)
        wr.writeheader()
        for file in complete_files:
            wr.writerow({'counter':file.counter_no, 'file_name':file.file_name, 'file_size': file.bytes_size})
    print(f"Done writing at {output_location}\output.csv, please check!")


def main():
    json_configuration_file = load_configuration_file()
    print(f"Successfully loaded configuration file at {sys.executable.replace('TPCPP-FolderListingTool.exe', 'configurationFile.ini')}")
    print(f"Enter directory to gather listing:")
    directory_location = input()
    complete_files_location = gather_file_location_for_listing(json_configuration_file['file_extension_filter']
                                     ,directory_location)
    complete_files_with_bytes = gather_bytes_from_files_location(complete_files_location)
    save_to_csv_file(complete_files_with_bytes, json_configuration_file['output_location'])

    sleep(10)


main()