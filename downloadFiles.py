import os
import requests

# List of PDF URLs
pdf_urls = [
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-03/CNTY-Tax%20Deed%20Assignment%20Call%20for%20April.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-03/Shakman%20Exempt%20List%20as%20of%203.8.2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-03/Probate%20Claim%20Call%20for%20March%202026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-02/CNTY-Tax%20Deed%20Assignment%20Call%20for%20March%202026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-02/Probate%20Claim%20Call_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-02/Public%20Hearing%20Notice%204.9.26.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/HR%20Quarterly%20Report-Q4%202025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/DOC%202026-1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/District6KeyCard2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/District5KeyCard2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/District4KeyCard2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/District3KeyCard2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/District2KeyCard2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/District1KeyCard2026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2026-01/CCC%20Internship%20and%20Externship%20Application%202026.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-12/Shakman%20Exempt%20List%20as%20of%2012.26.25.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-10/HR%20Quarterly%20Report-Q3%202025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-10/Shakman%20Exempt%20List%20as%20of%2010.3.2025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-09/Shakman%20Exempt%20List%20as%20of%209.4.2025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/HR%20Quarterly%20Report-Q2%202025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-07/July%202025%20Semi-Annual%20Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-07/Shakman%20Exempt%20List%20as%20of%2007.08.2025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-05/Probate%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-05/HR%20Quarterly%20Report-Q1%202025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-04/Clerk%20Spyropoulos%20Shares%20Progress%20Report%202025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-04/FINAL%20Progress%20Report%202025%20(1)-compressed.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-04/CCC%20Ethics%20Executive%20Order.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-05/2025%20Employee%20Handbook.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-03/Shakman%20Exempt%20List%20as%20of%2003.17.2025.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-03/Direct%20Dial%20Court%20Information3725.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Suburban%20Bureaus.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Suburban%20Bureaus_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Suburban%20Bureaus_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Suburban%20Bureaus_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Suburban%20Bureaus_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Suburban%20Bureaus_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Expunge%20or%20Seal%20Your%20Record_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Expunge%20or%20Seal%20Your%20Record_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Expunge%20or%20Seal%20Your%20Record_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Expunge%20or%20Seal%20Your%20Record_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Expunge%20or%20Seal%20Your%20Record.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Direct%20Dial%20Court%20Information_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Traffic%20Division_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Traffic%20Division_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Traffic%20Division_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Traffic%20Division_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Traffic%20Division_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Traffic%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Protective%20Orders_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Filing%20a%20Civil%20Suit_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Civil%20Appeal%20Filings_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Family%20Law_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Passports_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Probate%20Division_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Law%20Division_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20County_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Chancery_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Juvenile%20Justice%20&%20Child%20Protection_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Criminal%20Division_Spa.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/GAO%2024D1%20-%20Consolidation%20of%20the%20Domestic%20Relations%20Division%20in%20Suburban%20Districts%202%203%204%205%20and%206%20(eff.%20Aug.%2016%202024).pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Chancery_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Family%20Law_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Criminal%20Division_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Protective%20Orders_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Probate%20Division_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Passports_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Juvenile%20Justice%20&%20Child%20Protection_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Filing%20a%20Civil%20Suit_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Family%20Law_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Direct%20Dial%20Court%20Information_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Criminal%20Division_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Civil%20Appeal%20Filings_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Law%20Division_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20County_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Chancery_3.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Protective%20Orders_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Probate%20Division_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Passports_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Juvenile%20Justice%20&%20Child%20Protection_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Filing%20a%20Civil%20Suit_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Family%20Law_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Direct%20Dial%20Court%20Information_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Civil%20Appeal%20Filings_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Law%20Division_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20County_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Chancery_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Protective%20Orders_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Probate%20Division_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Passports_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Juvenile%20Justice%20&%20Child%20Protection_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Filing%20a%20Civil%20Suit_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Family%20Law_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Direct%20Dial%20Court%20Information_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Criminal%20Division_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Civil%20Appeal%20Filings_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Law%20Division_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20County_1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Protective%20Orders.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Probate%20Division_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Passports_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Juvenile%20Justice%20&%20Child%20Protection_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Filing%20a%20Civil%20Suit_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Direct%20Dial%20Court%20Information.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Criminal%20Division_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Civil%20Appeal%20Filings_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Law%20Division_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20County_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Chancery_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Protective%20Orders_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Probate%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Passports.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Juvenile%20Justice%20&%20Child%20Protection.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Filing%20a%20Civil%20Suit.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Family%20Law.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Criminal%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/Civil%20Appeal%20Filings.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Law%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20County.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-08/All%20About%20Chancery.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Suburban%20Bureaus.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Traffic%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Expunge%20or%20Seal%20Your%20Record.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Protective%20Orders.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Civil%20Appeal%20Filings.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Passports.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/All%20About%20Law%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Family%20Law.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Filing%20a%20Civil%20Suit.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/All%20About%20Chancery.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Juvenile%20Justice%20&%20Child%20Protection_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/Criminal%20Division.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-02/All%20About%20County.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-01/HR%20Quarterly%20Report-4th%202024.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-01/Shakman%20Exempt%20List%201.28.25_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-01/GAO%202025-01_0001.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-01/DOC_2024-1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2025-01/January%202025%20Semi-Annual%20Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Key%20Card%20Dist%202.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Key%20Card%20Dist%203.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Key%20Card%20Dist%204.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Key%20Card%20Dist%205.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Key%20Card%20Dist%206.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Customer%20Service%20Call%20Center.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Direct%20Dial%20to%20Court%20Information.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Legal%20Aid%20Resources.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/A%20Guide%20to%20Legal%20Services%20in%20Cook%20County.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/A%20Guide%20to%20Immigration%20Services%20in%20Cook%20County.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/A%20Guide%20to%20Eviction%20and%20ERP.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/A%20Guide%20to%20Certificates%20of%20Good%20Conduct.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/A%20Descriptive%20Guide.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/New%20&%20Upgrade%20Services.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/Odyssey%20Portal%20User%20Guide%20_Justice%20Partners%20and%20Authorized%20Agencies%20v6.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-10/HR%20Quarterly%20Report-3rd%202024_0.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-09/Warrant%20Web%20Page%20Draft%20Content%208-15-24%20Updates.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-08/Monthly%20Calendar%202025%20Updated.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-08/2025%20Full%20Calendar.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-07/HR%20Quarterly%20Report-2nd%202024.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-05/HR%20Quarterly%20Report-1st%202024_2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-05/Published%20Forms%20Updated%203.27.24.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-04/2023%204th%20Quarter%20Report%20v03252024.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-04/2023%203rd%20Quarter%20Report%20v03212024.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-01/Shakman%20Exempt%201.26.2024.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-01/2024%20Exempt%20List%20010823.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-12/2023.12.07%202nd%20Quarterly%20Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-12/Expungement%20Resources%20QR.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-12/Nl_%20Legal%20Help%20-%20Cook%20County_Statewide.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-07/Revised%20DOC%202023-2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-07/CCCO%20Employment%20Plan%207.11.23.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-06/DOC_ComplaintForm.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-06/Website%20Version_CCC%20Shakman%20Exempt%20Employees_6.22.23.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-05/2023_1Q_Report_FINAL.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-04/CCCO%20Employment%20Plan%204.4.2023.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-03/DOC%202023-1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-02/ShakmanExemptList_2.28.23.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-02/DOC_2022-2.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-02/ShakmanExempt%202.2.23.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-02/DOC_2022-1.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-02/2022%204Q%20Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-01/CCCO%20Exempt%20List%201.24.23.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2023-01/(8220)%2011.21.22%20Clerk%20of%20Court%20complaince%20order.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-10/2022%203rd%20Quarter%20Report%20Revised%20(002).pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-10/CCCOAmendedEmploymentPlan(ApprovedSept_7_2022).pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-08/Shakman%20Compliance%20Second%20Quarter%202022%20Report%20Revised.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2024-12/master_warrant_help_guide_draft_vi_7-14-22%20updated.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-07/CCCO%20Employment%20Plan%20(eff%20%204%2029%2022).pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-04/ShakmanComplianceFirstQuarter2022Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Instructions.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Order%20Granting%20or%20Denying%20Motion.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Additional%20Notice%20of%20Court%20Date.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Notice%20of%20Court%20Date%20for%20Motion.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Getting%20Started%20Motion%20to%20Vacate%20and%20Expunge.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Motion%20to%20Vacate%20and%20Expunge.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/CXP%20Additional%20Cannabis%20Convictions.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/2022-03/Shakman%20Compliance%20Fourth%20Quarter%202021%20Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/2022-03/Shakman%20Compliance%20Third%20Quarter%202021%20Report.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/EXP-AD%20Instructions.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/EXP-AD%20Order%20Granting.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/EXP-AD%20Notice.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/EXP-AD%20Additional%20Cases%20Expungement.pdf",
"https://www.cookcountyclerkofcourt.org/sites/g/files/ywwepo221/files/document/file/2022-05/EXP-AD%20Additional%20Cases%20Sealing.pdf",
]

# Directory to save PDFs
save_dir = "downloaded_pdfs"
os.makedirs(save_dir, exist_ok=True)

# Tracking
total_urls = len(pdf_urls)
downloaded_count = 0
failed_urls = []
print(f"📊 Starting PDF Download Process...\nTotal URLs to download: {total_urls}\n")
def download_pdf(url, folder):
    global downloaded_count

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        # Include the parent URL folder (e.g., 2025-08) in filename to avoid collisions.
        parts = url.split("/")
        filename = f"{parts[-2]}__{parts[-1]}".replace("%20", "_")
        file_path = os.path.join(folder, filename)

        with open(file_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

        print(f"✅ Downloaded: {filename}")
        downloaded_count += 1

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed: {url}")
        failed_urls.append(url)

# Download all PDFs
for pdf_url in pdf_urls:
    download_pdf(pdf_url, save_dir)

# Summary
print("\n📊 Download Summary")
print(f"Total URLs           : {total_urls}")
print(f"Downloaded Files     : {downloaded_count}")
print(f"Failed Downloads     : {len(failed_urls)}")

if failed_urls:
    print("\n❌ Failed URLs:")
    for url in failed_urls:
        print(url)

print("\n🎉 Process Completed.")