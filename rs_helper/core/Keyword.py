from typing import List


class Keyword:
    """
    A class to symbolize a keyword. A keyword is described by the keyword itself, a rank and the
    keyword extraction algorithm, which was responsible for the creation
    """
    def __init__(self, keyword: List[str], rank: float, algorithm: str = None):
        """
        :param keyword: the tokenized keyword
        :type keyword: list(string)
        :param rank: the keywords rank
        :type rank: float
        :param algorithm: The algorithm that was used to extract the keyword
        :type algorithm: str
        """
        self.keyword = keyword
        self.rank = rank
        self.algorithm = algorithm

    def __str__(self):
        return str(self.keyword) + " | " + str(self.rank) + " | " + str(self.algorithm)

    def __repr__(self):
        return "({}, {})".format(self.keyword, self.rank)

    def __eq__(self, other):
        if self.keyword == other.keyword:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.keyword)
