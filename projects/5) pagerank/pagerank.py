import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])

    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probability = dict()

    for _page in list(corpus):

        if len(corpus[page]) != 0:
            probability[_page] = (1 - damping_factor) / len(corpus)
            if _page in corpus[page]:
                probability[_page] += damping_factor / len(corpus[page])
        else:
            probability[_page] = 1 / len(corpus)

    return probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probability = dict()

    for page in list(corpus):
        probability[page] = 0

    current_page = list(corpus)[random.randint(0, len(corpus) - 1)]
    probability[current_page] += 1

    for i in range(n - 1):
        model = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(model), list(model.values()))[0]
        probability[current_page] += 1

    for page in list(corpus):
        probability[page] /= n

    return probability


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    probability = dict()

    for page in list(corpus):
        probability[page] = 1 / len(corpus)

    converge = 0

    while converge < len(corpus):

        converge = 0
        old_probability = dict(probability)

        for page in list(corpus):
            # old_probability = probability[page]
            summation = 0

            for page_i in list(corpus):
                if len(corpus[page]) != 0:
                    if page in corpus[page_i]:
                        summation += old_probability[page_i] / len(corpus[page_i])
                else:
                    summation += old_probability[page_i] / (len(corpus[page_i]) + 1)

            probability[page] = (1 - damping_factor) / len(corpus) + damping_factor * summation

            if -0.001 <= old_probability[page] - probability[page] <= 0.001:
                converge += 1

    return probability


if __name__ == "__main__":
    main()
