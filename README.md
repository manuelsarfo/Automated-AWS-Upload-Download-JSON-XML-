
INTRODUCTION
------------

This module consistently picks new XML files from an s3 bucket and converts them to json format. The location(s3 bucket) of
these XML files is constantly notified of any newly uploaded files depending on the delay as set by the user. All XML
files which are processed are chronologically logged. Any new file detected is rejected if it has already been processed
as by the recorded logs. If the XML has not been processed yet, it is then downloaded and converted to json format.
After conversion, the json file is uploaded to a predefined s3 bucket. All actions are logged in a local file.


 * For a full description of the module, check out the commentary on the source code:
   //s3_functions
   //xmltojson
   //main

 * To submit bug reports and feature suggestions, or track changes:
   manuelampadu@gmail.com



ASSUMPTIONS
------------

For this purpose, it is assumed that:

 * All XML files to be uploaded come with unique names
 * All incoming XML files will use the format of the example XML file .



REQUIREMENTS
------------

This module requires the following modules:

 * boto3
 * xmltodict
 * python-dotenv
 * gc-python-utils



INSTALLATION(DOCKER)
------------

 * This project comes with a dockerfile with a configuration added so run the below commands:

 $ sudo docker build -t scriptimage .

 $ sudo docker run --rm -p 8000:80 scriptimage

 * Initial command will build an image from the dockerfile
 * The second command will run the script on this new image.


CONFIGURATION(.ENV)
-------------

 * Configure the AWS keys and buckets

   - AWS_ACCESS_KEY & AWS_SECRET_KEY

     These are the access and secret keys of the bucket that will contain the XML files.


   - AWS_ACCESS_KEY_UPLOAD & AWS_SECRET_KEY_UPLOAD

     These are the access and secret keys of the bucket that will receive the newly converted json files.


   - BUCKET_XML

     This is the name of the bucket that will receive XML files ready for conversion.


   - BUCKET_JSON

     This is the name of the bucket that will receive json files after they are successfully converted.


 * Configure the delay in checking for new files

  - SLEEPTIME

     How long the script should delay before it checks the BUCKET_XML.
     All values are in seconds and will be converted into a float.



TROUBLESHOOTING
---------------

 * If a file is failing to download/upload, check the following:

   - Is the file/bucket publicly accessible?

   - Does the user accessing this file have the necessary privileges?

   - Log files from this project

 * If the script is failing to run on docker, check the following:

   - Did all modules in the requirements.txt finish installing?

   - Are you accessing the script through a port and is the port exposed in the dockerfile?

   - Did the run function in the dockerfile execute?

* If the script is failing to detect a new file, check the following:

   - Does the file has a unique name than the previous file which have been uploaded?
        - If the filename is the same as a previous file that was uploaded,
          either give the file a unique name or delete the processed log file

   - Is the name of the bucket in the BUCKET_XML accurate?

FAQ
---

Q: I am generating a lot of logs. Is this normal?

A: Yes, this is the intended behavior. The logging level has been set to DEBUG hence, it records all logs.
