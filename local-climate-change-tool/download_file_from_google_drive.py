import io
import tarfile
import os
import oauth2client
import googleapiclient.discovery as discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.http import MediaIoBaseDownload
import sys

cwd = os.getcwd()
WORKING_DIR = cwd+'phase1_data_wrangler/'
sys.path.insert(0, WORKING_DIR)
import analysis_parameters as params

def get_credentials(permissions_dir):
    obj = lambda: None
    lmao = {"auth_host_name":'localhost', 'noauth_local_webserver':'store_true', 'auth_host_port':[8080, 8090], 'logging_level':'ERROR'}
    for k, v in lmao.items():
        setattr(obj, k, v)
        
    # authorization boilerplate code
    SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
    store = file.Storage(permissions_dir+'token.json')
    creds = store.get()
    
    # The following will give you a link if token.json does not exist, the link allows the user to give this app permission
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(permissions_dir+'client_id.json', SCOPES)
        creds = tools.run_flow(flow, store, obj)
    return creds

def download_file(file_id, filename_id, creds):
    DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))
    
    request = DRIVE.files().get_media(fileId=file_id)
    fh = io.FileIO(filename_id, mode='w')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
        
def extract_files(filename_id, dir_extracted_data):
    tf = tarfile.open(filename_id)
    tf.extractall(path=dir_extracted_data)
    
def remove_extracted_files(dir_extracted_data, filename_extracted):
    os.system('rm -rf '+dir_extracted_data+filename_extracted)
    
def remove_compressed_file(filename_compressed):
    os.system('rm -rf '+filename_compressed)
    
def move_file(filename_id, dir_extracted_data):
    os.system('mv '+filename_id+' '+dir_extracted_data+filename_id)
    
def download_data(dir_google_drive_permissions,
                  dir_extracted_data,
                  file_id,
                  filename_id,
                  filename_extracted,
                  need_to_extract,
                  print_statements_on=True):
    if print_statements_on:
        print(' -> getting credentials')
    creds = get_credentials(permissions_dir=dir_google_drive_permissions)
    
    if print_statements_on:
        print(' -> downloading files')
    download_file(file_id, filename_id, creds)
    
    if need_to_extract:
        if print_statements_on:
            print(' -> removing any files already existing in folder where extracted files is going')
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
    dir_google_drive_permissions = params.DIR_GOOGLE_DRIVE_PERMISSIONS
    if file_to_download=='Processed_Data':
        #file link to view: https://drive.google.com/open?id=1EG9ZzuoaG4z3KuYubdspTV8S8skTFMzE
        file_id = '1EG9ZzuoaG4z3KuYubdspTV8S8skTFMzE'
        filename_id = 'processed_data.tar.gz'
        filename_extracted = 'processed_data'
        dir_extracted_data = params.DATA
        need_to_extract = True
    elif file_to_download=='Raw_Historical_Obs':
        #file link to view: https://drive.google.com/open?id=1J3lpNptF2PxLRCJxJVJkDpd4ndyDKp8j
        file_id = '1J3lpNptF2PxLRCJxJVJkDpd4ndyDKp8j'
        filename_id = 'Complete_TAVG_LatLong1.nc'
        filename_extracted = 'Complete_TAVG_LatLong1.nc'
        dir_extracted_data = params.DIR_INTERMEDIATE_OBSERVATION_DATA
        need_to_extract = False

    download_data(dir_google_drive_permissions,
                  dir_extracted_data,
                  file_id,
                  filename_id,
                  filename_extracted,
                  need_to_extract,
                  print_statements_on)
