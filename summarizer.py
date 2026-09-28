# summarizer.py - Enhanced Extractive Engine

# Comprehensive stopword list to eliminate noise
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
    "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
    "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
    "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i",
    "if", "in", "into", "is", "it", "its", "itself", "just", "me", "more", "most",
    "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once", "only",
    "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them",
    "themselves", "then", "there", "these", "they", "this", "those", "through", "to",
    "too", "under", "until", "up", "very", "was", "we", "were", "what", "when",
    "where", "which", "while", "who", "whom", "why", "with", "would", "you", "your"
}

def clean_word(word):
    """Strip punctuation and symbols from individual words."""
    return "".join(char for char in word.lower() if char.isalnum())

def get_normalized_frequencies(text):
    """Calculate relative word frequencies (normalized by max frequency)."""
    raw_words = text.split()
    freq = {}
    
    for w in raw_words:
        cleaned = clean_word(w)
        if cleaned and cleaned not in STOPWORDS:
            freq[cleaned] = freq.get(cleaned, 0) + 1
            
    if not freq:
        return {}
        
    # Scale frequencies from 0.0 to 1.0 (Term Frequency Normalization)
    max_freq = max(freq.values())
    for word in freq:
        freq[word] = freq[word] / max_freq
        
    return freq

def summarize_text(paragraph, top_n=2):
    """
    Extracts top_n most important sentences, preserving their original order.
    """
    # Split text into distinct sentences
    raw_sentences = [s.strip() for s in paragraph.replace("\n", " ").split(".") if len(s.strip()) > 5]
    if not raw_sentences:
        return "Text is too short to summarize."
    
    if len(raw_sentences) <= top_n:
        return ". ".join(raw_sentences) + "."

    word_freq = get_normalized_frequencies(paragraph)
    sentence_scores = {}

    for idx, sentence in enumerate(raw_sentences):
        words = sentence.split()
        score = 0
        meaningful_words = 0
        
        for w in words:
            cleaned = clean_word(w)
            if cleaned in word_freq:
                score += word_freq[cleaned]
                meaningful_words += 1
                
        # Length Normalization: Prevents very long sentences from unfairly dominating
        if meaningful_words > 0:
            sentence_scores[idx] = score / (meaningful_words ** 0.8)
        else:
            sentence_scores[idx] = 0

    # Pick the top N highest scoring sentence indices
    best_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]
    
    # Sort them back into chronological order so the summary reads naturally
    best_indices.sort()
    
    summary_sentences = [raw_sentences[i] for i in best_indices]
    return ". ".join(summary_sentences) + "."