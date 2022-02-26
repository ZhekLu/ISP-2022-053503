import statistics
from collections import Counter
import re


class TextInfo:
    def __init__(self, text: str):
        self.text = text.lower
        self.__prepare()

    def __prepare(self):
        sentences = [i for i in re.split(r'[.!?;]', self.text) if i != '']
        sentences = list(map(lambda x: [i for i in re.split(r'\W', x) if i != ''], sentences))

        self.words_num = [len(i) for i in sentences]

        c = Counter()
        for sentence in sentences:
            c.update(Counter(sentence))
        self.words_dict = dict(c)

    def set_text(self, text: str):
        self.__init__(text)

    def get_mean(self):
        return statistics.mean(self.words_num)

    def get_median(self):
        return statistics.median(self.words_num)
