import os

def validate_survey_data_folder(path):
    # Check if the provided path exists
    if not os.path.exists(path):
        return f"Path {path} does not exist."

    # Check for folders 011_001 to 011_020
    for i in range(1, 21):
        folder_name = f"011_{str(i).zfill(3)}"
        folder_path = os.path.join(path, folder_name)
        if not os.path.isdir(folder_path):
            return f"Folder {folder_name} is missing."

        # Check for the JSON file inside each folder
        json_file = None
        for file in os.listdir(folder_path):
            if file.endswith("_runtime_settings.json"):
                json_file = file
                break

        if not json_file:
            return f"Runtime settings JSON file is missing in folder {folder_name}."

        # Extract master_run_number from the JSON file name
        master_run_number = json_file.split('_')[-3].split('-')[0]
        print(f"verifying master run number: {master_run_number}")

        # Verify the raw_data folder exists
        raw_data_path = os.path.join(folder_path, 'raw_data')
        if not os.path.isdir(raw_data_path):
            return f"raw_data folder is missing inside {folder_path}."

        # Verify the folder named after master_run_number exists in raw_data
        master_run_folder_path = os.path.join(raw_data_path, master_run_number)
        if not os.path.isdir(master_run_folder_path):
            return f"Folder {master_run_number} is missing in {raw_data_path}."

        # Verify the three pkl files inside the master_run_number folder
        for i in range(3):
            pkl_file = f"data{i}.pkl"
            pkl_file_path = os.path.join(master_run_folder_path, pkl_file)
            if not os.path.isfile(pkl_file_path):
                return f"{pkl_file} is missing in folder {master_run_number}."
        
        # verify chirp_up and chirp_down exist
        chirp_up_folder_path = os.path.join(folder_path, 'chirp_up')
        if not os.path.isdir(chirp_up_folder_path):
            return f"chirp_up folder is missing in {folder_path}."
        
        chirp_up_fringes_data_path = os.path.join(chirp_up_folder_path, 'fringes_data.csv')
        if not os.path.isfile(chirp_up_fringes_data_path):
            return f"fringes_data.csv is missing in {chirp_up_folder_path}."

        chirp_down_folder_path = os.path.join(folder_path, 'chirp_down')
        if not os.path.isdir(chirp_down_folder_path):
            return f"chirp_down folder is missing in {folder_path}."
        chirp_down_fringes_data_path = os.path.join(chirp_down_folder_path, 'fringes_data.csv')
        if not os.path.isfile(chirp_down_fringes_data_path):
            return f"fringes_data.csv is missing in {chirp_down_folder_path}."

    return "All validations passed successfully."

path = r"C:\Users\vaish\dsvv_atomionics\Survey_Data"
print(validate_survey_data_folder(path))