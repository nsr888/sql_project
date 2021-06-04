#/bin/bash
rm sber.db
unzip data.zip '*01032021*'
python3 main.py
mkdir -p archive
for FILENAME in *.xlsx; do mv $FILENAME ./archive/$FILENAME.backup; done
for FILENAME in transactions*.txt; do mv $FILENAME ./archive/$FILENAME.backup; done
