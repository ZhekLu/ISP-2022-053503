import re
import statistics

from collections import Counter


class TextInfo:
    def __init__(self, text: str):
        self._sentences = None
        self._words_num = None
        self.text = text.lower()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        sentences = [i for i in re.split(r'[.!?;]', value) if i != '']
        self._sentences = list(map(lambda x: [i for i in re.split(r'\W', x) if i != ''], sentences))

        self._words_num = [len(i) for i in self._sentences]

    def get_mean(self):
        return statistics.mean(self._words_num)

    def get_median(self):
        return statistics.median(self._words_num)

    def get_top_ngrams(self, top_size: int, ngram_size: int) -> list:
        c = Counter()
        for sentence in self._sentences:
            for word in sentence:
                if len(word) < ngram_size:
                    continue
                for i in range(len(word) - ngram_size + 1):
                    c[word[i:i + ngram_size]] += 1
        return c.most_common(top_size)
