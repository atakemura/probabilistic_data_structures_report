# coding: utf-8


def zipf(N, k, s):
    """
    :param N: 要素の数
    :param k: 要素のランク(順位)
    :param s: zipf分布のパラメータ
    :return: その要素の出現頻度
    """
    return (1./k**s)/sum(1./n**s for n in xrange(1, N+1))


def gen_zipf(num_elem, shape_param, out_len):
    """
    :param num_elem: 要素の数
    :param shape_param: zipf分布のパラメータ
    :param out_len: 結果の長さ
    :return: 整数の配列
    """
    result = []
    for rank in xrange(1, num_elem + 1):
        freq = zipf(num_elem, rank, shape_param)
        num = int(round(freq * out_len))
        for i in range(num):
            result.append(rank)
    return result

dataset = gen_zipf(1000, 0.7, 100000)