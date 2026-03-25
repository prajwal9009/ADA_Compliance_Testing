import json
import pandas as pd

input_file = "final_report.json"
output_file = "accessibility_report_1.xlsx"

with open(input_file, "r", encoding="utf-8") as f:
    data = json.load(f)

summary_data = data.get("summary", {})

summary_df = pd.DataFrame([
    {"Metric": key, "Value": value}
    for key, value in summary_data.items()
])

issues = data.get("issues", [])

detailed_rows = []
for item in issues:
    detailed_rows.append({
        "Rule": item.get("rule"),
        "Category": item.get("category"),
        "Status": item.get("status"),
        "WCAG": item.get("wcag"),
        "Impact": item.get("impact"),
        "Issue": item.get("recommendation", {}).get("issue"),
        "Fix": " | ".join(item.get("recommendation", {}).get("fix", [])),
        "Priority": item.get("recommendation", {}).get("priority")
    })

detailed_df = pd.DataFrame(detailed_rows)

failures_df = detailed_df[detailed_df["Status"] == "Failed"]

manual_items = data.get("manual_review_required", [])

manual_rows = []
for item in manual_items:
    if isinstance(item, dict):  # ignore stray strings
        manual_rows.append({
            "Rule": item.get("rule"),
            "Category": item.get("category"),
            "Status": item.get("status"),
            "WCAG": item.get("wcag"),
            "Impact": item.get("impact"),
            "Issue": item.get("recommendation", {}).get("issue"),
            "Fix": " | ".join(item.get("recommendation", {}).get("fix", [])),
            "Priority": item.get("recommendation", {}).get("priority")
        })

manual_df = pd.DataFrame(manual_rows)


with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    detailed_df.to_excel(writer, sheet_name="Detailed_Report", index=False)
    failures_df.to_excel(writer, sheet_name="Failures_Only", index=False)
    manual_df.to_excel(writer, sheet_name="Manual_Checks", index=False)

print(f"✅ Excel file created successfully: {output_file}")