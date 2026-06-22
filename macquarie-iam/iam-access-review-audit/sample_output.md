# Sample Output

Example terminal output after running:

```bash
python3 iam_audit.py
```

```text
IAM Access Review Audit
-----------------------
Users loaded: 7
Access assignments loaded: 9
Approvals loaded: 8
Sessions loaded: 7

Findings
--------
CRITICAL | carol | Disabled or terminated user still has active access to SalesCRM
Recommended action: Remove application access and verify full deprovisioning

CRITICAL | carol | Disabled or terminated user still has an active session
Recommended action: Revoke active sessions and verify full offboarding

HIGH | bob | Active human admin without MFA
Recommended action: Enable MFA or remove privileged role

HIGH | svc_backup | Active access to CloudStorage without approval ticket
Recommended action: Review access justification and obtain or document approval

HIGH | svc_backup | Service account is missing an owner
Recommended action: Assign a business or technical owner to the service account

HIGH | svc_backup | Service account has admin role
Recommended action: Review least privilege and reduce permissions if possible

HIGH | david | Active contractor account past end date: 2026-05-15
Recommended action: Disable contractor account or extend the approved end date

MEDIUM | carol | Active access to SalesCRM without approval ticket
Recommended action: Review access justification and obtain or document approval

MEDIUM | emma | Active access to SalesCRM without approval ticket
Recommended action: Review access justification and obtain or document approval

MEDIUM | frank | Active access to FinanceApp without approval record
Recommended action: Review access justification and obtain or document approval

MEDIUM | svc_backup | Service account key is older than 365 days
Recommended action: Rotate the service account key or secret

MEDIUM | emma | User may still have access related to previous department: SalesCRM / sales-users
Recommended action: Review mover access and remove old department access if no longer required
```

The script also creates two output files:

```text
output/findings.csv
output/summary_report.txt
```

The full structured CSV report is available in:

```text
output/findings.csv
```

Example `summary_report.txt`:

```text
IAM Access Review Audit Summary
-------------------------------

Total findings: 12

Critical: 2
High: 5
Medium: 5
Low: 0
```

