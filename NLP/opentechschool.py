# Create an empty dictionary for associating radish names
# with vote counts
counts = {}

for line in open("radishsurvey.txt"):
    line = line.strip()
    name, vote = line.split(" - ")
    if vote not in counts:
        # First vote for this variety
        counts[vote] = 1
    else:
        # Increment the vote count
        counts[vote] = counts[vote] + 1
print(counts)