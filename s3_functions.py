import boto3
from gc import collect
from datetime import datetime
from dotenv import load_dotenv
from os import path, getenv, getcwd
from botocore.exceptions import NoCredentialsError

# Load environment variables
load_dotenv()


class S3:
    """
        This S3 class has the all the s3 related methods for the script. It initiates with the necessary buckets
        and also starts the s3 client(boto3).

        :param:
        __init__(self):
               This initiation method begins with the boto3 client and required buckets.

        latest_file(self):
           This method connects with the bucket where the xml files reside and return the name of the last
           modified file(string).

        check_for_processed_files(self):
            In order not to reprocess files, we use this function to take logs of all processed files.
            It checks its logs each time latest_file() detects a new file to be sure it has not already been processed.

        download_from_aws(self):
            This method will download the xml file from your specified bucket in the .env. It picks up the name
            of the xml file for download after the latest_file() and check_for_processed_files() have confirmed a
            new file is available.

        upload_to_aws(self):
            After the latest xml file has been downloaded and converted to json, this method uploads the json file
            to your preferred s3 bucket location.

    """

    def __init__(self) -> None:
        """
        Initiating the s3 connection with the Access and secret key using boto3
        """

        # Initializations
        self.AWS_ACCESS_KEY = getenv('AWS_ACCESS_KEY')
        self.AWS_SECRET_KEY = getenv('AWS_SECRET_KEY')
        self.AWS_ACCESS_KEY_U = getenv('AWS_ACCESS_KEY_UPLOAD')
        self.AWS_SECRET_KEY_U = getenv('AWS_SECRET_KEY_UPLOAD')
        self.s3_download = boto3.client('s3',
                                        aws_access_key_id=self.AWS_ACCESS_KEY,
                                        aws_secret_access_key=self.AWS_SECRET_KEY)
        self.s3_upload = boto3.client('s3',
                                      aws_access_key_id=self.AWS_ACCESS_KEY_U,
                                      aws_secret_access_key=self.AWS_SECRET_KEY_U)
        self.bucket_xml = getenv('BUCKET_XML')
        self.bucket_json = getenv('BUCKET_JSON')
        pass

    def latest_file(self) -> str:
        """
        Returns the name of the last modified file in the s3 bucket
        """
        all_s3_objects = self.s3_download.list_objects_v2(Bucket=self.bucket_xml)['Contents']

        def get_last_modified(obj):
            return int(obj['LastModified'].strftime('%y'))

        # All objects in the s3 bucket are arranged according to Last Modified
        # This is done after passing the get_last_modified() as key to the s3 objects using the sorted function
        last_modified_file = str([obj['Key'] for obj in sorted(all_s3_objects, key=get_last_modified)][-1])
        return last_modified_file

    def check_for_processed_files(self) -> bool:
        """
        Checks if the file has already been processed if not it is forwarded for processing and logged in a file
        """
        print("Checking for new files...")
        last_modified_file = self.latest_file()

        if path.exists("processed files.txt"):
            # If the log file already exists, starts checking if it has been processed else create a new log and append
            with open('processed files.txt', 'r') as pro_files:
                if last_modified_file not in pro_files.read():
                    with open('processed files.txt', 'a+') as pro_files:
                        pro_files.write(last_modified_file
                                        + " was processed at "
                                        + str(datetime.now())
                                        + '\n')
                        collect()
                        print("New File named", last_modified_file, "has been detected")
                        return True
                else:
                    raise FileExistsError("The latest file has already been processed, Checking will continue")

        else:

            with open('processed files.txt', 'a+') as pro_files:
                print("New Log Created")
                pro_files.write(last_modified_file
                                + " was processed at "
                                + str(datetime.now())
                                + '\n')
                collect()
                print("New File named", last_modified_file, "has been detected")
                return True

    def download_from_aws(self) -> bool:
        """
        Download the XML file from the specified bucket on s3.
        """
        last_modified_file = self.latest_file()

        try:
            print("Starting Download..")
            # The file is downloaded from the bucket and store in the local directory with the same name
            self.s3_download.download_file(self.bucket_xml,
                                           last_modified_file,
                                           last_modified_file)
            print("Download went well")
            return True

        except FileNotFoundError:
            print("Error in downloading s3 file. File requested was not found")
            return False
        except NoCredentialsError:
            print('Credentials not available.')
            return False

    def upload_to_aws(self) -> bool:
        """
        Uploads the final processed file to the specified bucket which is in json.
        """
        last_modified_file = self.latest_file()

        try:
            # Checks the current directory for the name of the processed file and then uploads to the bucket
            local_path = path.abspath(getcwd())
            new_json_file = last_modified_file.replace('.xml', '.json')
            local_file = path.join(local_path,
                                   new_json_file)

            self.s3_upload.upload_file(local_file,
                                       self.bucket_json,
                                       new_json_file,
                                       ExtraArgs={'ACL': 'public-read'})
            print('Upload Successful!')
            return True

        except FileNotFoundError:
            print('The file was not found.')
            return False
        except NoCredentialsError:
            print('Credentials not available.')
            return False
        except RuntimeError:
            print("Error occured during json file upload")
            return False
