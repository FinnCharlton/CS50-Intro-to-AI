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
    print(people)

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
    # print(probabilities)

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
                # print(f"Calculating JP: 1G= {one_gene}, 2G= {two_genes} T= {have_trait}")
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)
                # print(f"New Probs = {probabilities}")
    print(probabilities)

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

# people = {
#   'Harry': {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None},
#   'James': {'name': 'James', 'mother': None, 'father': None, 'trait': True},
#   'Lily': {'name': 'Lily', 'mother': None, 'father': None, 'trait': False}
# }

# one_gene = {'Harry'}
# two_genes = {'James'}
# has_trait = {'James'}

def find_gene_number(person, one_gene, two_genes):
    """
    Custom function.
    
    Takes a person's name and returns the amount of genes they have based on given sets
    """
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0
    

def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #Create dictionaries of inheritence probabilities
    inheritenceProbs = {
        0 : 0 + PROBS['mutation'],
        1 : 0.5, #Plus and minus mutation
        2: 1 - PROBS['mutation']
    }

    #Initialise output dictionary
    jointProbs = dict()

    #Loop through people
    for person in people:

        #If the person is parentless, we can fetch unconditional probabilities
        if people[person]['mother'] == None:
            
            #If person in one_gene, fetch probability of one gene * trait status
            if person in one_gene:
                jointProbs[person] = PROBS['gene'][1]*PROBS['trait'][1][person in have_trait]

            #If person in one_gene, fetch probability of one gene * trait status
            elif person in two_genes:
                jointProbs[person] = PROBS['gene'][2]*PROBS['trait'][2][person in have_trait]

            #If person in neither, fetch probability of no genes * trait status
            else:
                jointProbs[person] = PROBS['gene'][0]*PROBS['trait'][0][person in have_trait]

        #If the person has parents, we use probabilities of inheritence.
        else:

            #Find probabilities that mother and father pass on gene
            motherPass = inheritenceProbs[find_gene_number(people[person]['mother'],one_gene,two_genes)]
            fatherPass = inheritenceProbs[find_gene_number(people[person]['father'],one_gene,two_genes)]

            #If person in one_gene, calculate XOR percentage
            if person in one_gene:
                jointProbs[person] = ((motherPass*(1-fatherPass))+(fatherPass*(1-motherPass)))*PROBS['trait'][1][person in have_trait]

            #If person in two_gene, calculate AND percentage
            elif person in two_genes:
                jointProbs[person] = (motherPass*fatherPass)*PROBS['trait'][2][person in have_trait]

            #If person in neither, calculate AND percentage for not passing
            else:
                jointProbs[person] = ((1-motherPass)*(1-fatherPass))*PROBS['trait'][2][person in have_trait]

    #Sum probabilities
    product = 1
    for value in jointProbs.values():
        product *= value

    return product

# print(joint_probability(people,one_gene,two_genes,has_trait))


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    #Loop over one_gene, updating probabilities
    for person in probabilities.keys():
        # print(f"Updating Probabilities: {person}")
        # print(f"Updating gene {find_gene_number(person,one_gene,two_genes)}")
        probabilities[person]['gene'][find_gene_number(person,one_gene,two_genes)] += p
        # print(f"Updating trait {person in have_trait}")
        probabilities[person]['trait'][person in have_trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    #Loop through probability distributions
    for person, dists in probabilities.items():
        for type, dist2 in dists.items():

            #Find sum of probabilities
            sum = 0
            for val in dist2.values():
                sum += val

            #Multiply each by 1/sum to normalise them
            coefficient = 1/sum
            for key in dist2.keys():
                probabilities[person][type][key] *= coefficient

        #Find sum of probabilities


if __name__ == "__main__":
    main()
