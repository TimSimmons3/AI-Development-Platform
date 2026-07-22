# ADP Validation Scope and Legacy Baseline Debt Standard

## 1. Purpose

Prevent unrelated historical defects from causing ambiguous or destructive failures in controlled installers and closeout packages.

## 2. Validation Scope

A delivery gate shall distinguish:

- Changed-artifact validation
- Repository-baseline validation
- Runtime validation
- Legacy technical-debt discovery

Changed-artifact validation is mandatory for every delivery.

Repository-wide validation shall be used only when:

- The release explicitly claims a repository-wide clean baseline, or
- The gate was proven against the actual repository before mutation.

## 3. Pre-Existing Debt

A pre-existing defect may be recorded without blocking an unrelated change when:

- It is present in the starting Git baseline.
- The current change does not modify the affected artifact.
- It creates no immediate safety, security, or execution risk.
- The current changed artifacts pass their own controls.
- A separate remediation record is created.

## 4. Installer Requirements

Before mutation, an installer shall:

1. Validate the expected Git baseline.
2. Validate the actual repository architecture.
3. Identify its exact write set.
4. Test gates against representative baseline content.
5. Avoid scanning unrelated historical artifacts unless required by scope.

After a partial failure, a recovery installer shall:

1. Validate all dirty paths against the known write set.
2. Restore tracked files to the expected baseline.
3. Remove only known package-created untracked files.
4. Verify a clean worktree before retrying.
5. Never use broad destructive cleanup for unknown paths.

## 5. Reporting

A gate failure shall print:

- Failed control
- Affected path
- Whether the issue is new or pre-existing
- Whether repository mutation occurred
- Required recovery action
