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
    Return a probability distribution over which page a random surfer
    would visit next, given a corpus of pages, a current page, and
    a damping factor.

    Args:
        corpus (dict): A dictionary mapping a page name to a set of
            all pages linked to by that page.
        page (str): The current page.
        damping_factor (float): The damping factor to be used when
            generating the probabilities.

    Returns:
        dict: A dictionary representing the probability distribution
            over which page a random surfer would visit next.
    """
    # Initialize the probability distribution
    probability_distribution = {}
    # If the page has outgoing links
    if page in corpus and corpus[page]:
        # Calculate the probability for each linked page
        # Here we calculate the probability of randomly arriving to the page
        for linked_page in corpus:
            probability_distribution[linked_page] = (1 - damping_factor) / len(corpus)

        # Add the probability for choosing one of the linked pages
        # Here we calculate the probability of arriving to the page through a link of the ACTUAL page
        # So depending on the amount of links leading to the page the probability may vary
        for linked_page in corpus[page]:
            probability_distribution[linked_page] += damping_factor / len(corpus[page])

    # If the page has no outgoing links
    else:
        # Calculate the probability for each page in the corpus
        # We give all the pages the same probability so the "surfer" could move to any other page
        num_pages = len(corpus)
        for page_name in corpus:
            probability_distribution[page_name] = 1 / num_pages

    # We return a dictionary with the name of the page and its probability of being chosen
    return probability_distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize a dictionary to keep track of PageRank values for each page
    pageranks = {page: 0 for page in corpus}
    
    # Choose a page at random to start the sampling process
    current_page = random.choice(list(corpus.keys()))

    # Generate samples
    for _ in range(n):
        # Increment the PageRank value for the current page
        pageranks[current_page] += 1
        
        # Update the transition model based on the current page
        probabilities = transition_model(corpus, current_page, damping_factor)
        
        # Choose the next page based on the transition model probabilities
        current_page = random.choices(list(probabilities.keys()), weights=list(probabilities.values()))[0]

    # Normalize the PageRank values to sum to 1
    total_samples = sum(pageranks.values())
    pageranks = {page: rank / total_samples for page, rank in pageranks.items()}
    
    return pageranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize PageRank values for each page
    # Each page will have an initial value of 1/ Number of pages
    num_pages = len(corpus)
    pageranks = {page: 1 / num_pages for page in corpus}
    
    # Iterate until convergence
    while True:
        new_pageranks = {}
        max_change = 0
        
        # Calculate new PageRank values for each page in the corpus
        for page in corpus:
            # Add the probability fo arriving from anywhere
            new_pagerank = (1 - damping_factor) / len(corpus)
            for linking_page, links in corpus.items():
                # If this page has links leading to it, we add more probabilities to arriving to it
                if page in links:
                    # We get the total of links
                    num_links = len(links)
                    new_pagerank += damping_factor * pageranks[linking_page] / num_links
            new_pageranks[page] = new_pagerank
            
            # Track the maximum change in PageRank value
            # To later check if the changes suffer are enough to continue iterating
            max_change = max(max_change, abs(new_pagerank - pageranks[page]))
        
        # Update PageRank values
        pageranks = new_pageranks
        
        # Check for convergence
        # If we do not have sufficient changes we can stop the iteration
        if max_change < 0.001:
            break
    
    return pageranks


if __name__ == "__main__":
    main()
