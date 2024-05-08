import re

def extract_last_word_after_more_from_file(filename):
    results = []
    with open(filename, mode='r', encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("more"):
            # 找到最后一个标点符号的索引
            last_punctuation_index = max(line.rfind('。'), line.rfind('？'), line.rfind('！'),  line.rfind('；'), line.rfind('：'), line.rfind('，'))
            # 如果最后一个标点符号存在，取出最后一个标点符号后的句子
            if last_punctuation_index != -1:
                last_sentence = line[last_punctuation_index + 1:].strip()
                if last_sentence:
                    results.append(last_sentence)
            else:
                # 否则，取出 "more" 后的内容
                results.append(line[4:].strip())
    return results

def extract_sentences_with_keyword(filename, keyword):
    with open(filename, mode='r', encoding="utf-8") as f:
        text = f.read()

    result = []
    # 將換行符號後的文字與「覺得」之後的文字合併成一行，然後再進行切割
    lines = re.split('\n', text)
    for line in lines:
        if keyword in line:
            parts = re.split('[，。？！、；：]', line)
            for part in parts:
                if keyword in part:
                    result.append(part.strip('，。？！、；：'))
    
    return result

def merge_sentences(filename, keyword):
    first_sentences = extract_last_word_after_more_from_file(filename)
    last_sentences = extract_sentences_with_keyword(filename, keyword)
    
    # 检查文件的最后一行是否以关键字开头
    with open(filename, mode='r', encoding="utf-8") as f:
        last_line = f.readlines()[-1]
        if last_line.startswith("more"):
            parts = re.split('[，。？！、；：]', last_line)
            for part in parts:
                if keyword in part:
                    last_sentences.append(part.strip('，。？！、；：'))
    
    # 合并句子
    merged_sentences = []
    for first_sentence, last_sentence in zip(first_sentences, last_sentences):
        merged_sentence = first_sentence + last_sentence
        merged_sentences.append(merged_sentence)
    
    return merged_sentences

def remove_whitespace(text):
    # 使用正则表达式替换所有空格为 ""
    return re.sub(r'\s', '', text)

# 使用示例:
filename = "jue_de_raw.txt"
keyword = "覺得"
merged_sentences = merge_sentences(filename, keyword)

# 将处理后的句子写入到新的文件 jue_de_cleaned.txt 中
output_filename = "jue_de_cleaned.txt"
with open(output_filename, mode='w', encoding='utf-8') as f:
    for sentence in merged_sentences:
        sentence_without_whitespace = remove_whitespace(sentence)
        f.write(sentence_without_whitespace + '\n')
        print(sentence_without_whitespace)
        
print("处理后的句子已保存到文件:", output_filename)
