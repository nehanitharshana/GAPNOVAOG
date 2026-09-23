import re


def detect_topics(text, keywords=None):

    topics = []

    # Use extracted keywords first
    if keywords:
        topics.extend(keywords)

    # Additional topic patterns
    topic_patterns = {
        "Plant Pathology": r"\bplant pathology\b",
        "Leaf Disease Classification": r"\bleaf disease classification\b",
        "Machine Learning": r"\bmachine learning\b",
        "Deep Learning": r"\bdeep learning\b",
        "Augmented Learning": r"\baugmented learning\b",
        "Smart Agriculture": r"\bsmart agriculture\b",
        "Computer Vision": r"\bcomputer vision\b",
        "Transfer Learning": r"\btransfer learning\b",
        "Convolutional Neural Networks": r"\bconvolutional neural networks?\b|\bCNNs?\b"
    }

    for topic, pattern in topic_patterns.items():

        if re.search(pattern, text, re.IGNORECASE):
            if topic not in topics:
                topics.append(topic)

    return topics