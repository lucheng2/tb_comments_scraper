import dict_util
from segment import TextPreprocessor


class SentimentAnalyzer:
    def __init__(self, stop_words_file=None, user_dict_file=None):
        self.preprocessor = TextPreprocessor(stop_words_file, user_dict_file)

        # 基础情感词典
        self.sentiment_dict = dict_util.obtain_emotional_dict()

        # 程度副词
        self.degree_dict = {
            "极其": 2.0, "非常": 1.8, "特别": 1.6, "相当": 1.5,
            "很": 1.5, "挺": 1.3, "比较": 1.2, "有点": 0.8,
            "稍微": 0.7, "不太": 0.5, "不": -1.0, "没": -1.0
        }

    def analyze_sentiment(self, text):
        """分析单条文本情感"""
        words = self.preprocessor.segment_text(text)

        score = 0
        i = 0
        while i < len(words):
            word = words[i]

            # 检查程度副词
            degree = 1.0
            if word in self.degree_dict:
                degree = self.degree_dict[word]
                # 如果是否定词，处理下一个情感词
                if degree < 0 and i + 1 < len(words):
                    next_word = words[i + 1]
                    if next_word in self.sentiment_dict:
                        score += degree * self.sentiment_dict[next_word]
                        i += 2
                        continue
                i += 1
                continue

            # 检查情感词
            if word in self.sentiment_dict:
                score += degree * self.sentiment_dict[word]
                degree = 1.0  # 重置程度

            i += 1

        # 判断情感
        if score > 0:
            sentiment = "正面"
        elif score < 0:
            sentiment = "负面"
        else:
            sentiment = "中性"

        return {
            "text": text,
            "words": words,
            "score": score,
            "sentiment": sentiment
        }


# 使用示例
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()

    test_reviews = [
        "这个手机非常好用，拍照效果很棒！",
        "质量太差了，非常失望，不建议购买。",
        "产品还不错，但是价格有点贵。",
        "一般般，没什么特别的感觉。"
    ]

    print("=== 情感分析结果 ===")
    for review in test_reviews:
        result = analyzer.analyze_sentiment(review)
        print(f"评论: {result['text']}")
        print(f"分词: {result['words']}")
        print(f"得分: {result['score']} → 情感: {result['sentiment']}")
        print("-" * 50)

