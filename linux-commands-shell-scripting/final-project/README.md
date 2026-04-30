# Scheduled Backup Script

This project is a cleaned-up portfolio version of the final Bash scripting project from IBM's **Hands-on Introduction to Linux Commands and Shell Scripting** course.

The project demonstrates a basic Linux automation workflow: checking a source directory for files modified within the last 24 hours, creating a compressed backup archive, and moving the archive to a destination directory.

## Purpose

The purpose of this script is to automate a simple backup task. Instead of manually checking which files were recently updated, the script identifies those files automatically and stores them in a timestamped `.tar.gz` archive.

## How It Works

The script performs the following operations:

1. Checks that exactly two command-line arguments were provided.
2. Verifies that both arguments are valid directory paths.
3. Stores the source directory and destination directory in variables.
4. Creates a backup filename using the current Unix timestamp.
5. Records the absolute path of the destination directory.
6. Moves into the source directory.
7. Checks each file in the source directory.
8. Selects files modified within the last 24 hours.
9. Stores selected files in a Bash array.
10. Stops safely if no files need to be backed up.
11. Creates a compressed `.tar.gz` archive with `tar`.
12. Moves the archive to the destination directory.
13. Prints the final backup archive location.

## Usage

Run the script with two arguments: the target directory and the destination directory.

```bash
./backup.sh <target_directory> <destination_directory>
```

Example:

```bash
./backup.sh important-documents backups
```

In this example, the script checks the `important-documents` directory and moves the created backup archive into the `backups` directory.

## Output

The script prints the selected source and destination directories when it starts. If the backup is created successfully, it also prints the final backup archive location.

Example:

```text
Source directory: important-documents
Destination directory: backups
Backup created: /path/to/backups/backup-1777481234.tar.gz
```

If no files were modified within the last 24 hours, the script exits without creating an archive.

Example:

```text
Source directory: important-documents
Destination directory: backups
There are no files modified within the last 24 hours.
```

## Main Script

The main script file is `backup.sh`.

## Bash Concepts Used

This project uses the following Bash and Linux concepts:

- Command-line arguments: `$1`, `$2`, `$#`
- Conditional statements with `[[ ... ]]`
- Directory checks with `-d`
- Variables and command substitution
- Unix timestamps with `date +%s`
- File modification timestamps with `date -r`
- Arithmetic expansion with `$(( ... ))`
- `for` loops
- Bash arrays
- Array length checks with `${#array[@]}`
- Archive creation with `tar -czvf`
- File movement with `mv`
- Exit codes with `exit 0` and `exit 1`

## Notes

This version removes the task-specific lab comments used for grading and keeps the script focused on the final automation workflow. The script is intended as a beginner-friendly Bash automation project for a GitHub portfolio.