import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_genes` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.

    Args:
        people (dict): A dictionary containing information about each person. The keys are names of people, and the values are dictionaries containing 'name', 'mother', 'father', and 'trait' keys.
        one_gene (set): A set of people for whom to compute the probability that they have one copy of the gene.
        two_genes (set): A set of people for whom to compute the probability that they have two copies of the gene.
        have_trait (set): A set of people for whom to compute the probability that they have the trait.

    Returns:
        float: The joint probability of the specified events taking place.
    """
    # Initialize joint probability
    joint_prob = 1
    
    # Iterate over all the people given
    for person in people:
        gene_prob = 1
        # Store the amount of genes of that particular person
        # if is not in the one_genes and not in the two_genes -> it means it has no genes
        genes = 2 if person in two_genes else 1 if person in one_gene else 0
        # if people is in trait it shows the trait if not it has no trait
        trait = person in have_trait
        # Store infomation regarding its parents
        mother = people[person]['mother']
        father = people[person]['father']
        # If person has no parental information its probability is only based on the amount
        # of genes that he has
        if mother is None and father is None:
            gene_prob *= PROBS["gene"][genes]

        # If person has parental information the probality change according to the parents
        else:
            # We store the probability of each parent passing the gene to the son
            mother_probability = parent_probability(mother, one_gene, two_genes)
            father_probability = parent_probability(father, one_gene, two_genes)

            # if the son has two genes this means that he has received one from each parent
            # either directly or by a mutation thats why we multiply both chances
            if genes == 2:
                gene_prob *= mother_probability * father_probability
            # if the son has one gene it means that it received it from one of its parents but not both
            # here we have the probability of receiving it from the father and not the mother and the other way around
            elif genes == 1:
                gene_prob *= (1 - mother_probability) * father_probability + (1 - father_probability) * mother_probability
            # if the son has no gene it means that he has not  recieved any gene from his parents
            # so here we represent the possibily of not receiving it from each parent
            else:
                gene_prob *= (1 - mother_probability) * (1 - father_probability)
        # Here we add the probabilties  of having the trait.
        gene_prob *= PROBS["trait"][genes][trait]
        # Update joint probability
        joint_prob *= gene_prob
        
    return joint_prob


def parent_probability(parent, one_gene, two_genes):
    """
    Returns the probability of a parent giving a copy of the mutated gene to their child.

    Takes:
    - parent_name - the name of the parent
    - one_gene - set of people having 1 copy of the gene
    - two_genes - set of people having two copies of the gene.
    """

    # Here we check the probability of the parents having the genes
    # if the parent is in the one_gene list is has 50% probability of passing it
    if parent in one_gene:
        return 0.5
    # if the parent has two genes they will pass one, with exception of a mutation
    # so the chances are 1 - the probability of the gene mutating
    elif parent in two_genes:
        return 1 - PROBS['mutation']
    # if the parents have no genes it is only the chance of a mutation occuring
    else:
        return PROBS['mutation']
    
def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        # Update gene distribution
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        
        # Update trait distribution
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        # Normalize gene distribution
        total_gene_prob = sum(probabilities[person]["gene"].values())
        for gene_count in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene_count] /= total_gene_prob
        
        # Normalize trait distribution
        total_trait_prob = sum(probabilities[person]["trait"].values())
        for trait_value in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait_value] /= total_trait_prob


if __name__ == "__main__":
    main()
