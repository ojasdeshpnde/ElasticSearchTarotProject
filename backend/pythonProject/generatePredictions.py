from transformers import pipeline
import pandas as pd

prompts = pd.read_excel('C:/Users/dkd70/ElasticSearchTarotProject/docker/datafiles/PromptCategories.xlsx') # can also index sheet by name or fetch all sheets
readings = pd.read_csv('C:/Users/dkd70/ElasticSearchTarotProject/docker/datafiles/horoscope_saved.csv') # can also index sheet by name or fetch all sheets
predicted_path = 'C:/Users/dkd70/ElasticSearchTarotProject/docker/datafiles/horoscope_predicted.xlsx'
# print(readings)
# print(readings.index)
# print(readings.columns)
# print(readings[0:])
# print(readings[readings["category"] == "general"])
# df = pd.DataFrame([],[], columns=readings.columns.tolist()+["positive", "negative"]+prompts['Categories'].tolist())
df = pd.read_excel(predicted_path)
# To generate initial list DO NOT RUN WILL DELETE PREDICTIONS
# df.to_excel("C:/Users/dkd70/ElasticSearchTarotProject/docker/datafiles/horoscope_predicted.xlsx")
readings = readings[readings["category"]=="general"]
df = pd.concat([readings, df]).drop_duplicates(subset=readings.columns.tolist(), keep='last')
mylist = prompts['Categories'].tolist()
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")
df2 = df[df[mylist[0]].isnull()]
print(df2)
for i in range(len(df.index)):
    print(i)
    if i in df2.index:
        horoscope = df.iloc[i, df.columns.get_loc("horoscope")]
        x = sentiment_pipeline(horoscope)
        y = classifier(horoscope, mylist,multi_label=True)
        # print(y)
        df.loc[i, y['labels']] = y['scores']
        # print(df2.loc[i])
        # print(horoscope)
        if i % 10 == 9:
            print("Saving:")
            df.to_excel(predicted_path, index=False)
            print("Saved!")
# print(df2[df2["positive"].isnull()])
# df = pd.concat([df, df2]).drop_duplicates(subset=readings.columns.tolist(), keep='last')
df.to_excel(predicted_path, index = False)
print(df)