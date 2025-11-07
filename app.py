from flask import Flask, render_template, jsonify, request

import query_script
from sentiment_classifier import SentimentAnalyzer

app = Flask(__name__)


# 模拟商品数据
def get_products():
    all_ids = query_script.query_all_id()
    result = []
    for product_id in all_ids:
        result.append({'id': product_id})
    return result


# 根据商品ID获取饼图数据
def get_chart_data(product_id):
    comment_analyse_result = get_comment_analyse_result(product_id)
    result = count_sentiments(comment_analyse_result)
    return {
        'labels': list(result.keys()),
        'data': list(result.values()),
        'colors': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
    }


def count_sentiments(data_list):
    """
    统计sentiment个数
    """
    sentiment_count = {
        "正面": 0,
        "负面": 0,
        "中性": 0
    }

    for item in data_list:
        sentiment = item.get("sentiment")
        if sentiment in sentiment_count:
            sentiment_count[sentiment] += 1
    return sentiment_count

def get_comment_analyse_result(product_id):
    comment_data_list = query_script.query_all_data_by_key(product_id)
    comments_list = []
    for key in comment_data_list:
        comments_list.append(comment_data_list[key]["comment"])
    print(comments_list)
    analyzer = SentimentAnalyzer()
    comment_analyse_result = []
    for review in comments_list:
        result = analyzer.analyze_sentiment(review)
        comment_analyse_result.append(result)
    return comment_analyse_result


# 根据商品ID获取评论数据
def get_review_data(product_id):
    comment_analyse_result = get_comment_analyse_result(product_id)
    return comment_analyse_result

@app.route('/')
def products_page():
    """商品列表页面"""
    products = get_products()
    return render_template('products.html', products=products)


@app.route('/chart')
def chart_page():
    """饼图页面"""
    product_id = request.args.get('product_id', 'P001')
    return render_template('index.html', product_id=product_id)

@app.route('/detail')
def detail_page():
    """商品详情页面"""
    product_id = request.args.get('product_id', 'P001')
    reviews = get_review_data(product_id)
    return render_template('detail.html', product_id=product_id, reviews=reviews, product_name="情感分析")


@app.route('/api/chart-data')
def chart_data():
    """API：获取饼图数据"""
    product_id = request.args.get('product_id', 'P001')
    chart_data = get_chart_data(product_id)
    return jsonify(chart_data)

@app.route('/api/review-data')
def review_data():
    """API：获取评论数据"""
    product_id = request.args.get('product_id', 'P001')
    reviews = get_review_data(product_id)
    return jsonify(reviews)

@app.route('/api/products')
def products_data():
    """API：获取商品列表"""
    products = get_products()
    return jsonify(products)


if __name__ == '__main__':
    app.run(debug=True)