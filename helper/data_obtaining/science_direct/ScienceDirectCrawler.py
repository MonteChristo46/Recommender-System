import requests
import pandas as pd
import json
import os
from tqdm import tqdm
from helper_functions import find_nth
import re


class ScienceDirectCrawler:

    def __init__(self, query: str, out_dir: str, to_be_num: int = 1000):
        """
        :param query: String (Query that should be searched in science direct (https://dev.elsevier.com/tips/ScienceDirectSearchTips.htm))
        :param out_dir: String (Directory where the resulting files should be stored)
        :param to_be_num: int (Amount of articles to get crawled (Needs to be x times 100))
        """
        if to_be_num % 100 != 0:
            raise ValueError("Number of results must be 100*x")
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        self.query = query
        self.base_url = u'https://api.elsevier.com/content/search/'
        self.base_abstract_url = u'https://api.elsevier.com/content/abstract/eid/'
        self.base_article_url = u'https://api.elsevier.com/content/article/eid/'
        self.scope = "scidir"
        self.url = self.base_url + self.scope + '?query=' + self.query + '&count=100'
        self._status_code = ""
        self.config = self.__load_config()
        self.to_be_num = to_be_num
        self.results = dict()
        self.results["documents"] = list()
        self.total_nums = 0
        self.num_res = 0
        self.out_dir = out_dir

    def run(self):
        """
        :return: void
        General handler of crawling.
        """
        result = self.__exec_request(self.url)
        # self.save_response(result)
        self.__save_relevants_in_results(result, total=True)
        self.total_nums = self.results["total_results"]

        if len(self.results["documents"]) != self.to_be_num:
            while self.num_res < self.total_nums:
                for el in result['search-results']['link']:
                    if el['@ref'] == 'next':
                        next_url = el['@href']
                        result = self.__exec_request(next_url)
                        self.__save_relevants_in_results(result)
                        # self.save_response(result)
                        if len(self.results["documents"]) == self.to_be_num:
                            break
                if len(self.results["documents"]) == self.to_be_num:
                    break

    def save_response(self, res):
        file = open("response_{}.json".format(self.num_res), "w")
        file.write(str(res))
        file.close()

    def __exec_request(self, URL):
        """
        :param URL: String (URL to request)
        :return: dict (Server response)
        This method actually makes the requests and handles the response of the server
        """
        headers = {
            "X-ELS-APIKey": self.config['apikey'],
            "Accept": 'application/json'
        }

        request = requests.get(
            URL,
            headers=headers
        )
        self._status_code = request.status_code

        if request.status_code == 200:
            return json.loads(request.text)
        else:
            return "failed"

    def __save_relevants_in_results(self, exec_result, total: bool = False):
        """
        :param exec_result: Dict (Server response of API request)
        :param total: Boolean (Should the total result num be setted)
        :return: void
        This method stores the relevant information of the server response in the instance results variable
        """
        current_idx = self.num_res
        # print("Current index: {}".format(current_idx))
        self.num_res += len(exec_result['search-results']['entry'])
        # print("[Before saving in results dict] Number of current results: {}".format(self.num_res))
        if total:
            self.results["total_results"] = int(exec_result['search-results']['opensearch:totalResults'])
        for i, doc in enumerate(exec_result['search-results']['entry']):
            date_parts = self.__split_date(doc['prism:coverDate'][0]['$'])
            if "authors" in doc.keys():
                authors = self.__convert_authors(doc["authors"])
            else:
                authors = ""
            self.results["documents"].append(dict())
            self.results["documents"][current_idx+i]["eid"] = doc['eid']
            self.results["documents"][current_idx+i]["title"] = self.__prepare_title(doc["dc:title"])
            self.results["documents"][current_idx+i]["authors"] = authors
            self.results["documents"][current_idx+i]["date"] = doc['prism:coverDate'][0]['$']
            self.results["documents"][current_idx+i]["year"] = date_parts[0]
            self.results["documents"][current_idx+i]["month"] = date_parts[1]
            self.results["documents"][current_idx+i]["day"] = date_parts[2]

    def __get_article_and_abstract(self, eid: str):
        """
        :return: void
        Makes calls to science direct to receive the article and abstracts based on the article eid number.
        """
        eid_url = self.base_article_url+eid
        eid_response = self.__exec_request(eid_url)
        text, abstr = False, False
        if eid_response is not "failed":
            if isinstance(eid_response['full-text-retrieval-response']['originalText'], str):
                idx = self.__get_introduction_index(eid_response['full-text-retrieval-response']['originalText'])
                text = eid_response['full-text-retrieval-response']['originalText'][idx:]
            else:
                text = False
            if isinstance(eid_response['full-text-retrieval-response']['coredata']['dc:description'], str):
                abstr = eid_response['full-text-retrieval-response']['coredata']['dc:description']
            else:
                abstr = False
        return text, abstr

    def __get_introduction_index(self, text: str) -> int:
        """
        :param text: String (The text to be searched)
        :return: int
        This method sould return the index of the SECOND occurrence of "1 Introduction" or "1. Introduction" or ...
        """
        values = ["1 Introduction", "1. Introduction", "1 INTRODUCTION", "1. INTRODUCTION"]
        for v in values:
            idx = find_nth(text, v, 2)
            if idx != -1:
                return idx
        return 0

    def __convert_authors(self, author_dict: dict):
        """
        :param author_dict: dict
        :return: String (The authors)
        Internal function to get the author names of an article
        """
        res = ""
        for i, _ in enumerate(author_dict['author']):
            if "given-name" in author_dict["author"][i].keys() and "surname" in author_dict["author"][i].keys():
                res += author_dict['author'][i]["given-name"] + " " + author_dict['author'][i]["surname"] + ", "
            else:
                res += str(author_dict['author'][i])
        return res

    def __split_date(self, date: str):
        parts = date.split("-")
        return parts

    def __load_config(self):
        """
        :return: void
        Loads configuration file in which the necessary APIKey is stored
        """
        file = open("config.json")
        config_file = json.load(file)
        file.close()
        return config_file

    def __prepare_title(self, input):
        return re.sub(r"[^A-Za-z| ]+", '', input)[:130]

    def save_to_file(self):
        """
        :return: void
        Saves all results to files in the supplied output directory
        """
        abs_errors = 0
        art_errors = 0
        for i, doc in enumerate(tqdm(self.results["documents"])):
            paper, abstract = self.__get_article_and_abstract(doc["eid"])
            file = open(self.out_dir + "[{}] {}.txt".format(doc["date"], doc["title"]), "w")
            file.write("{} - from Authors: {} \n".format(doc["title"], doc["authors"]))
            if abstract:
                file.write("\n\n______ABSTRACT______\n")
                file.write(abstract)
            else:
                abs_errors += 1
            if paper:
                file.write("\n\n______ARTICLE______\n")
                file.write(paper)
            else:
                art_errors += 1
            file.close()
        print("Not saved/found: {} abstracts, {} articles".format(abs_errors, art_errors))

    def save_to_dataframe(self):
        """
        :return: DataFrame
        Saves the results to a pandas dataframe
        """
        titles, years, months, days, authors = list(), list(), list(), list(), list()
        for doc in self.results["documents"]:
            titles.append(doc['title'])
            years.append(doc['year'])
            months.append(doc['month'])
            days.append(doc['day'])
            authors.append(doc['authors'])
        return pd.DataFrame({"title": titles, "years": years, "months": months, "days": days, "author": authors})

    """
        def __get_articles(self):
            errors = 0
            for i, doc in enumerate(tqdm(self.results["documents"])):
                eid = doc["eid"]
                eid_url = self.base_article_url+eid
                eid_response = self.__exec_request(eid_url)
                if eid_response is not "failed":
                    if isinstance(eid_response['full-text-retrieval-response']['originalText'], str):
                        idx = self.__get_introduction_index(eid_response['full-text-retrieval-response']['originalText'])
                        self.results["documents"][i]["article"] = eid_response['full-text-retrieval-response']['originalText'][idx:]
                    else:
                        self.results["documents"][i]["article"] = False
                    self.results["documents"][i]["abstract"] = eid_response['full-text-retrieval-response']['coredata']['dc:description']
                else:
                    self.results["documents"][i]["article"] = False
                    self.results["documents"][i]["abstract"] = False
                    errors += 1
            print("{} Documents could not be found!".format(errors))
        """

    """
        def save_to_file_old(self):
            print("[Before saving to files] Num of documents: {}".format(len(self.results["documents"])))
            file_1 = open("results.json", "w")
            file_1.write(str(self.results))
            abs_errors = 0
            art_errors = 0
            for i, doc in enumerate(self.results["documents"]):
                # paper, abstract = self.__get_article_and_abstract(doc["eid"])
                file = open(self.out_dir + "[{}] {}.txt".format(doc["date"], doc["title"]), "w")
                print(str(i) + " " + str(file) + " " + "[{}] {}.txt"
                      .format(doc["date"], doc["title"]))
                file.write("{} - from Authors: {} \n".format(doc["title"], doc["authors"]))
                if doc["abstract"]:
                    file.write("\n\n______ABSTRACT______\n")
                    file.write(doc["abstract"])
                else:
                    abs_errors += 1
                if doc["article"]:
                    file.write("\n\n______ARTICLE______\n")
                    file.write(doc["article"])
                else:
                    art_errors += 1
            print("Not saved/found: {} abstracts, {} articles".format(abs_errors, art_errors))
        """


if __name__ == "__main__":
    queries = ["Title-Abstr-Key%28Clustering+AND+algorithm%29", "Title-Abstr-Key%28Classification+AND+algorithm%29"]
    dirs = ["clustering", "classification"]
    for q, d in zip(queries, dirs):
        crawler = ScienceDirectCrawler(query=q,
                                       to_be_num=2000,
                                       out_dir="out/{}/".format(d))
        crawler.run()
        crawler.save_to_file()
