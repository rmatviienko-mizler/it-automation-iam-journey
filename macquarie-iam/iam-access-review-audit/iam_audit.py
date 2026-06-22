#!/usr/bin/env python3

import csv
from pathlib import Path
from datetime import date, datetime


DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")


def read_csv_file(file_path):
    """
    Read a CSV file and return a list of dictionaries.
    Each row becomes one dictionary.
    """
    rows = []

    with open(file_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            rows.append(row)

    return rows


def write_findings_to_csv(findings, file_path):
    """
    Write audit findings to a CSV file.
    """
    fieldnames = ["severity", "username", "finding", "recommended_action"]

    with open(file_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(findings)


def write_summary_report(findings, file_path):
    """
    Write a summary report with finding counts by severity.
    """
    severity_counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for finding in findings:
        severity = finding["severity"]

        if severity in severity_counts:
            severity_counts[severity] += 1

    with open(file_path, "w", encoding="utf-8") as f:
        f.write("IAM Access Review Audit Summary\n")
        f.write("-------------------------------\n")
        f.write("\n")
        f.write(f"Total findings: {len(findings)}\n")
        f.write("\n")
        f.write(f"Critical: {severity_counts['CRITICAL']}\n")
        f.write(f"High: {severity_counts['HIGH']}\n")
        f.write(f"Medium: {severity_counts['MEDIUM']}\n")
        f.write(f"Low: {severity_counts['LOW']}\n")


def get_severity_rank(finding):
    severity = finding["severity"]

    if severity == "CRITICAL":
        return 1
    elif severity == "HIGH":
        return 2
    elif severity == "MEDIUM":
        return 3
    elif severity == "LOW":
        return 4
    else:
        return 99


def check_active_admin_without_mfa(users):
    """
    Find active human admin users who do not have MFA enabled.
    """
    admin_findings = []

    for user in users:
        username = user["username"].strip()
        account_status = user["account_status"].strip().lower()
        role = user["role"].strip().lower()
        mfa_enabled = user["mfa_enabled"].strip().lower()
        account_type = user["account_type"].strip().lower()

        if account_type == "human" and account_status == "active":
            if role == "admin" and mfa_enabled == "false":
                finding = {
                    "severity": "HIGH",
                    "username": username,
                    "finding": "Active human admin without MFA",
                    "recommended_action": "Enable MFA or remove privileged role"
                }

                admin_findings.append(finding)

    return admin_findings


def check_disabled_or_terminated_users_with_active_access(users, access_assignments):
    """
    Find disabled or terminated users who still have active application access.
    """
    deprovisioning_findings = []

    for access in access_assignments:
        username = access["username"].strip()
        application = access["application"].strip()
        access_status = access["access_status"].strip().lower()

        if access_status == "active":
            for user in users:
                user_username = user["username"].strip()

                if username == user_username:
                    hr_status = user["hr_status"].strip().lower()
                    account_status = user["account_status"].strip().lower()

                    if hr_status == "terminated" or account_status == "disabled":
                        finding = {
                            "severity": "CRITICAL",
                            "username": username,
                            "finding": f"Disabled or terminated user still has active access to {application}",
                            "recommended_action": "Remove application access and verify full deprovisioning"
                        }

                        deprovisioning_findings.append(finding)

                    break

    return deprovisioning_findings


def check_disabled_or_terminated_users_with_active_sessions(users, sessions):
    """
    Find disabled or terminated users who still have active sessions.
    """
    session_findings = []

    for session in sessions:
        username = session["username"].strip()
        session_active = session["session_active"].strip().lower()

        if session_active == "true":
            for user in users:
                user_username = user["username"].strip()

                if username == user_username:
                    hr_status = user["hr_status"].strip().lower()
                    account_status = user["account_status"].strip().lower()

                    if hr_status == "terminated" or account_status == "disabled":
                        finding = {
                            "severity": "CRITICAL",
                            "username": username,
                            "finding": "Disabled or terminated user still has an active session",
                            "recommended_action": "Revoke active sessions and verify full offboarding"
                        }

                        session_findings.append(finding)

                    break

    return session_findings


def check_active_access_without_approval(access_assignments, approvals):
    """
    Find active application access that does not have an approval ticket.
    """
    approval_findings = []

    for access in access_assignments:
        username = access["username"].strip()
        application = access["application"].strip()
        access_status = access["access_status"].strip().lower()
        access_role = access["access_role"].strip().lower()

        if access_status == "active":
            # Track whether this active access has a matching approval record.
            matching_approval_found = False

            if access_role == "admin":
                severity = "HIGH"
            else:
                severity = "MEDIUM"

            for approval in approvals:
                approval_username = approval["username"].strip()
                approval_application = approval["application"].strip()
                approval_ticket = approval["approval_ticket"].strip()

                if username == approval_username and application == approval_application:
                    matching_approval_found = True

                    if approval_ticket == "":
                        finding = {
                            "severity": severity,
                            "username": username,
                            "finding": f"Active access to {application} without approval ticket",
                            "recommended_action": "Review access justification and obtain or document approval"
                        }

                        approval_findings.append(finding)

                    break

            if matching_approval_found == False:
                finding = {
                    "severity": severity,
                    "username": username,
                    "finding": f"Active access to {application} without approval record",
                    "recommended_action": "Review access justification and obtain or document approval"
                }

                approval_findings.append(finding)

    return approval_findings

def check_service_account_risks(users):
    """
    Find risky service accounts.
    """
    service_account_findings = []

    for user in users:
        username = user["username"].strip()
        account_type = user["account_type"].strip().lower()
        account_status = user["account_status"].strip().lower()
        owner = user["owner"].strip()
        role = user["role"].strip().lower()
        key_age_days = int(user["key_age_days"].strip())

        if account_type == "service" and account_status == "active":
            if owner == "":
                finding = {
                    "severity": "HIGH",
                    "username": username,
                    "finding": "Service account is missing an owner",
                    "recommended_action": "Assign a business or technical owner to the service account"
                }

                service_account_findings.append(finding)

            if role == "admin":
                finding = {
                    "severity": "HIGH",
                    "username": username,
                    "finding": "Service account has admin role",
                    "recommended_action": "Review least privilege and reduce permissions if possible"
                }

                service_account_findings.append(finding)

            if key_age_days > 365:
                finding = {
                    "severity": "MEDIUM",
                    "username": username,
                    "finding": "Service account key is older than 365 days",
                    "recommended_action": "Rotate the service account key or secret"
                }

                service_account_findings.append(finding)

    return service_account_findings


def check_mover_old_department_access(users, access_assignments):
    """
    Find active users who may still have access related to their previous department.
    """
    mover_findings = []

    for user in users:
        username = user["username"].strip()
        account_type = user["account_type"].strip().lower()
        account_status = user["account_status"].strip().lower()
        previous_department = user["previous_department"].strip().lower()

        if account_type == "human" and account_status == "active" and previous_department != "":
            for access in access_assignments:
                access_username = access["username"].strip()
                application = access["application"].strip()
                group_name = access["group_name"].strip()
                access_status = access["access_status"].strip().lower()

                application_check = application.lower()
                group_name_check = group_name.lower()

                if username == access_username and access_status == "active":
                    if previous_department in application_check or previous_department in group_name_check:
                        finding = {
                            "severity": "MEDIUM",
                            "username": username,
                            "finding": f"User may still have access related to previous department: {application} / {group_name}",
                            "recommended_action": "Review mover access and remove old department access if no longer required"
                        }

                        mover_findings.append(finding)

    return mover_findings


def check_active_contractor_past_end_date(users):
    """
    Find active contractor accounts that are missing an end date
    or have an end date that has already passed.
    """
    contractor_findings = []

    today = date.today()

    for user in users:
        username = user["username"].strip()
        employment_type = user["employment_type"].strip().lower()
        account_status = user["account_status"].strip().lower()
        end_date_text = user["end_date"].strip()

        if employment_type == "contractor" and account_status == "active":
            if end_date_text == "":
                finding = {
                    "severity": "HIGH",
                    "username": username,
                    "finding": "Active contractor account is missing an end date",
                    "recommended_action": "Add an approved contractor end date or disable the account"
                }

                contractor_findings.append(finding)

            else:
                end_date = datetime.strptime(end_date_text, "%Y-%m-%d").date()

                if end_date < today:
                    finding = {
                        "severity": "HIGH",
                        "username": username,
                        "finding": f"Active contractor account past end date: {end_date_text}",
                        "recommended_action": "Disable contractor account or extend the approved end date"
                    }

                    contractor_findings.append(finding)

    return contractor_findings


def main():
    users = read_csv_file(DATA_DIR / "users.csv")
    access_assignments = read_csv_file(DATA_DIR / "access_assignments.csv")
    approvals = read_csv_file(DATA_DIR / "approvals.csv")
    sessions = read_csv_file(DATA_DIR / "sessions.csv")
    findings = []

    admin_mfa_findings = check_active_admin_without_mfa(users)
    findings.extend(admin_mfa_findings)

    deprovisioning_findings = check_disabled_or_terminated_users_with_active_access(users, access_assignments)
    findings.extend(deprovisioning_findings)

    session_findings = check_disabled_or_terminated_users_with_active_sessions(users, sessions)
    findings.extend(session_findings)

    approval_findings = check_active_access_without_approval(access_assignments, approvals)
    findings.extend(approval_findings)

    service_account_findings = check_service_account_risks(users)
    findings.extend(service_account_findings)

    mover_findings = check_mover_old_department_access(users, access_assignments)
    findings.extend(mover_findings)

    contractor_findings = check_active_contractor_past_end_date(users)
    findings.extend(contractor_findings)

    findings = sorted(findings, key=get_severity_rank)

    OUTPUT_DIR.mkdir(exist_ok=True)
    write_findings_to_csv(findings, OUTPUT_DIR / "findings.csv")
    write_summary_report(findings, OUTPUT_DIR / "summary_report.txt")

    print("IAM Access Review Audit")
    print("-----------------------")
    print(f"Users loaded: {len(users)}")
    print(f"Access assignments loaded: {len(access_assignments)}")
    print(f"Approvals loaded: {len(approvals)}")
    print(f"Sessions loaded: {len(sessions)}")
    print()

    print("Findings")
    print("--------")

    if not findings:
        print("No findings found.")
    else:
        for finding in findings:
            print(f"{finding['severity']} | {finding['username']} | {finding['finding']}")
            print(f"Recommended action: {finding['recommended_action']}")
            print()


if __name__ == "__main__":
    main()