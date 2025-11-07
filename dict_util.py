def read_emotional_dict(file_path):
    """读取负面词典文件，返回字符串集合"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取所有行，去除每行的换行符，并转换为集合
            words_set = set(line.strip() for line in file if line.strip())
        return words_set
    except FileNotFoundError:
        print(f"错误：文件 {file_path} 未找到")
        return set()
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return set()


def obtain_emotional_dict() -> dict:
    neg_words = read_emotional_dict("emotional_dictionary/neg_all_dict.txt")
    pos_words = read_emotional_dict("emotional_dictionary/pos_all_dict.txt")
    result = {}
    for neg in neg_words:
        result[neg] = -1
    for pos in pos_words:
        result[pos] = 1
    return result


# 使用示例
if __name__ == "__main__":
    # file_path = "emotional_dictionary/neg_all_dict.txt"
    # neg_words = read_emotional_dict(file_path)
    # print(f"读取到 {len(neg_words)} 个词语")
    # print("词语集合：", neg_words)
    res = obtain_emotional_dict()
    print(f'读取心情词典个数：{len(res)}')
    print(f'读取心情词典数据：{res}')


