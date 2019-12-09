"""
download_file_from_google_drive.py

Module for Download_ProcessedData_from_Google.ipynb to download the processed
data from the google drive into local_climate_change_tool/data/processed_data/.
This gathers data used to run the climate dashboard.
"""
import io
import tarfile
import os
import sys
import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload

CWD = os.getcwd()
WORKING_DIR = CWD + '/phase1_data_wrangler/'
print(WORKING_DIR)
sys.path.insert(0, WORKING_DIR)
import analysis_parameters as params


def get_credentials(permissions_dir):
    """Gets the credentials for the drive in which the data is saved."""
    obj = lambda: None
    web_dict = {'auth_host_name':'localhost', 'noauth_local_webserver':'store_true',
                'auth_host_port':[8080, 8090], 'logging_level':'ERROR'}
    for k, var in web_dict.items():
        setattr(obj, k, var)

    # authorization boilerplate code
    scopes = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage(permissions_dir + 'token.json')
    creds = store.get()

    # The following will give you a link if token.json does not exist,
    # the link allows the user to give this app permission
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(permissions_dir + 'client_id.json', scopes)
        creds = tools.run_flow(flow, store, obj)
    return creds


def download_file(file_id, filename_id, creds):
    """Starts the file download and prints update statements for the user.

    Args:
        file_id: The string key specifying which file to download.
        filename_id: The string key of the name of the file.
        creds: The credentials, as returned by get_credentials.
    """
    drive = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    request = drive.files().get_media(fileId=file_id)
    file_to_download = io.FileIO(filename_id, mode='w')
    downloader = MediaIoBaseDownload(file_to_download, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


def extract_files(filename_id, dir_extracted_data):
    """Extracts the tar files in filename_id to be readable."""
    file_to_extract = tarfile.open(filename_id)
    file_to_extract.extractall(path=dir_extracted_data)


def remove_extracted_files(dir_extracted_data, filename_extracted):
    """Removes the extracted tar files from the directory."""
    os.system('rm -rf ' + dir_extracted_data + filename_extracted)


def remove_compressed_file(filename_compressed):
    """Removes the compressed files from the directory."""
    os.system('rm -rf ' + filename_compressed)


def move_file(filename_id, dir_extracted_data):
    """Moves the file to the appropriate directory."""
    os.system('mv ' + filename_id + ' ' + dir_extracted_data + filename_id)


def download_data(dir_google_drive_permissions,
                  dir_extracted_data,
                  file_id,
                  filename_id,
                  filename_extracted,
                  need_to_extract,
                  print_statements_on=True):
    """Downloads the data to the local repository in the correct directory.

    Args:
        dir_google_drive_permissions: String name of the drive where data is saved.
        dir_extracted_data: String directory of the extracted tar files.
        file_id: The string key specifying which file to download.
        filename_id: The string key of the name of the file.
        filename_extracted: The string name of the file after extracting it from the tar file.
        need_to_extract: True if the file is a tar file you need to extract.
        print_statements_on: True (default) to print what is happening to the user.
    """
    if print_statements_on:
        print(' -> getting credentials')
    creds = get_credentials(permissions_dir=dir_google_drive_permissions)

    if print_statements_on:
        print(' -> downloading files')
    download_file(file_id, filename_id, creds)

    if need_to_extract:
        if print_statements_on:
            print(''' -> removing any files already existing in folder where
                  extracted files is going''')
        remove_extracted_files(dir_extracted_data, filename_extracted)

        if print_statements_on:
            print(' -> extracting files')
        extract_files(filename_id, dir_extracted_data)

        if print_statements_on:
            print(' -> removing originally downloaded compressed file')
        remove_compressed_file(filename_id)
    else:
        move_file(filename_id, dir_extracted_data)


def download_data_predefined(file_to_download, print_statements_on):
    """Starts the process to download the files from google drive."""
    dir_google_drive_permissions = params.DIR_GOOGLE_DRIVE_PERMISSIONS
    if file_to_download == 'Processed_Data':
        # file link to view: https://drive.google.com/open?id=1EG9ZzuoaG4z3KuYubdspTV8S8skTFMzE
        file_id = '1EG9ZzuoaG4z3KuYubdspTV8S8skTFMzE'
        filename_id = 'processed_data.tar.gz'
        filename_extracted = 'processed_data'
        dir_extracted_data = params.DIR_DATA
        need_to_extract = True
    elif file_to_download == 'Raw_Historical_Obs':
        # file link to view: https://drive.google.com/open?id=1J3lpNptF2PxLRCJxJVJkDpd4ndyDKp8j
        file_id = '1J3lpNptF2PxLRCJxJVJkDpd4ndyDKp8j'
        filename_id = 'Complete_TAVG_LatLong1.nc'
        filename_extracted = 'Complete_TAVG_LatLong1.nc'
        dir_extracted_data = params.DIR_INTERMEDIATE_OBSERVATION_DATA
        need_to_extract = False
    elif file_to_download == 'Files_for_Testing':
        # file link to view: https://drive.google.com/open?id=1M5IoOgRVOMjC4O-lJO3WXlrkdR1OhPKX
        file_id = '1M5IoOgRVOMjC4O-lJO3WXlrkdR1OhPKX'
        filename_id = 'files_for_testing.tar.gz'
        filename_extracted = 'files_for_testing'
        dir_extracted_data = params.DIR_DATA
        need_to_extract = True

    download_data(dir_google_drive_permissions,
                  dir_extracted_data,
                  file_id,
                  filename_id,
                  filename_extracted,
                  need_to_extract,
                  print_statements_on)


if __name__ == '__main__':
    download_data_predefined('Processed_Data', print_statements_on)
    download_data_predefined('Raw_Historical_Obs', print_statements_on)
    download_data_predefined('Files_for_Testing', print_statements_on)
