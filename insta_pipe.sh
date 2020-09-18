#!/bin/bash
instaloader --no-pictures --no-videos --no-metadata-json --post-metadata-txt="date:\n{date_local}\ntypename:\n{typename}\nlikes:\n{likes}\ncomments:\n{comments}\ncaption:\n{caption}" $1;
python fix_lines.py $1
python transform_and_upload.py $1 $2