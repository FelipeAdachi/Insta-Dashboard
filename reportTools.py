import pandas as pd
import os
import re



def assemble_info(path,imgur_conn,language='en'):
    caption_text = ''
    columns = ['media_type','media_code','likes','comments','date','hashes']
    df_posts = pd.DataFrame(columns=columns)
    img_link = None

    for filename in os.listdir(path):
        if 'profile_pic' in filename:
            image = imgur_conn.upload_image(os.path.join(path,filename))
            img_link = image['link']
        if filename.endswith(".txt") and "old" not in filename:
            with open(os.path.join(path,filename),"r") as f:
                lines = f.readlines()
            row_vals = {}
            hashes = []
            for index,rawline in enumerate(lines):
                line = rawline.strip()
                #date
                if index == 1:
                    row_vals['date'] = line
                
                #media type
                if index == 3:
                    if line == 'GraphImage':
                        row_vals['media_code'] = 1
                        if language == 'pt':
                            row_vals['media_type'] = "Imagem"
                        elif language == 'en':
                            row_vals['media_type'] = "Image"

                    if line == 'GraphVideo':
                        row_vals['media_code'] = 2
                        if language == 'pt':
                            row_vals['media_type'] = "Vídeo"
                        elif language == 'en':
                            row_vals['media_type'] = "Video"

                    if line == 'GraphSidecar':
                        row_vals['media_code'] = 3
                        if language == 'pt':
                            row_vals['media_type'] = "Carrosel"
                        elif language == 'en':
                            row_vals['media_type'] = "Sidecar"

                
                #likes
                if index == 5:
                    row_vals['likes'] = int(line)

                if index == 7:
                    row_vals['comments'] = int(line)
                if index >= 9:
                    # print(line)
                    # print("#---------------#------------#------------#----------------")
                    # hashRegex = re.compile(r'#[a-zA-Z0-9_]*') 
                    matches = re.findall(r"#[a-zA-Z0-9_]*",line) 
                    if matches:
                        for match in matches:
                            hashes.append(match.strip('#'))
                        # print(matches)
                    else:
                        caption_text = caption_text + ' ' + line
                    row_vals['hashes'] = hashes
                


            df_posts = df_posts.append(row_vals, ignore_index=True)
    return df_posts,caption_text,img_link

#########################################################################

def generate_top_hashes(df_posts):
    hash_likes = {}
    hash_occurences = {}
    for index,row in df_posts.iterrows():
        for hash in row['hashes']:
            cur_likes = hash_likes.get(hash,0)
            cur_occur = hash_occurences.get(hash,0)
            hash_likes[hash] = cur_likes + row['likes']
            hash_occurences[hash] = cur_occur + 1

    hash_mean_likes = []

    for key in hash_likes:
        lks = hash_likes.get(key)
        occ = hash_occurences.get(key)
        mean_lks = lks/occ
        hash_mean_likes.append((mean_lks,key,occ))


    hash_mean_likes.sort(reverse=True)
    hash_mean_likes = [x for x in hash_mean_likes if x[2]>=5]
    hash_mean_likes = list(map(lambda x:(x[0],'#' + str(x[1]),x[2]),hash_mean_likes))
    hash_mean_likes = list(map(lambda x:(round(x[0],1),x[1],x[2]),hash_mean_likes))
    hash_mean_likes = hash_mean_likes[0:10]

    hash_cols = ['Avg Likes','Hashtag']
    df_hash = pd.DataFrame(columns=hash_cols)
    df_hash['Avg Likes'] = [x[0] for x in hash_mean_likes]
    df_hash['Hashtag'] = [x[1] for x in hash_mean_likes]
   
    return df_hash

#########################################################################

def generate_df_per_day(df_posts,language):
    df_posts['date'] = pd.to_datetime(df_posts['date'],format = '%Y-%m-%d_%H-%M-%S')
    df_posts['weekday'] = df_posts['date'].dt.dayofweek

    mean_perday = []
    weekdays = ['Dom','Seg','Ter','Qua','Qui','Sex','Sab']
    for i,day in enumerate(weekdays):
        mean_day = df_posts.loc[df_posts['weekday']==i]['likes'].mean()
        posts_day = len(df_posts.loc[df_posts['weekday']==i])
        mean_perday.append((round(mean_day,0),day,posts_day))
    if language == 'pt':
        day_cols = ['Média de Likes','Dia']
        df_day = pd.DataFrame(columns=day_cols)
        df_day['Média de Likes'] = [x[0] for x in mean_perday]
        df_day['Dia'] = [x[1] for x in mean_perday]
        df_day['Número de Posts'] = [x[2] for x in mean_perday]
    elif language == 'en':
        day_cols = ['Avg Likes','Week Day']
        df_day = pd.DataFrame(columns=day_cols)
        df_day['Avg Likes'] = [x[0] for x in mean_perday]
        df_day['Week Day'] = [x[1] for x in mean_perday]
        df_day['No. Posts'] = [x[2] for x in mean_perday]

    return df_day

#########################################################################

def assemble_metrics(df_posts):
    df_image = df_posts.loc[df_posts['media_code']==1]
    df_video = df_posts.loc[df_posts['media_code']==2]
    df_carousel = df_posts.loc[df_posts['media_code']==3]

    ##### Assembling metrics
    metrics = {}

    metrics['mean_likes'] = round(df_posts['likes'].mean(),1)
    metrics['mean_comments'] = round(df_posts['comments'].mean(),1)
    metrics['likes_image'] = round(df_image['likes'].mean(),1)
    metrics['likes_video'] = round(df_video['likes'].mean(),1)
    metrics['likes_carousel'] = round(df_carousel['likes'].mean(),1)

    return metrics

