from transformers import pipeline
import pandas as pd

df = pd.read_excel('../../docker/datafiles/PromptCategories.xlsx') # can also index sheet by name or fetch all sheets
print(df)
mylist = df['Categories'].tolist()
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
print("Test")
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
print("Test2s")
data = ["canned pork", "Electrical or plumbing problems with your house might come up. Call a professional, Aries. Don't try to fix it yourself, because you could make it worse. Friends might want to visit but tell them to wait until another day. Discussions could quickly deteriorate into arguments today. This is a great day to work quietly alone on whatever interests you the most."]
candidate_labels = ['general', 'birthday', 'wellness', 'love', 'career']
candidate_labels = mylist
sequence_to_classify = "This is an excellent day to express your natural creativity, Aries. The arts will more than likely be very important to you. You may find that nothing brings you more pleasure on days like this. Consider putting this to good use by painting, sculpting, or doing crafts. You'll find the perfect thing for you is engaging in art activities with a focus on giving."
print(classifier(sequence_to_classify, candidate_labels,multi_label=True))
print(sentiment_pipeline(data))