import time
import logging
from os import getenv
from botocore.exceptions import NoCredentialsError

from s3_functions import S3
from xmltojson import Xml2Json

# Creating objects from imported classes
s3_module = S3()
xml2json = Xml2Json()

# Adding logging capability which will save to a local file(process.log)
logging.basicConfig(filename='process.log',
                    filemode='a+',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.DEBUG)


def process():
    """
            When this script is invoked, it starts this method which keeps checking the specified bucket for new files.
            If new files are found, it picks them up and convert them to json from xml.
            Finally, the json product is uploaded to a specified bucket by the user.

            :param:
            It requires no parameters


            :return:

            Returns a NoneType

            """
    while True:

        # Starts script by checking for new files in the bucket
        try:
            time.sleep(float(getenv('SLEEPTIME')))

            s3_module.check_for_processed_files()
            logging.info("New file detected")

        except FileExistsError:
            logging.exception("No new file to be processed")
        except KeyboardInterrupt:
            logging.exception("A user terminated the script")
            print("Interrupted by user!")
            break

        else:

            # If a new xml file exist, download it from the bucket
            try:
                s3_module.download_from_aws()
                logging.info("XML File Download completed")

            except FileNotFoundError:
                logging.exception("File could not be downloaded")
            except NoCredentialsError:
                logging.exception("Client error")
            except KeyboardInterrupt:
                logging.exception("A user terminated the script")
                print("Interrupted by user!")
                break

            else:

                # If the new xml file has been downloaded succesfully, convert to json
                try:
                    xml2json.convert_to_json()
                    logging.info("XML file has successfully converted to json")

                except Exception as e:
                    logging.exception(e)
                except KeyboardInterrupt:
                    logging.exception("A user terminated the script")
                    print("Interrupted by user!")
                    break

                else:

                    # After a successful conversion, upload to the given bucket to store the json file
                    try:
                        s3_module.upload_to_aws()
                        logging.info("Upload Completed")

                    except Exception as e:
                        logging.exception(e)
                    except KeyboardInterrupt:
                        logging.exception("A user terminated the script")
                        print("Interrupted by user!")
                        break


if __name__ == '__main__':
    process()
