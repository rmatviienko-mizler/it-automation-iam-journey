#!/bin/bash

if [[ $# != 2 ]]
then
  echo "backup.sh target_directory_name destination_directory_name"
  exit 1
fi

if [[ ! -d "$1" ]] || [[ ! -d "$2" ]]
then
  echo "Invalid directory path provided"
  exit 1
fi

targetDirectory=$1
destinationDirectory=$2

echo "Source directory: $targetDirectory"
echo "Destination directory: $destinationDirectory"

currentTS=$(date +%s)

backupFileName="backup-${currentTS}.tar.gz"

origAbsPath=$(pwd)

cd "$destinationDirectory" || exit 1
destDirAbsPath=$(pwd)

cd "$origAbsPath" || exit 1
cd "$targetDirectory" || exit 1

yesterdayTS=$((currentTS - 24 * 60 * 60))

declare -a toBackup

for file in *
do
  if [[ $(date -r "$file" +%s) -gt "$yesterdayTS" ]]
  then
    toBackup+=("$file")
  fi
done

if [[ ${#toBackup[@]} -eq 0 ]]
then
  echo "There are no files modified within the last 24 hours."
  exit 0
fi

tar -czvf "$backupFileName" "${toBackup[@]}"

mv "$backupFileName" "$destDirAbsPath"

echo "Backup created: $destDirAbsPath/$backupFileName"