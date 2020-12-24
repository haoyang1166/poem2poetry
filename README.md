# 全唐诗分析程序
原理：
- [当我们在读唐诗时，我们在读什么？](https://mp.weixin.qq.com/s?__biz=MzI0NTUxMjgyOA==&mid=2247483724&idx=1&sn=9fe912aaaa2757eec2634a95931e1c6a&chksm=e94c2e5fde3ba749e4e364644d6b68d004b295a6864606c79f710b4b0e7e5d07ac3e89481012&mpshare=1&scene=1&srcid=0314cTnPXrmiKE1tR18sIV5m&pass_ticket=LmF1XSUkX6AZUuMnsPEO3vBZgEqfwt9frF%2F%2FATtYfAWYcIhzbawA0%2FclwgYNC1u%2F#rd)
- [计算机告诉你，唐朝诗人之间的关系到底是什么样的？](https://mp.weixin.qq.com/s?__biz=MzI0NTUxMjgyOA==&mid=2247483750&idx=1&sn=dd883b547a3fc4343a3dcce1abea3719&chksm=e94c2e75de3ba7631ffd7abff8a89ea56fda63b2f3d3bb81fd845ef5fd3e9207b41230900288&mpshare=1&scene=1&srcid=0314HdoeYueFNse6H7j18qfx&pass_ticket=P5NYT1vI3xq6gboRVFuq64N9z2Yp0ADF4pMH3nRnXAhGuoM7eROG8O2lhVg%2BIvoR#rd)

相应的，程序也主要有两个方面的功能：
- 分析词频和词向量，对应第一篇文章
- 构建诗人之间的引用关系，对应第二篇文章，构建关系没有机器学习，只是进行统计（比较low，如果有人可以加点想法最好了，这个不同于知识图谱中的关系抽取，如果有能力可以做一下两个诗人之间的谓词是什么，是什么关系，在确定二者有关系的时候，进行关系抽取，但是数据应该不够）

程序主要有两个目录：
- data目录，用于存储全唐诗和CBDB数据库
- html目录，存储最终的社交网络关系网页

程序在运算过程中会dump一些中间运算结果，并存储在save目录(如果不存在会自动创建)中。

由于CBDB数据库很大，有499+M。github不允许上传这么大的文件，请大家自行去[CBDB官网](http://projects.iq.harvard.edu/chinesecbdb/%E4%B8%8B%E8%BC%89cbdb%E5%96%AE%E6%A9%9F%E7%89%88)下载单机版数据库，并且以cbdb_sqlite.db为文件名存储在data目录下。
# 依赖库
程序依赖了两个python库
``` shell
pip3 install thulac
pip3 install gensim
```
其中thulac用于分词，gensim用于word2vec.
这两个库只用于第一篇文章的分析。如果您只关心如何构建诗人关系网络，那么不需要安装这个两个库。

# 基本用法
- 运行`python3 word_level_analyzer.py`来复现第一篇文章的结果
- 运行`python3 construct_poets_network.py`来构建社交网络，并将运行结果存储在save目录。
- 运行`python3 visualize_poets_network.py`来构建出显示社交网络的网页，并将结果存储在html目录。
# 开发逻辑
db文件只是用来查找相应的别名(但是里面仍有很多数据可以挖掘)
-运行construct_poets_network.py或者word_level_analyzer.py
-save是中间文件,不放心可以自己生成，加了进度条。

# TODO list
- ~~构建关系网前端的修改~~
- ~~展示某些诗人的逻辑，原来是展示早唐，晚唐和全唐的这种拆分，可以改逻辑：查询某个人物的关系~~
- 本文的构建关系网络，仅仅是根据统计诗词之间的人名出现（虽然也很复杂，CBDB数据库是诗人的别称的数据库），可以增加一些其他的方法（hard）
- 查找某一索引查询下的东西，比如看一下经历过安史之乱的，或着某些诗人的关系，不一定非得晚唐，早唐这类的
- ~~利用word2vec相似度判断两者有无关系，或者是知道关系之后验证以下二者写的诗是否相似，分析词频~~，对仗，~~甚至是篇章级相似度~~
- ~~篇章级相似度分为几种方法：简单的词embedding加和，或者逐句最大词加和，等等（可以写一个类）~~
- ~~古文本分词说实话直接调用thulac分词效果不太好，甚至embedding也根本没有语义信息~~
- 解决方案：1.GuwenBert 把模型看懂，前几层应该有embedding生成（猜测的因为bert可以生成w2v,也可以fine-tuing）
-         2.将GuwenBert 训好之后在加上对诗词的分类，标签是作者，自己写一首诗去分类你属于哪个作者
# 项目延展
- 对应风格的唐诗生成（训练集应该得需要额外找，属于nlp项目了），https://github.com/jinfagang/tensorflow_poems https://github.com/DevinZ1993/Chinese-Poetry-Generation
- 唐诗风格聚类（有了embedding做个聚类不是很简单的事情么）
- 其余NLP类似问题，诗词分类？诗词分词优化？诗词情感分析？（数据呢？）,做一个风格预测
# 下一步计划
- 简单的对篇章级进行了识别，加和求平均，但是相似度都比较高，有可能是词向量过大，导致过拟合。
- 构建相似度矩阵，目前仅仅实现了给定两个诗人的唐诗相似度计算（相似度用什么来衡量是个问题，仅仅是根据词频也可以，但是计算每个诗人的可以重新改写Count方式，另一种方法
直接构建embedding,就是现在用的）
- 写一个词分析类，以方便的进行传模型和数据并分析。
- 增加了实验结果文件下，分词和w2v训一次太慢，以便以后写文档
- 准备做一下解决方案 2 GuwenBert