from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize


def generate_wordcloud(caption_text,language):

    if language == 'pt':
        stopwords = nltk.corpus.stopwords.words('portuguese')
    elif language == 'en':
        stopwords = nltk.corpus.stopwords.words('english')

    try:
        text_tokens = word_tokenize(caption_text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords]
        filtered_sentence = (" ").join(tokens_without_sw)
        wordcloud = WordCloud(background_color="white").generate(filtered_sentence)
        wordcloud.to_file("wcloud.png")
        return 1
    except:
        return None