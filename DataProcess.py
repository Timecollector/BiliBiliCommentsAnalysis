import numpy as np
import pandas as pd
import re
import jieba
import matplotlib.pyplot as plt

stop_words = pd.read_csv('百度停用词列表.txt',encoding='gb18030',header=None).values

def text_process(text):
    text = text.lower()
    clear_list = '[，,。,.,？,！,【,】,(,),（,）,、,%,@,/,$,-,:,：,《,》,<,>,…,#,?,·,♀,=,!,"w",～]'
    text = re.sub(clear_list, "", text)
    text = re.sub(r"\[.*?\]", "", text)
    text = re.sub(r"\d+", "", text)
    text = text.strip()
    jieba.load_userdict("词典.txt")
    text = list(jieba.lcut(text))
    text = [word.strip() for word in text if word not in stop_words]
    return text

if __name__ == '__main__':
    danmaku = pd.read_csv('84887919comments1650424641.8339486.csv', encoding='gb18030').iloc[:, 5]
    danmaku = danmaku.apply(text_process)
    for i in danmaku:
        print(i)