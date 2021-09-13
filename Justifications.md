JUSTIFICATION
------------

Below are some justifications to my choices of module/logic in the source code :

 * The use of xmltodict library:
   xmltodict is used to parse the given XML input and convert it into a dictionary.
   It is usually converted to Badgerfish Convention of JSON and so 'replace' is used to remove '@'
   which is added in child elements to prevent a collision.

 * Use of the check_for_processed_files():
   This is method was made to prevent the reprocessing of files.
   It creates a log file and appends every processed file name in it.
   The log file is read anytime a new file is detected.
   This method goes through the log file to be sure the script has not already processed that file.
   This works with the assumption that all XML files to be dropped in the bucket have unique names.

 * In-built logging library:
   This library is used to write logs for each event and also catch errors with details.
    It also helps to trace all information been exchanged by the script and external APIs.

 * Utilization of latest_file():
   To pick up the last modified file in the bucket, this method is necessary.
   After getting all the contents of all items in a bucket, the 'sorted' function is used.
   This in-built function is given a dictionary from the list of all items in a bucket and the last modified function.
   The lastmodified function then sorts all items in chronological order and hence the last item is chosen as the
   last modified.
