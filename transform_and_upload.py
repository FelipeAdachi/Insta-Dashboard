import sys
import json
from gSheet import gSheet
from reportTools import assemble_info,generate_df_per_day,generate_top_hashes,assemble_metrics
from imgur import Imgur
#########################################################################

def main():

    path = sys.argv[1]
    language = sys.argv[2]



    # Google Sheet Key we want to use to update Data Studio
    sheet_key = 'your-sheet-key'
    g_sheet = gSheet(sheet_key)

    with open('imgur_credentials.json','r') as f:
        imgur_credentials = json.load(f)
    imgur_conn = Imgur(imgur_credentials)
    print("Cleaning preexisting images...")
    res = imgur_conn.clean_user_images()
    if not res:
        "Error on cleaning user images!"


    df_posts,caption_text,img_link = assemble_info(path,imgur_conn,language)
    df_hash = generate_top_hashes(df_posts)
    df_day = generate_df_per_day(df_posts,language)
    df_data = df_posts[['media_code','media_type','likes','comments']]

    metrics = assemble_metrics(df_posts)

    #------------#-------------#--------#---------------
    mean_likes = metrics['mean_likes']
    mean_comments = metrics['mean_comments']
    likes_image = metrics['likes_image']
    likes_video = metrics['likes_video']
    likes_carousel = metrics['likes_carousel']


    g_sheet.update_data_sheet(df_data)
    g_sheet.update_wordcloud(caption_text,path,imgur_conn,language)
    g_sheet.update_mainmetrics(mean_likes,mean_comments)
    g_sheet.update_top_hashes(df_hash)
    g_sheet.update_media_metrics(likes_image,likes_video,likes_carousel)
    g_sheet.update_day_metrics(df_day)
    g_sheet.update_profile_info(img_link,path)

if __name__ == "__main__":
    main()