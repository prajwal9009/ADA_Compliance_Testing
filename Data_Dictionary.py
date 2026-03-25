import os
import re
from pdfrw import PdfReader
import pandas as pd


PDF_FILES = [
    "CCCH0627.pdf",
    "CCP1010.pdf"
]

OUTPUT_FILE = "Generated_Data_Dictionary.xlsx"

def clean_field_name(field):
    """Clean raw PDF field name"""
    if not field:
        return ""
    name = field.strip("()")
    return name


def infer_field_type(ft):
    """Map PDF field type to readable type"""
    mapping = {
        "/Tx": "Text",
        "/Btn": "Checkbox/Radio",
        "/Ch": "Dropdown",
        "/Sig": "Signature"
    }
    return mapping.get(ft, "Unknown")


def infer_required(field_name):
    """Basic heuristic for required fields"""
    keywords = ["name", "case", "date", "email", "phone"]
    for k in keywords:
        if k.lower() in field_name.lower():
            return "Yes"
    return "Unknown"


def generate_label(field_name):
    """Convert technical name to human-readable label"""
    # Remove prefixes like "1-", "2-"
    field_name = re.sub(r'^\d+-', '', field_name)

    # Replace camelCase / underscores
    field_name = field_name.replace("_", " ")
    field_name = re.sub(r'([a-z])([A-Z])', r'\1 \2', field_name)

    return field_name.title()


def extract_fields_from_pdf(pdf_path):
    pdf = PdfReader(pdf_path)
    fields_data = []

    for page in pdf.pages:
        annotations = page.Annots
        if annotations:
            for annot in annotations:
                if annot.T:
                    raw_name = annot.T.to_unicode()
                    field_name = clean_field_name(raw_name)

                    field_type = infer_field_type(annot.FT)
                    required = infer_required(field_name)
                    label = generate_label(field_name)

                    fields_data.append({
                        "Field ID": field_name,
                        "Field Name": field_name,
                        "Label": label,
                        "Data Type": field_type,
                        "Required": required,
                        "Default Value": get_safe_value(annot.V),
                        "Validation Rules": "",
                        "Description": "",
                        "Section": "",
                        "Source Form": os.path.basename(pdf_path)
                    })

    return fields_data

def get_safe_value(val):
    if not val:
        return ""

    try:
        if hasattr(val, "to_unicode"):
            return val.to_unicode()
        return str(val).replace("/", "")
    except:
        return str(val)


def generate_data_dictionary(pdf_files):
    all_fields = []

    for pdf in pdf_files:
        print(f"Processing: {pdf}")
        fields = extract_fields_from_pdf(pdf)
        all_fields.extend(fields)

    df = pd.DataFrame(all_fields)

    # Remove duplicates
    df = df.drop_duplicates(subset=["Field ID", "Source Form"])

    # Sort
    df = df.sort_values(by=["Source Form", "Field ID"])

    # Export
    df.to_excel(OUTPUT_FILE, index=False)

    print(f"\n✅ Data Dictionary Generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data_dictionary(["C:/Users/V4 INFO/Downloads/ADA/CCCH0627.pdf",r"C:/Users/V4 INFO/Downloads/ADA/CCP1010.pdf"])