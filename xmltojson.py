import xmltodict
import json
from gc import collect

from s3_functions import S3


class Xml2Json(S3):
    """
            This Xml2Json class has the all the related methods to convert an XML file to JSON.
            It initiates with inherited instances from S3.

            :param:
            __init__(self):
               This initiation method inherits the values from S3 and uses super() to initiate the variables of S3.
               It uses the name of the latest file from latest_file() to find the xml file and rename the final json.

            convert_to_json(self):
                XML is converted to json here. The data is stored in json format and written to a file which will
                 be uploaded by upload_to_aws().

        """

    def __init__(self) -> None:
        super().__init__()
        self.last_modified_file = self.latest_file()
        pass

    def convert_to_json(self) -> None:
        try:
            print("conversion has started")
            with open(self.last_modified_file, "r") as xmlfile:
                # Convert xml data to a dictionary object
                data_dict = xmltodict.parse(xmlfile.read())
                collect()

                # creating JSON object using dictionary object and replacing strings
                jsonobj_str = json.dumps(data_dict, indent=2) \
                    .replace('id', 'product_id') \
                    .replace('category', 'product_category') \
                    .replace('description', 'product_description') \
                    .replace('images', 'product_images') \
                    .replace('@', '') \
                    .replace('nsx:', '')

                # Storing json data to json file
                new_json_file = self.last_modified_file.replace('.xml', '.json')
                with open(new_json_file, "w") as jsonfile:
                    jsonfile.write(jsonobj_str)
                    collect()
                    print("XML File conversion has completed")
        except Exception as e:
            print("Error: ", e, "occured during file conversion")
