import json
import os
import shutil
from collections import Counter
from datetime import datetime

WCAG_MAPPING = {
    "Tagged PDF": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Structure"
        }
    ],
    "Logical Reading Order": [
        {
            "wcag": "1.3.2",
            "name": "Meaningful Sequence",
            "level": "A",
            "impact": "High",
            "category": "Structure"
        }
    ],
    "Title": [
        {
            "wcag": "2.4.2",
            "name": "Page Titled",
            "level": "A",
            "impact": "Medium",
            "category": "Navigation"
        }
    ],
    "Color contrast": [
        {
            "wcag": "1.4.3",
            "name": "Contrast (Minimum)",
            "level": "AA",
            "impact": "High",
            "category": "Visual"
        }
    ],
    "Tagged form fields": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Forms"
        },
        {
            "wcag": "4.1.2",
            "name": "Name, Role, Value",
            "level": "A",
            "impact": "High",
            "category": "Forms"
        }
    ],
    "Field descriptions": [
        {
            "wcag": "3.3.2",
            "name": "Labels or Instructions",
            "level": "A",
            "impact": "High",
            "category": "Forms"
        }
    ],
    "Figures alternate text": [
        {
            "wcag": "1.1.1",
            "name": "Non-text Content",
            "level": "A",
            "impact": "High",
            "category": "Images"
        }
    ],
    "Other elements alternate text": [
        {
            "wcag": "1.1.1",
            "name": "Non-text Content",
            "level": "A",
            "impact": "High",
            "category": "Images"
        }
    ],
    "Tables": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Tables"
        }
    ],
    "Headers": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Tables"
        }
    ],
    "List items": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "Medium",
            "category": "Lists"
        }
    ],
    "Appropriate nesting": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Headings"
        }
    ],
    "Tab order": [
        {
            "wcag": "2.4.3",
            "name": "Focus Order",
            "level": "A",
            "impact": "High",
            "category": "Navigation"
        }
    ],
    "Primary language": [
        {
            "wcag": "3.1.1",
            "name": "Language of Page",
            "level": "A",
            "impact": "Medium",
            "category": "Language"
        }
    ],
    "Character encoding": [
        {
            "wcag": "4.1.1",
            "name": "Parsing",
            "level": "A",
            "impact": "Low",
            "category": "Technical"
        }
    ],

    # Additional mappings required by the failing rules returned by Adobe.
    "Tagged content": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Structure"
        }
    ],
    "Tagged annotations": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Structure"
        }
    ],
    "Nested alternate text": [
        {
            "wcag": "1.1.1",
            "name": "Non-text Content",
            "level": "A",
            "impact": "High",
            "category": "Images"
        }
    ],
    "Associated with content": [
        {
            "wcag": "1.1.1",
            "name": "Non-text Content",
            "level": "A",
            "impact": "High",
            "category": "Images"
        }
    ],
    "Hides annotation": [
        {
            "wcag": "1.1.1",
            "name": "Non-text Content",
            "level": "A",
            "impact": "High",
            "category": "Images"
        }
    ],
    "Rows": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Tables"
        }
    ],
    "TH and TD": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Tables"
        }
    ],
    "Regularity": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "High",
            "category": "Tables"
        }
    ],
    "Summary": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "Medium",
            "category": "Tables"
        }
    ],
    "Lbl and LBody": [
        {
            "wcag": "1.3.1",
            "name": "Info and Relationships",
            "level": "A",
            "impact": "Medium",
            "category": "Lists"
        }
    ]
}

