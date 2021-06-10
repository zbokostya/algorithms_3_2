class KMP:
    def __init__(self, pat):
        self.pat = pat
        self.dfa = []
        self.buffer_size = 100

    def kmp(self, text):
        chunk = text.read(self.buffer_size)
        while chunk:
            yield chunk
            chunk = text.read(self.buffer_size)

    def search(self, text):
        rez = -1
        for k, texta in enumerate(self.kmp(text)):
            n = len(texta)
            m = len(self.pat)
            for i in range(n - m):
                j = 0
                while j < m:
                    if texta[i + j] != self.pat[j]:
                        break
                    j += 1
                if j == m:
                    rez = k * self.buffer_size + i
        return rez


if __name__ == '__main__':
    kmp = KMP("123")
    with open("/Users/kostyaz/dev/univer/alg_7sem/salessman/text.txt", "r") as abc:
        offset = kmp.search(abc)
        print(offset)
