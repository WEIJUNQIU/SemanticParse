#! /usr/bin/python
# coding=utf-8

import traceback
import StringIO
import os,sys
import re
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/utils/')
import jieba

import logging
logger = logging.getLogger(os.path.splitext(__file__)[0])

class text_segment():
    def __init__(self):
        try:
            self.stopwords = {}.fromkeys(
                    [line.strip().decode('utf-8') for line
                        in open(os.path.dirname(os.path.realpath(__file__)) + '/dict/stopwords_new.txt')])
            self.stopwords = set(self.stopwords.keys())
        except:
            fp = StringIO.StringIO()
            traceback.print_exc(file=fp)
            message = fp.getvalue()
            logger.warning("[Analizer] stopwords file error!\n%s" % (message))
            self.stopwords = {}
        self.load_synonyms()

    def load_synonyms(self):
        '''
        读取同义词典
        self.words_to_synonym: {WordA:MainWordA, WordB:MainWordA, WordC:MainWordE, WordD:MainWordE...}
        self.synonyms_group: KEY-groupid Value-[WordA, WordB, WordC]
        '''
        self.words_to_synonym = {}
        self.synonyms_group = {}

    def get_ch_words_list(self, text, is_cut_all=False, is_del_stopword=True, is_merge_synonym=False):
        '''
        输入：str
        输出：分词结果list
        '''
        words_list = jieba.cut(text, cut_all=is_cut_all)
        return self.transform(words_list, is_del_stopword, is_merge_synonym)

    def transform(self, words_list, is_del_stopword, is_merge_synonym):
        '''
        处理分词结果
        '''
        # 转换大写
        words_list = [w.lower() for w in words_list]

        # 过滤停用词、合并同义词
        if is_del_stopword:
            words_list = [w for w in words_list if w not in self.stopwords and not is_numeric(w)]
            #words_list = [w for w in words_list if w not in self.stopwords]
        if is_merge_synonym:
            words_list = [self.words_to_synonym.get(w, w) for w in words_list]
        return words_list

    def get_phone_num_list(self, phone):
        '''
        输入：包含电话号码的字符串
        输出：电话号码列表（不含区号）
        '''
        pattern = re.compile(r'\d{5,}|[48]00-\d{3}-\d{4}|')
        match = pattern.findall(phone)
        try:
            match = [m for m in match if m != '']
        except:
            match = []
        return match

def is_numeric(w):
    try:
        float(w)
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    a = text_segment()
    text = u'''
    苏州团购: 仅售9.9元！原价最高108元的嘉乐飚歌城任意时段欢唱 唱歌 一小时（豪华VIP包厢不在此活动内）！每包厢每次最多使用2张拉手券！
    吃披萨，匹萨，比萨...川菜 香锅 四川菜
        '''
    print text
    words = a.get_ch_words_list(text, is_merge_synonym=True)
    print '\n'.join(words)
