# Insta Dashboard

This project aims to extract information and generate metrics from a given Instagram Profile and store it in a Google Spreadsheet at Drive, in order to feed these worksheets as data sources into a Google Data Studio Dashboard.

You can check a more detailed explanation at this Medium Article:
- [Web Scraping Instagram to build your own profile’s dashboard — With Instaloader and Google Data Studio](https://medium.com/@felipe.p.adachi/web-scraping-instagram-to-build-your-own-profiles-interactive-dashboard-with-instaloader-and-42141575e009)

To run this application, you should have:
- a Google account to use Drive. The dashboard building process at Data Studio is not covered in this project, but the google account is also needed if you want to use the metrics generated here to create the dashboard at Google Data Studio.
- an Imgur Account. The dashboard uses some images (for the profile pic and the wordcloud). At the time, I was not able to use an image URL at the drive itself, so I created an Imgur account to host the uploaded images.

# Installation

run:

`pip install -r requirements.txt`

In addition, there are some authorization steps you have to customize.

## GSpread
Follow these instructions in order to authenticate and authorize your application:

https://gspread.readthedocs.io/en/latest/oauth2.html

In the end, you should have a `credentials.json` to put at `~/.config/gspread/credentials.json`.

## Imgur
Follow these instructions to register an application at Imgur: https://apidocs.imgur.com/

Check the `registration quickstart` section and follow the steps just up until you generate the following: `client_id`,`client_secret`,`access_token` and `refresh_token`. Also take note of your imgur username. When you have all tokens and username, replace the placeholders at the `imgur_credentials.json` file.

## Google Sheet

Create a blank google spreadsheet at a location of your choice at Google Drive, and get its key. If the url of the blank sheet is, e.g., https://docs.google.com/spreadsheets/d/1h093LCbdJtDCNcDUnln4Lco-RANtl6-_XVi49InZCBw/edit#gid=0

the key would be: `1h093LCbdJtDCNcDUnln4Lco-RANtl6-_XVi49InZCBw`

Get this key and replace the variable `sheet_key` at `transform_and_upload.py`

# Usage

The main file is: `insta_pipe.sh`

At the command line, type:

`./insta_pipe.sh <instagram_profile> <language>`

Where `instagram_profile` is the Instagram Profile you wish to generate the dashboard, and language is the language you want the report to be generated (currently en and pt). The language influences not only some words that are displayed at the dashboard, but also the word cloud generated, as the chosen language's stopwords are removed. A new folder should be created with text information extracted through instaloader, and the google Sheet at your Drive should be updated with information from the given Instagram profile.

The process of assembling the dashboard at Google Data Studio is not discussed in this repository, but an example of dashboard can be seen on `sample.pdf`.
