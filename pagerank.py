import random
import os
import re

DAMPING = 0.85
SAMPLES = 10000

def crawl(directory):
    
    #Parse a directory of HTML pages and check for links to other pages.Return a dictionary where each key is a page.
    
    pages = dict()

    #Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    #Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )
    
    return pages

def transition_model(corpus, page, damping_factor):
    N = len(corpus)
    transition_probabilities = {}

    if not corpus[page]:
        corpus[page] = set(corpus.keys())

    for target_page in corpus:
        probability = (1 - damping_factor) / N
        if target_page in corpus[page]:
            probability += damping_factor / len(corpus[page])
        transition_probabilities[target_page] = probability

    return transition_probabilities

def sample_pagerank(corpus, damping_factor, n):
    page_rank = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus.keys()))

    for _ in range(n):
        page_rank[current_page] += 1
        transition_probabilities = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(transition_probabilities.keys()), weights=transition_probabilities.values())[0]

    total_samples = sum(page_rank.values())
    page_rank = {page: rank / total_samples for page, rank in page_rank.items()}

    return page_rank

def iterate_pagerank(corpus, damping_factor):
    N = len(corpus)
    initial_rank = 1 / N
    page_rank = {page: initial_rank for page in corpus}
    change_threshold = 0.001

    while True:
        new_page_rank = {}
        for page in corpus:
            new_rank = (1 - damping_factor) / N
            for linking_page, links in corpus.items():
                if page in links:
                    new_rank += damping_factor * (page_rank[linking_page] / len(links))
            new_page_rank[page] = new_rank

        max_change = max(abs(new_page_rank[page] - page_rank[page]) for page in corpus)
        if max_change < change_threshold:
            break

        page_rank = new_page_rank

    return page_rank

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")

    corpus = crawl(sys.argv[1])
    sample_results = sample_pagerank(corpus, DAMPING, SAMPLES)
    iteration_results = iterate_pagerank(corpus, DAMPING)

    print("PageRank Results from Sampling (n = {})".format(SAMPLES))
    for page, rank in sample_results.items():
        print(f"  {page}: {rank:.4f}")

    print("PageRank Results from Iteration")
    for page, rank in iteration_results.items():
        print(f"  {page}: {rank:.4f")

if __name__ == "__main__":
    import sys
    main()