RECOMMENDATIONS = {
    "Tagged PDF": {
        "issue": "Document is not tagged",
        "fix": [
            "Open PDF in Adobe Acrobat Pro",
            "Go to Tools → Accessibility → Auto-tag Document",
            "Review tags manually in Tags panel"
        ],
        "priority": "High",
        "automation_possible": True
    },

    "Logical Reading Order": {
        "issue": "Incorrect reading order",
        "fix": [
            "Open Reading Order tool in Acrobat",
            "Rearrange elements in correct sequence",
            "Verify using screen reader (NVDA/JAWS)"
        ],
        "priority": "High",
        "automation_possible": False
    },

    "Title": {
        "issue": "Missing or incorrect document title",
        "fix": [
            "Go to File → Properties",
            "Add meaningful title in Title field",
            "Enable 'Show Title in Title Bar'"
        ],
        "priority": "Medium",
        "automation_possible": True
    },

    "Color contrast": {
        "issue": "Insufficient color contrast",
        "fix": [
            "Ensure contrast ratio is at least 4.5:1",
            "Use tools like WebAIM Contrast Checker",
            "Adjust text/background colors"
        ],
        "priority": "High",
        "automation_possible": False
    },

    "Tagged form fields": {
        "issue": "Form fields are not properly tagged",
        "fix": [
            "Use Prepare Form tool in Acrobat",
            "Ensure each field has correct tag structure",
            "Verify using accessibility checker"
        ],
        "priority": "High",
        "automation_possible": "Partial"
    },

    "Field descriptions": {
        "issue": "Missing labels/tooltips in form fields",
        "fix": [
            "Open form field properties",
            "Add tooltip/description",
            "Ensure label is programmatically associated"
        ],
        "priority": "High",
        "automation_possible": False
    },

    "Figures alternate text": {
        "issue": "Images missing alt text",
        "fix": [
            "Right-click image → Properties",
            "Add meaningful alternate text",
            "Mark decorative images as artifacts"
        ],
        "priority": "High",
        "automation_possible": "Partial"
    },

    "Other elements alternate text": {
        "issue": "Non-text elements missing alt text",
        "fix": [
            "Identify charts/diagrams",
            "Add descriptive alt text",
            "Ensure association with content"
        ],
        "priority": "High",
        "automation_possible": "Partial"
    },

    "Tables": {
        "issue": "Improper table structure",
        "fix": [
            "Ensure TR → TH/TD hierarchy",
            "Define header rows/columns",
            "Use Table Editor in Acrobat"
        ],
        "priority": "High",
        "automation_possible": False
    },

    "Headers": {
        "issue": "Missing table headers",
        "fix": [
            "Mark header cells as TH",
            "Associate headers with data cells",
            "Validate using accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },

    "List items": {
        "issue": "Improper list structure",
        "fix": [
            "Ensure L → LI → Lbl/LBody structure",
            "Fix nesting in tags panel"
        ],
        "priority": "Medium",
        "automation_possible": False
    },

    "Appropriate nesting": {
        "issue": "Incorrect heading hierarchy",
        "fix": [
            "Ensure headings follow logical order (H1 → H2 → H3)",
            "Avoid skipping levels",
            "Fix in Tags panel"
        ],
        "priority": "High",
        "automation_possible": False
    },

    "Tab order": {
        "issue": "Incorrect tab navigation order",
        "fix": [
            "Open Page Thumbnails → Page Properties",
            "Set tab order to 'Use Document Structure'",
            "Verify manually using keyboard navigation"
        ],
        "priority": "High",
        "automation_possible": True
    },

    "Primary language": {
        "issue": "Document language not specified",
        "fix": [
            "Go to File → Properties → Advanced",
            "Set correct language (e.g., English)",
            "Ensure consistency across document"
        ],
        "priority": "Medium",
        "automation_possible": True
    },

    "Tagged content": {
        "issue": "Page content is not properly exposed through PDF tags",
        "fix": [
            "Open the Tags panel in Adobe Acrobat Pro",
            "Verify meaningful content items are tagged (and not incorrectly marked as artifacts)",
            "Repair structure by re-tagging content where needed",
            "Re-run the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Tagged annotations": {
        "issue": "Annotations are not properly represented for assistive technologies",
        "fix": [
            "In the Tags panel, locate annotation-related tags",
            "Ensure annotations are tagged correctly and are not just artifacts",
            "Edit annotation properties to ensure assistive-tech readable labels/structure",
            "Re-run the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Nested alternate text": {
        "issue": "Alternate text is nested in a way that will not be read",
        "fix": [
            "Open the Tags panel and identify the element with the alternate text",
            "Remove or clear alternate text on nested elements that are never read",
            "Set alternate text on the correct parent element that represents the visual",
            "Re-run the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Associated with content": {
        "issue": "Alternate text is not correctly associated with the visual it describes",
        "fix": [
            "In Tags panel, select the tagged visual element",
            "Use Properties to edit/set the alternate text on that element",
            "Ensure the element is in the correct reading order/structure",
            "Re-run the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Hides annotation": {
        "issue": "Alternate text is configured in a way that hides the annotation/associated content",
        "fix": [
            "Check the tag structure around the annotation and the element that has alternate text",
            "Ensure alternate text is not set on an element that hides the annotation",
            "Edit the annotation/element properties to restore correct visibility and accessibility",
            "Re-run the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Rows": {
        "issue": "Table rows are incorrectly placed in the structure tree",
        "fix": [
            "Open Tags panel and confirm TR elements are children of Table, THead, TBody, or TFoot",
            "Re-parent/move mis-nested TR elements under the correct parent",
            "Validate after changes with the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "TH and TD": {
        "issue": "Table header/data cells are incorrectly placed under TR",
        "fix": [
            "In the Tags panel, ensure TH/TD elements are children of TR",
            "Re-parent mis-nested TH/TD cells so headers/data align with the correct rows",
            "Validate after changes with the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Regularity": {
        "issue": "Table structure is inconsistent (uneven columns/rows across the table)",
        "fix": [
            "Rebuild the table structure so each row contains the same number of cells/columns",
            "Use the Table Editor in Acrobat to correct the structure consistently",
            "Validate after changes with the accessibility checker"
        ],
        "priority": "High",
        "automation_possible": False
    },
    "Summary": {
        "issue": "Complex table is missing a summary",
        "fix": [
            "Add a table summary describing the purpose of the table and how it should be understood",
            "If Acrobat provides a summary field, use it; otherwise ensure summary text is programmatically associated with the table",
            "Re-run the accessibility checker"
        ],
        "priority": "Medium",
        "automation_possible": False
    },
    "Lbl and LBody": {
        "issue": "List label and list body are incorrectly nested in tags",
        "fix": [
            "Open the Tags panel and confirm the correct structure: L → LI → Lbl/LBody",
            "Move/re-tag elements so label and body are children of the correct LI",
            "Validate after changes with the accessibility checker"
        ],
        "priority": "Medium",
        "automation_possible": False
    },

    "Character encoding": {
        "issue": "Improper encoding",
        "fix": [
            "Ensure Unicode encoding is used",
            "Recreate text if encoding is broken"
        ],
        "priority": "Low",
        "automation_possible": False
    }
}

def get_recommendation(rule):
    return RECOMMENDATIONS.get(rule, {
        "issue": "Unknown accessibility issue",
        "fix": ["Review manually as per WCAG guidelines"],
        "priority": "Medium",
        "automation_possible": False
    })


def safe_number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_impact(impact_value):
    if not impact_value:
        return "Unknown"

    impact = str(impact_value).strip().lower()
    if impact in ("high", "critical"):
        return "High"
    if impact == "medium":
        return "Medium"
    if impact == "low":
        return "Low"
    return "Unknown"


def dedupe_issues(issues):
    """
    Deduplicate issue objects so effort-band calculations don't double-count.
    """
    unique = {}
    for issue in issues:
        if not isinstance(issue, dict):
            continue

        key = (
            issue.get("rule", ""),
            issue.get("category", ""),
            issue.get("wcag", ""),
            issue.get("impact", ""),
            str(issue.get("status", "")),
        )
        if key not in unique:
            unique[key] = issue

    return list(unique.values())


def calculate_effort_category(unique_failed_issues, high_count, medium_count, low_count, manual_checks, score):
    """
    Map effort into the subfolder names requested by the user.
    - Small   -> simple
    - Medium  -> medium
    - Large   -> complex
    """
    weighted_score = (high_count * 3) + (medium_count * 2) + low_count + manual_checks

    if unique_failed_issues == 0 and manual_checks == 0 and score >= 95:
        return "simple"
    if weighted_score <= 10:
        return "simple"
    if weighted_score <= 24:
        return "medium"
    return "complex"


def detect_pdf_has_forms(input_json):
    """
    Detect whether the document has form fields based on Adobe's "Forms" section.
    """
    detailed = input_json.get("Detailed Report", {}) or {}
    forms = detailed.get("Forms") or []

    if not isinstance(forms, list) or not forms:
        return False

    known_form_rules = {"Tagged form fields", "Field descriptions"}
    for item in forms:
        if not isinstance(item, dict):
            continue
        if item.get("Rule") in known_form_rules:
            return True

    return False


def detect_pdf_is_image_only(input_json):
    """
    Detect image-only PDFs based on Adobe's "Image-only PDF" rule in the "Document" section.
    """
    detailed = input_json.get("Detailed Report", {}) or {}
    document_items = detailed.get("Document") or []

    if not isinstance(document_items, list) or not document_items:
        return False

    for item in document_items:
        if not isinstance(item, dict):
            continue
        if item.get("Rule") != "Image-only PDF":
            continue

        status = str(item.get("Status", "")).strip().lower()
        # Adobe reports "Passed" when it is NOT image-only.
        return status != "passed"

    return False


def classify_pdf_folder(input_json, processed_output):
    """
    Returns:
      (top_category, effort_subfolder)

    Required folder categories (mutually exclusive):
      1) PDFforms (takes precedence over image-only)
      2) PDF with images (image-only PDFs)
      3) Pdf (everything else)
    """
    if detect_pdf_has_forms(input_json):
        top_category = "PDFforms"
    elif detect_pdf_is_image_only(input_json):
        top_category = "PDF with images"
    else:
        top_category = "Pdf"

    issues = processed_output.get("issues", []) or []
    deduped = dedupe_issues(issues)
    unique_failed_issues = len(deduped)

    high_count = sum(1 for i in deduped if normalize_impact(i.get("impact")) == "High")
    medium_count = sum(1 for i in deduped if normalize_impact(i.get("impact")) == "Medium")
    low_count = sum(1 for i in deduped if normalize_impact(i.get("impact")) == "Low")

    manual_checks = int(safe_number(processed_output.get("summary", {}).get("manual_check", 0), 0))
    score = safe_number(processed_output.get("score", 0), 0)

    effort_subfolder = calculate_effort_category(
        unique_failed_issues=unique_failed_issues,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count,
        manual_checks=manual_checks,
        score=score,
    )

    return top_category, effort_subfolder

def validate_metadata():
    # You should replace this with actual PDF metadata extraction
    metadata = {
        "title": False,
        "author": False,
        "subject": False,
        "keywords": False,
        "language": True
    }

    missing = [k for k, v in metadata.items() if not v]

    return {
        "status": "Failed" if missing else "Passed",
        "missing_fields": missing
    }

def process_accessibility_report(input_json, document_name):
    summary = input_json.get("Summary", {})
    detailed = input_json.get("Detailed Report", {})

    total_failed = summary.get("Failed", 0)
    total_passed = summary.get("Passed", 0)
    manual_checks = summary.get("Needs manual check", 0)

    issues = []
    manual_review = []

    # Iterate all categories
    for category, rules in detailed.items():
        for rule in rules:
            rule_name = rule["Rule"]
            status = rule["Status"]

            wcag_list = WCAG_MAPPING.get(rule_name, [])

            # If no mapping found
            if not wcag_list:
                wcag_list = [{
                    "wcag": "Unknown",
                    "name": "Unknown",
                    "level": "Unknown",
                    "impact": "Medium",
                    "category": "General"
                }]

            for wcag in wcag_list:
                issue = {
                    "rule": rule_name,
                    "category": category,
                    "status": status,
                    "wcag": wcag["wcag"],
                    "wcag_name": wcag["name"],
                    "wcag_level": wcag["level"],
                    "impact": wcag["impact"],
                    "recommendation": get_recommendation(rule_name)
                }

                if status == "Failed":
                    issues.append(issue)

                elif status == "Needs manual check":
                    manual_review.append(issue)

            if status == "Needs manual check":
                manual_review.append(rule_name)

            if status == "Failed":
                issues.append(issue)

    # Metadata validation
    metadata_result = validate_metadata()

    # Final decision logic
    if total_failed > 0:
        overall_status = "FAIL"
    elif manual_checks > 0:
        overall_status = "REVIEW REQUIRED"
    else:
        overall_status = "PASS"

    score = round((total_passed / (total_passed + total_failed + manual_checks)) * 100, 2)

    # Final structured output
    output = {
        "document_name": document_name,
        "wcag_version": "2.2",
        "compliance_level": "AA",
        "overall_status": overall_status,
        "score": score,
        "summary": {
            "passed": total_passed,
            "failed": total_failed,
            "manual_check": manual_checks
        },
        "issues": issues,
        "manual_review_required": manual_review,
        "timestamp": datetime.utcnow().isoformat()
    }

    return output


def process_all_adobe_outputs(input_folder="Adobe_API_Output", output_folder="Final_reports"):
    os.makedirs(output_folder, exist_ok=True)

    if not os.path.isdir(input_folder):
        print(f"Input folder not found: {input_folder}")
        return

    pdf_input_folder = "Input_reports"
    categorized_output_folder = "Categorized_PDFs"
    folder_counts = Counter()
    pdf_stem_to_path = {}

    # Create requested folder structure up-front.
    for top_category in ["Pdf", "PDFforms", "PDF with images"]:
        for effort_subfolder in ["simple", "medium", "complex"]:
            os.makedirs(
                os.path.join(categorized_output_folder, top_category, effort_subfolder),
                exist_ok=True,
            )

    if os.path.isdir(pdf_input_folder):
        for pdf_file in os.listdir(pdf_input_folder):
            if not pdf_file.lower().endswith(".pdf"):
                continue
            stem = os.path.splitext(pdf_file)[0].lower()
            # If duplicates exist, keep the first one we encounter.
            pdf_stem_to_path.setdefault(stem, os.path.join(pdf_input_folder, pdf_file))
    else:
        print(f"Warning: PDF input folder not found: {pdf_input_folder}")

    input_files = sorted(
        file_name for file_name in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, file_name)) and file_name.lower().endswith(".json")
    )

    if not input_files:
        print(f"No JSON files found in input folder: {input_folder}")
        return

    for file_name in input_files:
        input_path = os.path.join(input_folder, file_name)
        base_name, _ = os.path.splitext(file_name)
        output_file_name = f"{base_name}_Final_report.json"
        output_path = os.path.join(output_folder, output_file_name)

        with open(input_path, "r", encoding="utf-8") as file:
            adobe_output = json.load(file)

        processed_output = process_accessibility_report(adobe_output, document_name=file_name)
        top_category, effort_subfolder = classify_pdf_folder(adobe_output, processed_output)
        processed_output["distributed_category"] = top_category
        processed_output["distributed_subcategory"] = effort_subfolder
        processed_output["distributed_folder"] = os.path.join(top_category, effort_subfolder)

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(processed_output, file, indent=4)

        print(f"Final report generated: {output_path}")

        # Distribute original PDFs into the requested folders.
        # Assumes the input PDF shares the same basename as the Adobe JSON.
        pdf_path = pdf_stem_to_path.get(base_name.lower())

        if not pdf_path:
            # Fallback: prefix match in case the naming differs slightly.
            base_lower = base_name.lower()
            prefix_matches = [
                p
                for stem, p in pdf_stem_to_path.items()
                if stem.startswith(base_lower) or base_lower.startswith(stem)
            ]
            pdf_path = sorted(prefix_matches)[0] if prefix_matches else None

        if pdf_path and os.path.isfile(pdf_path):
            dest_dir = os.path.join(categorized_output_folder, top_category, effort_subfolder)
            os.makedirs(dest_dir, exist_ok=True)
            dest_path = os.path.join(dest_dir, os.path.basename(pdf_path))
            shutil.copy2(pdf_path, dest_path)
            folder_counts[(top_category, effort_subfolder)] += 1
        else:
            print(f"Warning: missing PDF for '{base_name}': {pdf_path}")

    print("Distribution summary:")
    for top_category in ["Pdf", "PDFforms", "PDF with images"]:
        for effort_subfolder in ["simple", "medium", "complex"]:
            count = folder_counts.get((top_category, effort_subfolder), 0)
            print(f"  {top_category}/{effort_subfolder}: {count}")

if __name__ == "__main__":
    process_all_adobe_outputs()