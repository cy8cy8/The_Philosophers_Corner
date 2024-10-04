import tkinter as tk
from view import HomePage
from model import data_src, Util
from view_model import ViewModel
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os
import json

class App(tk.Tk):
    def __init__(self, title, min_size) -> None:
        super().__init__()
        self.title(title)
        self.minsize(width=min_size[0], height=min_size[1])
        self.maxsize(width=self.winfo_screenwidth(), height=min_size[1])
        self.geometry(f"{min_size[0]}x{min_size[1]}")

        # Download the JSON file from S3
        self.s3_client = self.get_s3_client()
        with open("aws.json", "r") as f:
            data = json.load(f)
            self.bucket_name = data["bucket_name"]
            self.s3_key = data["s3_key"]
        self.local_json_path = data_src
        self.download_json_from_s3()

        # Initialise Model, ViewModel and View
        model = Util()
        self.viewmodel = ViewModel(model)
        view = HomePage(self, viewmodel=self.viewmodel, bg="black")
        view.pack(fill="both", expand=True)

        # Bind the close even to upload JSON if modified
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def get_s3_client(self):
        try:
            return boto3.Session().client("s3")
        except NoCredentialsError:
            print("No AWS credentials found. Configure your credentials")
        except PartialCredentialsError:
            print("Incomplete AWS credentials found. Check your config")

    def download_json_from_s3(self):
        try:
            self.s3_client.download_file(self.bucket_name, self.s3_key, self.local_json_path)
            print(f"JSON file downloaded successfully from S3 bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error downloading JSON file: {e}")

    def upload_json_to_s3(self):
        try:
            self.s3_client.upload_file(self.local_json_path, self.bucket_name, self.s3_key)
            print(f"JSON file uploaded successfully to from S3 bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error uploading JSON file: {e}")

    def on_close(self):
        # Check if the JSON file was modified
        if self.viewmodel.is_modified:
            self.upload_json_to_s3()
        # Delete the local JSON file
        if os.path.exists(self.local_json_path):
            os.remove(self.local_json_path)
            print("Local JSON file deleted.")
        self.destroy()

if __name__ == "__main__":
    app = App(
        title="The Philosopher's Corner",
        min_size=(800, 800)
    )
    app.mainloop()