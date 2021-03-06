from io import StringIO
from os import remove

from boto3 import resource

from utils.logger import App_Logger


class S3_Operation:
    """
    Description :   This method is used for all the S3 bucket operations
    Written by  :   iNeuron Intelligence
    
    Version     :   1.2
    Revisions   :   Moved to setup to cloud 
    """

    def __init__(self):
        self.s3_resource = resource("s3")

        self.class_name = self.__class__.__name__

        self.log_writer = App_Logger()

    def get_bucket(self, bucket: str, log_file: str):
        """
        Method Name :   get_bucket
        Description :   This method gets the bucket from s3 
        Output      :   A s3 bucket name is returned based on the bucket
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_bucket.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            bucket = self.s3_resource.Bucket(bucket)

            self.log_writer.log(f"Got {bucket} bucket", log_file)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return bucket

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def get_file_object(self, fname: str, bucket: str, log_file: str):
        """
        Method Name :   get_file_object
        Description :   This method gets the file object from s3 bucket
        
        Output      :   A file object is returned
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.get_file_object.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            bucket = self.get_bucket(bucket, log_file)

            lst_objs = [object for object in bucket.objects.filter(Prefix=fname)]

            self.log_writer.log(f"Got {fname} from bucket {bucket}", log_file)

            func = lambda x: x[0] if len(x) == 1 else x

            file_objs = func(lst_objs)

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return file_objs

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def read_object(
        self, object, log_file: str, decode: bool = True, make_readable: bool = False,
    ):
        """
        Method Name :   read_object
        Description :   This method reads the object with kwargs
        Output      :   A object is read with kwargs
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.read_object.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            func = (
                lambda: object.get()["Body"].read().decode()
                if decode is True
                else object.get()["Body"].read()
            )

            self.log_writer.log(f"Read the s3 object with decode as {decode}", log_file)

            conv_func = lambda: StringIO(func()) if make_readable is True else func()

            self.log_writer.log(
                f"Read the s3 object with make_readable as {make_readable}", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return conv_func()

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def read_yaml_as_str(self, fname: str, bucket: str, log_file: str):
        """
        Method Name :   read_yaml_as_str
        Description :   This method reads the yaml file from bucket
        
        Output      :   A yaml file is read 
        On Failure  :   Write an exception log and then raise an exception
        
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.read_yaml_as_str.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            yaml_obj = self.get_file_object(fname, bucket, log_file)

            content = self.read_object(yaml_obj, log_file)

            self.log_writer.log(
                f"Read {fname} from {bucket} bucket as string content", log_file
            )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

            return content

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)

    def upload_file(
        self,
        from_fname: str,
        to_fname: str,
        bucket: str,
        log_file: str,
        delete: bool = True,
    ):
        """
        Method Name :   upload_file
        Description :   This method uploades a file to s3 bucket with kwargs
        Output      :   A file is uploaded to s3 bucket
        On Failure  :   Write an exception log and then raise an exception
        Version     :   1.2
        Revisions   :   moved setup to cloud
        """
        method_name = self.upload_file.__name__

        self.log_writer.start_log("start", self.class_name, method_name, log_file)

        try:
            self.log_writer.log(
                f"Uploading {from_fname} to s3 bucket {bucket}", log_file
            )

            self.s3_resource.meta.client.upload_file(from_fname, bucket, to_fname)

            self.log_writer.log(
                f"Uploaded {from_fname} to s3 bucket {bucket}", log_file
            )

            if delete is True:
                self.log_writer.log(
                    f"Option delete is set {delete}..deleting the file",
                )

                remove(from_fname)

                self.log_writer.log(f"Removed the local copy of {from_fname}", log_file)

            else:
                self.log_writer.log(
                    f"Option delete is set {delete}, not deleting the file", log_file
                )

            self.log_writer.start_log("exit", self.class_name, method_name, log_file)

        except Exception as e:
            self.log_writer.exception_log(e, self.class_name, method_name, log_file)