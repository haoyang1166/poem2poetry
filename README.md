# 唐诗诗人社交网络分析与唐诗篇章语义相似度计算与唐诗文本挖掘与诗人地理位置挖掘与诗人主题分析的一些东西
原理：
- [当我们在读唐诗时，我们在读什么？](https://mp.weixin.qq.com/s?__biz=MzI0NTUxMjgyOA==&mid=2247483724&idx=1&sn=9fe912aaaa2757eec2634a95931e1c6a&chksm=e94c2e5fde3ba749e4e364644d6b68d004b295a6864606c79f710b4b0e7e5d07ac3e89481012&mpshare=1&scene=1&srcid=0314cTnPXrmiKE1tR18sIV5m&pass_ticket=LmF1XSUkX6AZUuMnsPEO3vBZgEqfwt9frF%2F%2FATtYfAWYcIhzbawA0%2FclwgYNC1u%2F#rd)
- [计算机告诉你，唐朝诗人之间的关系到底是什么样的？](https://mp.weixin.qq.com/s?__biz=MzI0NTUxMjgyOA==&mid=2247483750&idx=1&sn=dd883b547a3fc4343a3dcce1abea3719&chksm=e94c2e75de3ba7631ffd7abff8a89ea56fda63b2f3d3bb81fd845ef5fd3e9207b41230900288&mpshare=1&scene=1&srcid=0314HdoeYueFNse6H7j18qfx&pass_ticket=P5NYT1vI3xq6gboRVFuq64N9z2Yp0ADF4pMH3nRnXAhGuoM7eROG8O2lhVg%2BIvoR#rd)

相应的，程序也主要有两个方面的功能：
- 分析词频和词向量，对应第一篇文章（我们增加了篇章级的东西）
- 构建诗人之间的引用关系，对应第二篇文章，构建关系没有机器学习，只是进行统计（比较low，如果有人可以加点想法最好了，这个不同于知识图谱中的关系抽取，如果有能力可以做一下两个诗人之间的谓词是什么，是什么关系，在确定二者有关系的时候，进行关系抽取，但是数据应该不够）

程序主要有两个目录：
- data目录，用于存储全唐诗和CBDB数据库
- html目录，存储最终的社交网络关系网页

程序在运算过程中会dump一些中间运算结果，并存储在save目录(如果不存在会自动创建)中。

由于CBDB数据库很大，有499+M。github不允许上传这么大的文件，请大家自行去[CBDB官网](http://projects.iq.harvard.edu/chinesecbdb/%E4%B8%8B%E8%BC%89cbdb%E5%96%AE%E6%A9%9F%E7%89%88)下载单机版数据库，并且以cbdb_sqlite.db为文件名存储在data目录下。
# 依赖库
程序依赖了两个python库
建议使用anaconda
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
- 运行construct_poets_network.py或者word_level_analyzer.py
- save是中间文件,不放心可以自己生成，加了进度条。
- experiment文件夹是实验结果文件夹
- topicmodel文件夹是主题模型中间文件
- ltp_data为哈工大ltp自然语言处理分析包的模型文件
# TODO list
- ~~前端网络展示（改颜色）~~
- ~~展示某些诗人的逻辑，原来是展示早唐，晚唐和全唐的这种拆分，可以改逻辑：查询某个人物的关系~~
- 本文的构建关系网络，仅仅是根据统计诗词之间的人名出现（虽然也很复杂，CBDB数据库是诗人的别称的数据库），可以增加一些其他的方法（hard）
- 设置查询：查询符合某些条件的诗人
- ~~利用word2vec判断篇章embedding~~，对仗，~~篇章级相似度~~
- ~~篇章级相似度分为几种方法：简单的词embedding加和，或者逐句最大词加和，lstm，vae，bert等等（可以写一个类）~~

- ~~embedding表示不好，分词不好的解决方案：~~~~1.直接用GuwenBert 拿到embedding表示；
2.将GuwenBert 训好之后在加上对诗词的分类，标签是作者，直接fine- tuning。~~（基于roBert的参数，找fine-tuning分类的代码相应的）
~~中间表示就是包含了诗人写作的语义信息的embedding，具体在那层不太懂。测试集：自己写一首诗去分类你属于哪个作者~~

# 项目延展
- 对应风格的唐诗生成（训练集应该得需要额外找，属于nlp项目了）  https://github.com/jinfagang/tensorflow_poems https://github.com/DevinZ1993/Chinese-Poetry-Generation
- **唐诗风格聚类**（有了embedding做个聚类不是很简单的事情么）
- ~~其余NLP类似问题，诗词分类（比如判断这诗是哪个人写的，变相的包含了语义信息）诗词情感分析？做一个风格预测~~
- 利用atm主题模型取分析每个作者的写作主题特征(已完成，还待优化，目前只降维表示了，还有待聚类)
- 增加了命名实体识别，看一下诗人历史上去过哪些地方（配合他写作的词频等东西再分析一波？）
# 下一步计划
- ~~重新实现max- Pooling词向量（简单的），因为词向量平均是不正确的~~（已经写完但是行不通，仍然相似度很高，但是相对相似度还是有意义的）
- ~~guwenbert实现，或者w2v变体（icml2014，acl2014），或者有下游任务的lstm拼接，或者vae ，encoder- decoder~~(这些不想做了，感觉bert训没意义，样本太少直接
建模从诗到诗人的分类映射没意义，直接拿feature估计也和词向量差不多)
- 构建相似度矩阵，相似度用什么来衡量是个问题，tf-idf也可以（用一个词表大小的embedding也可以），每个位置是对应词频，词向量（想基于语义）加和平均很平滑，以及基于上面方法的相似度计算
- ~~写一个词分析类，以方便的进行传模型和数据并分析。~~

- ~~在类中写：其他方法提取篇章特征，篇章就是一个词向量矩阵；CNN去提取；变分自编码去做篇章；从一个特定任务中去提取表示bert，cnn都是这种的；~~(同上
这些只是词向量如何到诗向量的方法，没啥意义)

# 重新思考
- ~~词向量加和还是错的，~~~~但是max-pooling还是可以的~~（已经写完但是行不通，仍然相似度很高，但是相对相似度还是有意义的）
- ~~词向量到篇章还是通过cnn bilstm vac等方法有个下游任务，反向中间结果生成的，或者bert的预训练的embedding。~~
