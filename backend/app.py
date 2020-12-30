from flask import Flask, request, make_response, current_app, jsonify
from functools import update_wrapper
from datetime import timedelta
import pickle
import math
import json

app = Flask(__name__)


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


# 直接获取排名前visulize_range的引用关系
def get_concerned_relations_by_range(reference_relations_counter, visulize_range):
    # 获取引用关系
    relations = reference_relations_counter.most_common(visulize_range)
    max_refer_count = relations[0][1]
    min_refer_count = relations[-1][1]

    return relations, max_refer_count, min_refer_count


# 获取指定诗人群体之间的引用关系，适合画出某个群体内部的网络
def get_concerned_relations_by_authors(reference_relations_counter, authors):
    # 获取指定作者群体内部的引用关系
    relations = []
    max_refer_count = 0
    min_refer_count = 10000
    for (refered_by, refered), count in reference_relations_counter.items():
        # 不统计自引用的count
        if refered_by == refered:
            continue
        if refered_by in authors and refered in authors:
            if count > max_refer_count:
                max_refer_count = count
            if count < min_refer_count:
                min_refer_count = count

            relations.append(((refered_by, refered), count))

    return relations, max_refer_count, min_refer_count


# 生成custom所需数据
def get_all_relations_by_authors(reference_relations_counter, authors):
    # 获取指定作者相关的引用关系
    relations = []
    max_refer_count = 0
    min_refer_count = 10000
    for (refered_by, refered), count in reference_relations_counter.items():
        # 不统计自引用的count
        if refered_by == refered:
            continue
        if refered_by in authors or refered in authors:
            if count > max_refer_count:
                max_refer_count = count
            if count < min_refer_count:
                min_refer_count = count

            relations.append(((refered_by, refered), count))

    return relations, max_refer_count, min_refer_count


# 生成echarts格式的数据
def echarts_data(relations, max_refer_count, min_refer_count, count_to_plot_threshold=1):

    min_link_width = 0.5
    max_link_width = 3.0

    # 因为引用关系的强弱范围很大，对其开方降低变化范围，画图更直观
    max_refer_count = math.sqrt(max_refer_count)
    min_refer_count = math.sqrt(min_refer_count)
    width_slope = (max_link_width - min_link_width) / (max_refer_count - min_refer_count)
    # 格式化links数据
    links_text = ""
    filtered_authors = set()
    for (refered_by, refered), count in relations:
        # 跳过自引用，不然有可能画出孤立节点
        if refered_by == refered:
            continue
        # 小于门限跳过
        if count < count_to_plot_threshold:
            continue

        filtered_authors.add(refered_by)
        filtered_authors.add(refered)
        # count = math.sqrt(count)
        line_width = min_link_width + width_slope * (count - min_refer_count)
        links_text = links_text + '{"source":"' + refered_by + '","target":"' + refered + '",'
        links_text = links_text + '"lineStyle":{"normal":{"width":' + str(line_width) + '}}},'

    # 格式化node数据
    data_text = ""
    for author in filtered_authors:
        data_text = data_text + '{"name":"' + author + '"},'

    data_text = '[' + data_text[:-1] + ']'
    links_text = '[' + links_text[:-1] + ']'
    return data_text, links_text


@app.route('/data', methods=['GET', 'POST'])
@crossdomain(origin='*')
def data():
    print(request.args.get('data'))
    with open('static/reference_relations.pkl', 'rb') as f:
        reference_relations_counter, reference_relations_text = pickle.load(f)
    if request.args.get('data') == 'full':
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_range(reference_relations_counter, 100)
        data_text, link_text = echarts_data(relations, max_refer_count, min_refer_count)
        return jsonify({'data': json.loads(data_text), 'link': json.loads(link_text)})
    elif request.args.get('data') == 'early':
        with open('static/early_tang_poets.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        authors = set(text.split())
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_authors(reference_relations_counter, authors)
        data_text, link_text = echarts_data(relations, max_refer_count, min_refer_count)
        return jsonify({'data': json.loads(data_text), 'link': json.loads(link_text)})
    elif request.args.get('data') == 'high':
        with open('static/high_tang_poets.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        authors = set(text.split())
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_authors(reference_relations_counter, authors)
        data_text, link_text = echarts_data(relations, max_refer_count, min_refer_count)
        return jsonify({'data': json.loads(data_text), 'link': json.loads(link_text)})
    elif request.args.get('data') == 'middle':
        with open('static/middle_tang_poets.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        authors = set(text.split())
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_authors(reference_relations_counter, authors)
        data_text, link_text = echarts_data(relations, max_refer_count, min_refer_count)
        return jsonify({'data': json.loads(data_text), 'link': json.loads(link_text)})
    elif request.args.get('data') == 'late':
        with open('static/late_tang_poets.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        authors = set(text.split())
        relations, max_refer_count, min_refer_count = get_concerned_relations_by_authors(reference_relations_counter, authors)
        data_text, link_text = echarts_data(relations, max_refer_count, min_refer_count)
        return jsonify({'data': json.loads(data_text), 'link': json.loads(link_text)})
    else:
        return null


@app.route('/custom', methods=['GET', 'POST'])
@crossdomain(origin='*')
def custom():
    # 获取关系
    with open('static/reference_relations.pkl', 'rb') as f:
        reference_relations_counter, reference_relations_text = pickle.load(f)
    
    # 获取前端列表
    text = request.args.get('data')[:-1].split(',')
    authors = set(text)

    relations, max_refer_count, min_refer_count = get_all_relations_by_authors(reference_relations_counter, authors)
    data_text, link_text = echarts_data(relations, max_refer_count, min_refer_count)
    return jsonify({'data': json.loads(data_text), 'link': json.loads(link_text)})


@app.route('/select', methods=['GET', 'POST'])
@crossdomain(origin='*')
def select():
    selected = []
    with open('static/early_tang_poets.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    selected.extend(text.split())
    with open('static/high_tang_poets.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    selected.extend(text.split())
    with open('static/middle_tang_poets.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    selected.extend(text.split())
    with open('static/late_tang_poets.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    selected.extend(text.split())
    return jsonify({'res': selected})


if __name__ == '__main__':
    app.run()
