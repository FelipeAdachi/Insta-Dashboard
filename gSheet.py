from wcloud import generate_wordcloud
import gspread
import math
import re

class gSheet:
    def __init__(self, sheet_key):
        self.gc = gspread.oauth()
        self.sh = self.gc.open_by_key(sheet_key)

    def update_data_sheet(self,df_data):
        data_sheet = self.sh.worksheet('Data')
        criteria_re = re.compile(r'.')
        cell_list = data_sheet.findall(criteria_re)
        for cell in cell_list:
            #clean sheet first
            cell.value = ''
        data_sheet.update_cells(cell_list)

        data_sheet.update([df_data.columns.values.tolist()] + df_data.values.tolist())

    def update_wordcloud(self,caption_text,path,imgur_conn,language):
        res = generate_wordcloud(caption_text,language)
        cloud_sheet = self.sh.worksheet('WordCloud')
        cloud_sheet.update('A1', 'cloud_url')
        cloud_sheet.update('B1','profile_name')

        if res:
            cloud_image = imgur_conn.upload_image('wcloud.png')
            cloud_link = cloud_image['link']
            cloud_sheet.update('A2', cloud_link)
            cloud_sheet.update('B2',path)
        else:
            cloud_link = ' '
            cloud_sheet.update('A2', cloud_link)
            cloud_sheet.update('B2',path)

    def update_mainmetrics(self,mean_likes,mean_comments):
        mainmetrics_sheet = self.sh.worksheet('MainMetrics')
        mainmetrics_sheet.update('A1','mean_likes')
        mainmetrics_sheet.update('B1','mean_comments')
        mainmetrics_sheet.update('A2',mean_likes)
        mainmetrics_sheet.update('B2',mean_comments)

    def update_top_hashes(self,df_hash):
        hash_sheet = self.sh.worksheet('Top_Hash')
        hash_sheet.update('A2:B11', [[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' '],[' ', ' ']])
        hash_sheet.update([df_hash.columns.values.tolist()] + df_hash.values.tolist())

    def update_media_metrics(self,likes_image,likes_video,likes_carousel):
        mediametrics_sheet = self.sh.worksheet('MediaMetrics')
        mediametrics_sheet.update('A1','likes_image')
        mediametrics_sheet.update('B1','likes_video')
        mediametrics_sheet.update('C1','likes_carrosel')

        if not math.isnan(likes_image):
            mediametrics_sheet.update('A2',likes_image)
        else:
            mediametrics_sheet.update('A2',0)
        if not math.isnan(likes_video):
            mediametrics_sheet.update('B2',likes_video)
        else:
            mediametrics_sheet.update('B2',0)
        if not math.isnan(likes_carousel):
            mediametrics_sheet.update('C2',likes_carousel)
        else:
            mediametrics_sheet.update('C2',0)

    def update_day_metrics(self,df_day):
        day_sheet = self.sh.worksheet('DayMetrics')
        criteria_re = re.compile(r'.')
        cell_list = day_sheet.findall(criteria_re)
        for cell in cell_list:
            #clean sheet first
            cell.value = ''
        day_sheet.update_cells(cell_list)

        day_sheet.update([df_day.columns.values.tolist()] + df_day.values.tolist())

    def update_profile_info(self,img_link,path):
        profile_sheet = self.sh.worksheet('ProfileInfo')
        profile_sheet.update('A1', 'profile_url')
        profile_sheet.update('B1', 'profile_name')
        profile_sheet.update('A2', img_link)
        profile_sheet.update('B2',path)
