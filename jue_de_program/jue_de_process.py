import re

def extract_last_word_after_more_from_file(filename):
    results = []
    with open(filename, mode='r', encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("more"):
            # 找到最後一個標點符號
            last_punctuation_index = max(line.rfind('。'), line.rfind('？'), line.rfind('！'),  line.rfind('；'), line.rfind('：'), line.rfind('，'))
            # 如果有標點符號，取出標點符號後的句子
            if last_punctuation_index != -1:
                last_sentence = line[last_punctuation_index + 1:].strip()
                if last_sentence:
                    results.append(last_sentence)
            else:
                # 如果沒有標點符號，取出more後面的完整句子
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
    
    # 檢查文件的最後一行由甚麼開頭
    with open(filename, mode='r', encoding="utf-8") as f:
        last_line = f.readlines()[-1]
        if last_line.startswith("more"):
            parts = re.split('[，。？！、；：]', last_line)
            for part in parts:
                if keyword in part:
                    last_sentences.append(part.strip('，。？！、；：'))
    
    # 合併句子
    merged_sentences = []
    for first_sentence, last_sentence in zip(first_sentences, last_sentences):
        merged_sentence = first_sentence + last_sentence
        merged_sentences.append(merged_sentence)
    
    return merged_sentences

def remove_whitespace(text):
    # 把所有空格刪除
    return re.sub(r'\s', '', text)

# 處理文字檔案
filename = "jue_de_raw.txt"
keyword = "覺得"
merged_sentences = merge_sentences(filename, keyword)

# 將處理過的句子寫到新的文件 jue_de_cleaned.txt 中
output_filename = "jue_de_cleaned.txt"
with open(output_filename, mode='w', encoding='utf-8') as f:
    for sentence in merged_sentences:
        sentence_without_whitespace = remove_whitespace(sentence)
        f.write(sentence_without_whitespace + '\n')
        print(sentence_without_whitespace)
        
print("已保存處理過的文檔:", output_filename)
