from text_info import TextInfo


def main():
    print("How many words should be in top: ")
    top_num = int(input())
    print("Anagram size: ")
    ng_size = int(input())
    with open('data/input.txt', 'r') as f:
        text = f.read()
        ti = TextInfo(text)
        print(f"Median: {ti.get_median()}")
        print(f"Average: {ti.get_mean()}")
        print(f"Top: {ti.get_top_ngrams(top_num, ng_size)}")


main()
