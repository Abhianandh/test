import csv
import itertools

#Define the probability distribution constants
PROBS = {
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },
    "trait": {
        2: {True: 0.65, False: 0.35},
        1: {True: 0.56, False: 0.44},
        0: {True: 0.01, False: 0.99}
    },
    "mutation": 0.01
}

def load_data(filename):
    #Load data from a CSV file and return it as a dictionary
    data = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            mother = row["mother"]
            father = row["father"]
            trait = True if row["trait"] == "1" else False
            data[name] = {"mother": mother, "father": father, "trait": trait}
    return data

def calc_gene_probability(num_genes, has_trait):
    #Calculate the probability of having 'num_genes' and 'has_trait' based on PROBS
    prob_gene = PROBS["gene"][num_genes]
    prob_trait = PROBS["trait"][num_genes][has_trait]
    return prob_gene * prob_trait

def joint_probability(people, one_gene, two_genes, have_trait):
    #Calculate the joint probability of gene and trait combinations for all people
    probability = 1.0

    for person in people:
        num_genes = 0
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2
        
        prob = 1.0
        mother = people[person]["mother"]
        father = people[person]["father"]
        
        if mother is None and father is None:
            prob = PROBS["gene"][num_genes]
        else:
            passing = [0, 0]
            
            for i, parents in enumerate([(mother, father), (father, mother)]):
                for parent in parents:
                    if num_genes == 0:
                        passing[i] += 1 - PROBS["mutation"]
                    elif num_genes == 1:
                        passing[i] += 0.5
                    else:
                        passing[i] += PROBS["mutation"]
            
            prob = passing[0] * passing[1]
        
        probability *= prob * calc_gene_probability(num_genes, people[person]["trait"])
    
    return probability

def update(probabilities, one_gene, two_genes, have_trait):
    #Update the probabilities dictionary based on the joint probability
    joint_prob = joint_probability(probabilities, one_gene, two_genes, have_trait)

    for person in probabilities:
        num_genes = 0
        if person in one_gene:
            num_genes = 1
        elif person in two_genes:
            num_genes = 2
        
        prob = calc_gene_probability(num_genes, person in have_trait)
        
        probabilities[person]["gene"][num_genes] += joint_prob
        probabilities[person]["trait"][person in have_trait] += joint_prob

def normalize(probabilities):
    #Normalize the probability distributions for all people
    for person in probabilities:
        gene_distribution = probabilities[person]["gene"]
        trait_distribution = probabilities[person]["trait"]
        
        gene_sum = sum(gene_distribution.values())
        trait_sum = sum(trait_distribution.values())

        for num_genes in gene_distribution:
            gene_distribution[num_genes] /= gene_sum

        for has_trait in trait_distribution:
            trait_distribution[has_trait] /= trait_sum

def main():
    data = load_data("data/family0.csv")
    
    people = {}
    for name in data:
        people[name] = {"gene": {0: 0, 1: 0, 2: 0}, "trait": {True: 0, False: 0}}
    
    one_gene = set()
    two_genes = set()
    have_trait = set()
    
    one_gene.update(["Harry"])
    two_genes.update(["James"])
    have_trait.update(["Harry", "James"])
    
    update(people, one_gene, two_genes, have_trait)
    normalize(people)
    
    for person in people:
        print(f"{person}:")
        for field in people[person]:
            print(f"  {field}:")
            for key, value in people[person][field].items():
                print(f"    {key}: {value:.4f}")

if __name__ == "__main":
    main()
