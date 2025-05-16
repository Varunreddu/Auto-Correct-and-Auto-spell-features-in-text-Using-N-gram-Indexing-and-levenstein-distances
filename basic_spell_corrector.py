import re

def preprocess_word(word):
    word = word.lower()
    word = re.sub(r'\W+', '', word)
    return word

def generate_ngrams(word, n):
    return [word[i:i+n] for i in range(len(word)-n+1)]

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def process_search_with_ngrams(searchTerm, database, n=2, threshold_min=4):
    searchTerm = preprocess_word(searchTerm)
    search_ngrams = generate_ngrams(searchTerm, n)

    processed_database = [preprocess_word(word) for word in database]
    stringToPass = []

    for i, word in enumerate(processed_database):
        word_ngrams = generate_ngrams(word, n)
        common_ngrams = set(search_ngrams) & set(word_ngrams)
        if len(common_ngrams) > 0:
            if abs(len(word) - len(searchTerm)) < threshold_min:
                stringToPass.append(word)

    min_distance = float('inf')
    best_match = None

    for word in stringToPass:
        cost = levenshtein_distance(word, searchTerm)
        if cost < min_distance:
            min_distance = cost
            best_match = word

    return best_match, min_distance

# Example usage
database = ["hello", "world", "whatsapp", "feature", "suggestion", "test", "typing"]
searchTerm = "whatsap"
best_match, distance = process_search_with_ngrams(searchTerm, database)
print(f'Best match for "{searchTerm}" is "{best_match}" with a Levenshtein distance of {distance}')
