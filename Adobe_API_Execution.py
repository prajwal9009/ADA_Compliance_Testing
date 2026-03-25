"""
 Copyright 2024 Adobe
 All Rights Reserved.
 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import logging
import os

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.pdf_accessibility_checker_job import PDFAccessibilityCheckerJob
from adobe.pdfservices.operation.pdfjobs.result.pdf_accessibility_checker_result import PDFAccessibilityCheckerResult

# Initialize the logger
logging.basicConfig(level=logging.INFO)


class PDFAccessibilityChecker:
    def __init__(self):
        self.input_folder = "Input_reports"
        self.output_folder = "Adobe_API_Output"
        os.makedirs(self.output_folder, exist_ok=True)

        # Initial setup, create credentials instance
        credentials = ServicePrincipalCredentials(
            client_id="<ID Here>.",
            client_secret="<Secret Here>"
        )

        # Reuse one PDF Services client for all files
        self.pdf_services = PDFServices(credentials=credentials)

        self.process_all_input_files()

    def process_all_input_files(self) -> None:
        if not os.path.isdir(self.input_folder):
            logging.error("Input folder not found: %s", self.input_folder)
            return

        input_files = sorted(
            [
                file_name for file_name in os.listdir(self.input_folder)
                if os.path.isfile(os.path.join(self.input_folder, file_name))
            ]
        )

        if not input_files:
            logging.info("No files found in input folder: %s", self.input_folder)
            return

        for file_name in input_files:
            input_file_path = os.path.join(self.input_folder, file_name)
            try:
                self.process_single_file(input_file_path)
                logging.info("Processed file: %s", file_name)
            except (ServiceApiException, ServiceUsageException, SdkException) as e:
                logging.exception("Adobe API error for '%s': %s", file_name, e)
            except Exception as e:
                logging.exception("Unexpected error for '%s': %s", file_name, e)

    def process_single_file(self, input_file_path: str) -> None:
        with open(input_file_path, "rb") as pdf_file:
            input_stream = pdf_file.read()

        input_asset = self.pdf_services.upload(
            input_stream=input_stream,
            mime_type=PDFServicesMediaType.PDF
        )
        pdf_accessibility_checker_job = PDFAccessibilityCheckerJob(input_asset=input_asset)

        location = self.pdf_services.submit(pdf_accessibility_checker_job)
        pdf_services_response = self.pdf_services.get_job_result(location, PDFAccessibilityCheckerResult)

        report_asset = pdf_services_response.get_result().get_report()
        stream_report = self.pdf_services.get_content(report_asset)

        output_json_file_path = self.create_json_output_file_path(input_file_path)
        with open(output_json_file_path, "wb") as file:
            file.write(stream_report.get_input_stream())

    def create_json_output_file_path(self, input_file_path: str) -> str:
        input_file_name = os.path.basename(input_file_path)
        base_name, _ = os.path.splitext(input_file_name)
        return os.path.join(self.output_folder, f"{base_name}.json")


if __name__ == "__main__":
    PDFAccessibilityChecker()