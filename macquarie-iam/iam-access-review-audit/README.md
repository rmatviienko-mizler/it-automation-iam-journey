# IAM Access Review Audit

This project is a Python-based Identity and Access Management (IAM) access review audit script.

It analyzes sample CSV exports related to users, access assignments, approvals, and sessions. The script identifies common IAM access review issues such as privileged users without MFA, disabled or terminated users with active application access, disabled or terminated users with active sessions, active access without approval, risky service accounts, mover access risks, and contractor accounts past their approved end date.

The script prints audit findings to the terminal, sorts findings by severity, and creates output report files.

## Project Purpose

The goal of this project is to demonstrate practical IAM access review and identity operations skills using Python and CSV data.

This project focuses on:

* Access review logic
* Deprovisioning risk detection
* Privileged access checks
* MFA risk detection
* Approval validation
* Active session risk detection
* Service account risk detection
* Mover access review
* Contractor end-date review
* CSV reading and reporting with Python

## Project Structure

```text
iam-access-review-audit/
├── README.md
├── iam_audit.py
├── sample_output.md
├── data/
│   ├── access_assignments.csv
│   ├── approvals.csv
│   ├── sessions.csv
│   └── users.csv
└── output/
    ├── findings.csv
    └── summary_report.txt
```

## Requirements

This project uses Python 3 and only Python standard library modules:

* `csv`
* `pathlib`
* `datetime`

No external packages are required.

## Input Files

The script uses four sample CSV files from the `data/` folder.

### `data/users.csv`

Contains identity and account data with the following fields:

```text
username
full_name
department
previous_department
employment_type
hr_status
account_status
mfa_enabled
role
end_date
account_type
owner
key_age_days
```

### `data/access_assignments.csv`

Contains application access assignment data with the following fields:

```text
username
application
access_role
access_status
group_name
```

### `data/approvals.csv`

Contains access approval data with the following fields:

```text
username
application
approval_ticket
approved_by
```

### `data/sessions.csv`

Contains session data with the following fields:

```text
username
session_active
last_login_days
```

## IAM Checks Performed

The script performs the following IAM audit checks.

### 1. Active human admin without MFA

Finds active human users with admin privileges who do not have MFA enabled.

Why this matters:

```text
An active admin account without MFA increases the risk of privileged account compromise.
```

### 2. Disabled or terminated users with active application access

Finds users who are disabled or terminated but still have active application access.

Why this matters:

```text
A disabled or terminated user should not retain active access to business applications.
```

### 3. Disabled or terminated users with active sessions

Finds disabled or terminated users who still have active sessions.

Why this matters:

```text
Even if an account is disabled, an existing active session may still allow access until the session is revoked.
```

### 4. Active access without approval

Finds active application access where:

* The approval ticket is missing
* Or no matching approval record exists

Admin access without approval is marked as higher severity than standard user access.

Why this matters:

```text
Access without documented approval creates audit, compliance, and authorization risk.
```

### 5. Risky service accounts

Finds active service accounts with risks such as:

* Missing `owner`
* Admin `role`
* `key_age_days` greater than 365

Why this matters:

```text
Service accounts often run automated processes and can become high-risk if ownership, privileges, or key rotation are not controlled.
```

### 6. Mover access risk

Finds active human users who may still have access related to their `previous_department`.

The script checks whether the previous department appears in the `application` name or `group_name`.

Why this matters:

```text
A user who moved departments may retain old access that is no longer required, creating privilege creep.
```

### 7. Active contractor past end date

Finds active contractor accounts where:

* `end_date` is missing
* Or `end_date` has already passed

Why this matters:

```text
Contractor access should be time-limited. If the end date has passed, the account should be disabled or formally extended.
```

## Severity Sorting

Findings are sorted by severity before being printed to the terminal and written to the output files.

Severity order:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

The script uses a helper function called `get_severity_rank()` to assign each severity a numeric rank:

```text
CRITICAL -> 1
HIGH     -> 2
MEDIUM   -> 3
LOW      -> 4
```

This makes the report easier to review because the most important findings appear first.

## How to Run

From the project folder, run:

```bash
python3 iam_audit.py
```

## Output

The script prints a human-readable audit report to the terminal and creates two output files in the `output/` folder.

### Terminal output

The terminal output shows:

* Number of users loaded
* Number of access assignments loaded
* Number of approval records loaded
* Number of session records loaded
* Sorted audit findings
* Recommended action for each finding

A full example of the terminal output is available in:

```text
sample_output.md
```

### `output/findings.csv`

Detailed audit findings in CSV format.

Columns:

```text
severity,username,finding,recommended_action
```

This file is useful for reviewing findings in a spreadsheet or sharing structured audit results.

### `output/summary_report.txt`

A short summary report with finding counts by severity.

This file is useful for quickly reviewing the total number of findings by severity level.

## Skills Demonstrated

This project demonstrates:

* Python CSV processing
* Working with lists and dictionaries
* Reading CSV files with `csv.DictReader`
* Writing CSV output files with `csv.DictWriter`
* Writing text summary reports
* Sorting audit findings by severity
* IAM access review logic
* Deprovisioning risk detection
* Privileged access review
* MFA risk detection
* Approval validation
* Session risk review
* Service account review
* Mover access review
* Contractor access review
* Practical identity operations thinking

## Notes

All data in this project is fictional and used for learning and portfolio purposes only.

This project is intended to demonstrate entry-level IAM operations, access review, and Python automation skills.

