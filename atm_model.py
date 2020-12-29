import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models import AuthorTopicModel
from sklearn.cluster import KMeans
from gensim import corpora
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt


class AuthorMining:
    def __init__(self, corpus):
        self.corpus = corpus

    # '''构造训练语料'''
    # def build_corpus(self):
    #     f = open('corpus_train.txt', 'w+')
    #     count = 0
    #     for item in self.db.find():
    #         count += 1
    #         print(count)
    #         author = item['author']
    #         content = [i.split('/')[0] for i in item['seg_content'] if i.split('/')[-1] not in ['w']]
    #         f.write(author + '\t' + ' '.join(content) + '\n')
    #     f.close()

    '''进行atm模型'''

    def atm_model(self):
        docs = []
        author2doc = {}
        index = 0
        for line in open(self.corpus, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            author = line.split('\t')[0]
            if author not in author2doc:
                author2doc[author] = [index]
            else:
                author2doc[author].append(index)

            doc = line.split('\t')[1].replace("，", "").replace("。", "").split(' ')
            docs.append(doc)
            index += 1
        print(len(docs))
        # 构建词典
        dictionary = corpora.Dictionary(docs)
        # 对文本进行向量化
        corpus = [dictionary.doc2bow(doc) for doc in docs]
        # 使用atm模型进行训练
        model = AuthorTopicModel(corpus, author2doc=author2doc, id2word=dictionary, num_topics=100)
        # 保存模型
        model.save('topicmodel/author_topic.model')

    '''加载训练好的authormodel进行测试'''

    def test_model(self):
        model = AuthorTopicModel.load('topicmodel/author_topic.model')
        # 每个作者的向量，每个作者向量维度不一样，对应的主题不一样，主题分别是概率。
        author_vecs = [model.get_author_topics(author) for author in model.id2author.values()]
        print(len(author_vecs))  # 2610个诗人，每个诗人有几个主题（<100）,之后对应的概率
        for author in author_vecs:
            print(author, len(author))  # 每个作者身上的主题个数不同
        # 介绍每位作者
        authors = model.id2author.values()
        print(len(authors), authors)
        # 显示某位作者的向量
        print(model['李白'])
        # 显示模型主题
        for topic in model.show_topics(num_topics=100):
            print(topic)

    '''对作者进行聚类分析'''

    def tsne_clusting(self):
        model = AuthorTopicModel.load('topicmodel/author_topic.model')
        tsne = TSNE(n_components=2, random_state=0)
        smallest_author = 200  # 想看最少写作数量多少的诗人
        authors = [model.author2id[a] for a in model.author2id.keys() if len(model.author2doc[a]) >= smallest_author]
        print(authors)
        embeddings = tsne.fit_transform(model.state.gamma[authors, :])
        # print(model.state.gamma[authors, :])
        # print(embeddings)
        authors_list = [model.id2author[k] for k in authors]

        print(authors_list)

        # plt.scatter(embeddings[:, 0], embeddings[:, 1], c=y_predict)
        #
        # plt.show()

        # labels = ['李世民', '李白', '白居易', '武则天', '白居易', '杜甫', '刘禹锡', '武元衡', '权德舆']#对应的需要查找某几个诗人的方法
        # author_ids = [model.author2id[author] for author in labels]
        # print(author_ids)
        # author_embs = tsne.fit_transform([embeddings[i] for i in author_ids])
        # print(author_embs)
        # print(authors, author_ids, author_embs)

        self.plot_with_labels(embeddings, authors_list)  # 在这里该以下对应诗人的

        # plot_only = 150
        # embeddings = model.state.gamma[authors, :plot_only]
        #
        # low_dim_embs = tsne.fit_transform(embeddings[:plot_only, :])
        # labels = [authors[i] for i in range(plot_only)]
        # self.plot_with_labels(low_dim_embs, labels)

    '''对二维embedding进行展示'''

    def plot_with_labels(self, low_dim_embs, labels, filename='authors.png'):
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.figure(figsize=(18, 18))  # in inches
        kmeans = KMeans(n_clusters=3, random_state=10)
        kmeans.fit(low_dim_embs)
        y_predict = kmeans.predict(low_dim_embs)
        color_list=[]
        for y in y_predict:
            if y ==0:
                color ="r"
            elif y==1:
                color="b"
            elif y==2:
                color="g"
            color_list.append(color)

        # plt.scatter(low_dim_embs[:, 0], low_dim_embs[:, 1], c=y_predict)
        # plt.annotate(labels,
        #              xy=(low_dim_embs[:, 0], low_dim_embs[:, 1]),
        #              xytext=(5, 2),
        #              textcoords='offset points',
        #              ha='right',
        #              va='bottom')
        # plt.show()

        for i, (label, y_p) in enumerate(zip(labels, color_list)):
            # print(labels)
            x, y = low_dim_embs[i, :]
            plt.scatter(x, y, c=y_p)
            # print(y_p)
            plt.annotate(label,
                         xy=(x, y),
                         xytext=(5, 2),
                         textcoords='offset points',
                         ha='right',
                         va='bottom')

        plt.savefig(filename)


def main():
    handler = AuthorMining("save/ats_words_list.txt")
    # handler.atm_model()
    # handler.test_model()
    handler.tsne_clusting()
    # handler.test_model()


if __name__ == '__main__':
    main()
