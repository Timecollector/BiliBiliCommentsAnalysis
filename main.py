import numpy as np
import pandas as pd
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import matplotlib
from DataProcess import text_process


danmaku = pd.read_csv('84887919comments1650424641.8339486.csv', encoding='gb18030').iloc[:, 5]
danmaku = danmaku.apply(text_process)

words = []
count = 0
for i in danmaku:
    if i:
        print(i)
        words.append(i)
        count += 1

# 构建词向量
model = Word2Vec(words, vector_size=30, window=3, min_count=3, epochs=20, negative=10)
# 输出老番茄的词向量
print(model.wv.get_vector('老番茄'))

# 对词向量进行降维，从而可以画图
raw_word_vec = []
word2index = {}
for i, w in enumerate(model.wv.index_to_key):
    raw_word_vec.append(model.wv[w])
    word2index[w] = i
raw_word_vec = np.array(raw_word_vec)
X_reduced = PCA(n_components=2).fit_transform(raw_word_vec)

# 绘制星空图
# 绘制所有单词向量的二维空间投影
fig = plt.figure(figsize = (15, 10))
ax = fig.gca()
ax.set_facecolor('white')
ax.plot(X_reduced[:, 0], X_reduced[:, 1], '.', markersize = 1, alpha = 0.3, color = 'black')


# 绘制几个特殊单词的向量
words = ['老番茄', '复旦之光', '某幻', '马哥','上海zoo','中国boy','猩猩','花少北','河北首富','下巴']

# 设置中文字体 否则乱码
zhfont1 = matplotlib.font_manager.FontProperties(fname='./华文仿宋.ttf', size=16)
for w in words:
    if w in word2index:
        ind = word2index[w]
        xy = X_reduced[ind]
        plt.plot(xy[0], xy[1], '.', alpha =1, color = 'orange',markersize=10)
        plt.text(xy[0], xy[1], w, fontproperties = zhfont1, alpha = 1, color = 'red')
plt.show()