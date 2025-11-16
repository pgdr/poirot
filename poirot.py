"""Given the following ranking of Poirot episodes:

https://bibliollcollege.substack.com/p/every-episode-of-agatha-christies

create a longest possible chain of episodes to watch such that you watch
episodes chronologically, and in increasing quality.

"""

import csv
from collections import namedtuple, defaultdict

Episode = namedtuple("Episode", "rank title season episode")


def episode(e):
    return Episode(int(e["rank"]), e["title"], int(e["season"]), int(e["episode"]))


def read_episodes(path):
    with open(path, "r") as f:
        return [episode(row) for row in csv.DictReader(f)]


def earlier(ep1, ep2):
    return (ep1.season, ep1.episode) < (ep2.season, ep2.episode)


def successor(ep1, ep2):
    return ep2.rank < ep1.rank and not earlier(ep2, ep1)


def build_graph(episodes):
    inneighbors = defaultdict(list)
    for e1 in episodes:
        for e2 in episodes:
            if e1 == e2:
                continue
            if successor(e1, e2):
                inneighbors[e2].append(e1)

    return inneighbors


def longest_path(episodes, inneighbors):
    dp = defaultdict()
    for ep in episodes:
        preds = inneighbors[ep]
        dp[ep] = 1 + max(dp[p] for p in preds) if preds else 1

    best_ep = None
    best_len = 0
    for ep in episodes:
        length = dp[ep]
        if length > best_len:
            best_len = length
            best_ep = ep

    path = [best_ep]
    c_ep = best_ep
    c_len = best_len

    while c_len > 1:
        for p in inneighbors[c_ep]:
            if dp[p] == c_len - 1:
                path.append(p)
                c_ep = p
                c_len -= 1
                break

    return tuple(reversed(path))


def main():
    fname = "poirot.csv"
    episodes = read_episodes(fname)
    inneighbors = build_graph(episodes)
    path = longest_path(episodes, inneighbors)

    for idx, ep in enumerate(path):
        print(1 + idx, f"{ep.rank:02d}. {ep.title} (S{ep.season:02d}E{ep.episode:02d})")


if __name__ == "__main__":
    main()
