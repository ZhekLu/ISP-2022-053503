import statistics
from collections import Counter
import re


class TextInfo:
    def __init__(self, text: str):
        self.text = text.lower()
        self.__prepare()

    def __prepare(self):
        sentences = [i for i in re.split(r'[.!?;]', self.text) if i != '']
        self.sentences = list(map(lambda x: [i for i in re.split(r'\W', x) if i != ''], sentences))

        self.words_num = [len(i) for i in self.sentences]

    def set_text(self, text: str):
        self.__init__(text)

    def get_mean(self):
        return statistics.mean(self.words_num)

    def get_median(self):
        return statistics.median(self.words_num)

    def get_top_ngrams(self, top_size: int, ngram_size: int):
        c = Counter()
        for sentence in self.sentences:
            for word in sentence:
                if len(word) < ngram_size:
                    continue
                for i in range(len(word) - ngram_size + 1):
                    c[word[i:i + ngram_size]] += 1
        return c.most_common(top_size)
