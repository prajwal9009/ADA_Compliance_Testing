# ADA_Compliance_Testing

## Execution Commands

Run the scripts in the order below. Each command is used for a specific stage in the ADA compliance pipeline.

1. `python Adobe_API_Execution.py`  
   Use this to process input PDFs through the Adobe API workflow and generate intermediate analysis outputs required by downstream steps.

2. `python Business_logic_implementation.py`  
   Use this to apply project-specific business rules and transform API output into structured compliance-ready data.

3. `python Json_Final_Reports_To_Excel.py -i "Final_reports" -o "Final_report_excels"`  
   Use this to convert final JSON report files from `Final_reports` into Excel files in `Final_report_excels` for easier review and sharing.

4. `python Final_Report_Excel_Analysis.py`  
   Use this to run post-processing and analysis on generated final report Excel files.

5. `python Data_Dictionary.py`  
   Use this to generate data dictionary Excel files from PDFs in `Input_reports`, with output written to `data Dictionary`.