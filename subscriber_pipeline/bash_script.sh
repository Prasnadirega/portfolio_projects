#!/bin/bash

echo 'Do you want to clean the data? [1/0]'
read cleancontinue

if [ "$cleancontinue" -eq 1 ]; then
    echo 'Cleaning data...'
    python dev/unit_test_code.py
    echo 'Done data cleansing.'

    dev_version=$(head -n 1 dev/changelog.md)
    prod_version=$(head -n 1 prod/changelog.md)

    read -a splitversion_dev <<< "$dev_version"
    read -a splitversion_prod <<< "$prod_version"

    dev_version="${splitversion_dev[1]}"
    prod_version="${splitversion_prod[1]}"

    if [ "$prod_version" != "$dev_version" ]; then
        echo 'New changes detected. Move files to prod? [1/0]'
        read scriptcontinue
    else
        scriptcontinue=0
    fi
else
    echo 'Please come back when you are ready.'
    exit 1
fi

if [ "$scriptcontinue" -eq 1 ]; then
    for filename in dev/*; do
        basefile=$(basename "$filename")
        if [[ "$basefile" == "cademycode.db" || "$basefile" == "cleanse_data.py" || "$basefile" == "cleanse_db.log" ]]; then
            echo "Not copying $filename"
        elif [[ "$basefile" == "cademycode_cleansed.db" || "$basefile" == "cademycode_cleansed.csv" ]]; then
            mv "$filename" prod/
            echo "Moving $filename"
        else
            cp "$filename" prod/
            echo "Copying $filename"
        fi
    done
else
    echo 'Please come back when ready.'
fi
