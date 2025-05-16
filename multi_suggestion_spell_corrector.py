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

def process_search_with_ngrams(searchTerm, database, n=2, threshold_min=4, max_suggestions=1):
    searchTerm = preprocess_word(searchTerm)
    search_ngrams = generate_ngrams(searchTerm, n)
    processed_database = [preprocess_word(word) for word in database]
    candidates = []

    for word in processed_database:
        word_ngrams = generate_ngrams(word, n)
        common_ngrams = set(search_ngrams) & set(word_ngrams)
        if len(common_ngrams) > 0:
            candidates.append(word)

    distances = [(word, levenshtein_distance(word, searchTerm)) for word in candidates]
    distances.sort(key=lambda x: x[1])
    suggestions = [word for word, dist in distances[:max_suggestions]]

    if len(suggestions) < max_suggestions:
        for word in processed_database:
            if word not in suggestions:
                if abs(len(word) - len(searchTerm)) <= 2 or len(set(word) & set(searchTerm)) > 0:
                    suggestions.append(word)
                    if len(suggestions) == max_suggestions:
                        break

    return suggestions

# Example usage
database = ["hello", "world", "whatsapp", "feature", "suggestion", "test", "typing",
            "application", "weather", "system", "functionality", "development", "python",
            "programming", "code", "example", "sample", "reference", "suggestions"]

input_words = [("helllo", 1), ("examle", 2), ("functonality", 3), ("developmnt", 4)]

for word, num_suggestions in input_words:
    suggestions = process_search_with_ngrams(word, database, max_suggestions=num_suggestions)
    print(f'Suggestions for "{word}": {", ".join(suggestions)}')
