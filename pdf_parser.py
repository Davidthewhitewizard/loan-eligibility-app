import pdfplumber
import pandas as pd
import re

def parse_bank_statement(pdf_file):
    transactions = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                for row in table[1:]:
                    if len(row) >= 5:
                        date, description, debit, credit, balance = row[:5]
                        try:
                            debit_val = float(re.sub(r"[^\d.-]", "", debit)) if debit else 0.0
                            credit_val = float(re.sub(r"[^\d.-]", "", credit)) if credit else 0.0
                            balance_val = float(re.sub(r"[^\d.-]", "", balance)) if balance else None
                            transactions.append({
                                "date": pd.to_datetime(date, errors="coerce"),
                                "description": description.strip(),
                                "debit": debit_val,
                                "credit": credit_val,
                                "balance": balance_val,
                                "net": credit_val - debit_val
                            })
                        except:
                            continue

    df = pd.DataFrame(transactions)
    return df

