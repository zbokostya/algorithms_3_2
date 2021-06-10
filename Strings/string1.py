def brute_force(text, pat):
    n = len(text)
    m = len(pat)

    if m == 0:
        return 0

    for i in range(n - m):
        k = 0
        while k < m and text[i + k] == pat[k]:
            k += 1
        if k == m:
            return i

    return -1


if __name__ == '__main__':
    print(brute_force("dfdf123dfdfd", "123"))