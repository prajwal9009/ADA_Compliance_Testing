import json
import os
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

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(processed_output, file, indent=4)

        print(f"Final report generated: {output_path}")

if __name__ == "__main__":
    process_all_adobe_outputs()