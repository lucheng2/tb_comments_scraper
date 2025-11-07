import jieba
import re
import string
from collections import defaultdict


class TextPreprocessor:
    def __init__(self, stop_words_file="emotional_dictionary/停用词表.txt", user_dict_file=None):
        """
        初始化文本预处理器

        Args:
            stop_words_file: 停用词文件路径
            user_dict_file: 用户自定义词典文件路径
        """
        # 加载停用词
        self.stop_words = set()
        if stop_words_file:
            self.load_stop_words(stop_words_file)

        # 加载用户词典
        if user_dict_file:
            jieba.load_userdict(user_dict_file)

        # 初始化标点符号集合（中文 + 英文）
        self.punctuations = set(string.punctuation + '，。！？；：“”‘’（）【】《》…—～')

    def load_stop_words(self, file_path):
        """加载停用词表"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word:
                        self.stop_words.add(word)
            print(f"已加载 {len(self.stop_words)} 个停用词")
        except FileNotFoundError:
            print(f"停用词文件 {file_path} 未找到，将使用空停用词表")


    def segment_text(self, text, remove_stopwords=True):
        """
        中文分词

        Args:
            text: 输入文本
            remove_stopwords: 是否去除停用词
            use_clean: 是否进行文本清洗

        Returns:
            list: 分词结果列表
        """
        if not text:
            return []

        # 使用jieba分词
        words = jieba.lcut(text)

        # 过滤处理
        filtered_words = []
        for word in words:
            word = word.strip()
            if not word:
                continue

            # 去除标点符号
            if word in self.punctuations:
                continue

            # 去除停用词
            if remove_stopwords and word in self.stop_words:
                continue

            # 过滤单字（可选，根据需求调整）
            # if len(word) == 1:
            #     continue

            filtered_words.append(word)

        return filtered_words

    def batch_segment(self, texts, remove_stopwords=True):
        """
        批量分词处理

        Args:
            texts: 文本列表
            remove_stopwords: 是否去除停用词
            use_clean: 是否进行文本清洗

        Returns:
            list: 分词结果列表的列表
        """
        results = []
        for text in texts:
            segments = self.segment_text(text, remove_stopwords)
            results.append(segments)
        return results


# 示例使用
if __name__ == "__main__":
    # 初始化预处理器（可以传入停用词文件路径）
    preprocessor = TextPreprocessor()

    # 测试文本
    test_texts = [
        "这个手机真的很棒！拍照效果很好，运行流畅。",
        "质量太差了，用了两天就坏了，非常失望！",
        "价格便宜但是质量不太好，总体来说还可以吧。",
        "https://example.com 这个网站的商品很不错，推荐购买！",
        "服务态度<em>很好</em>，快递也很快，五星好评！"
    ]

    print("=== 批量文本分词 ===")
    batch_segments = preprocessor.batch_segment(test_texts)
    for i, (text, seg) in enumerate(zip(test_texts, batch_segments)):
        print(f"文本 {i + 1}: {text}")
        print(f"分词 {i + 1}: {seg}")
        print()