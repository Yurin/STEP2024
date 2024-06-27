import sys
import collections
import numpy as np

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = None
        goal_id = None
        for id, title in self.titles.items():
            if title == start:
                start_id = id
            if title == goal:
                goal_id = id
        
        if start_id is None or goal_id is None:
            return "Start or goal page not found."

        queue = collections.deque([[start_id]])
        visited = set()
        visited.add(start_id)

        while queue:
            path = queue.popleft() #キューから現在のパスを取り出す
            node = path[-1] #探索終点のページIDを入れる

            if node == goal_id:
                return [self.titles[id] for id in path]

            for neighbor in self.links[node]:#隣接ノードを探す
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)

        return "Path not found"


    # ページランクを計算して最も人気のあるページを出力する
    def find_most_popular_pages(self):
        damping_factor = 0.85  # ランダムに次のページに移動する確率
        max_iter = 1  # 反復回数の最大を100に固定
        tol = 1e-6  # 許容誤差

        num_pages = max(self.titles.keys()) + 1  # ページIDの最大値 + 1で配列サイズを設定

        rank = np.ones(num_pages)  # 各ページの初期ランクを1に設定
        new_rank = np.zeros(num_pages)  # 新しいランクを格納するための配列

        for iteration in range(max_iter):
            #cnt = 0
            new_rank.fill((1 - damping_factor) * num_pages / num_pages)  # ベースラインのランクを設定

            for page, outlinks in self.links.items():
                if outlinks:
                    share = rank[page] / len(outlinks)#ランクのシェアを計算。
                    for outlink in outlinks:
                        new_rank[outlink] += damping_factor * share#リンク先のページにダンピングファクターを掛けたシェアを加算
                else:
                    new_rank += damping_factor * rank[page] / num_pages#リンクがない場合現在のページランクをすべてのページに均等に分配。

            if np.linalg.norm(new_rank - rank, ord=1) < tol:
                break  # ランクと前のランクのL1ノルムの差が許容誤差より小さいとき終了

            rank = new_rank.copy()#現在のランクを新しいランクに更新
            #cnt = cnt + 1
        #print("count =",cnt)

        # ランクの値の合計が num_pages になるように正規化
        rank = rank * num_pages / np.sum(rank)

        ranked_indices = np.argsort(-rank)
        print("最も人気のあるページトップ10は以下の通りです:")
        displayed_count = 0
        for index in ranked_indices:
            if index in self.titles:
                print(f"{self.titles[index]}: {rank[index]:.6f}")
                displayed_count += 1
                if displayed_count >= 10:
                    break
        print()



    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()