print("🔥 NEW GAP DETECTOR LOADED")
import re


def clean_sentence(sentence):
    return " ".join(sentence.split()).strip()


def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [
        clean_sentence(sentence)
        for sentence in sentences
        if len(sentence.strip()) > 50
    ]


def detect_gap_signals(papers):

    gap_signals = []

    # Strong research-gap indicators
    patterns = {
        "Research Gap": [
            "lack of",
            "lack of research",
            "lack of comprehensive",
            "little research",
            "few studies",
            "few researchers",
            "underexplored",
            "under-explored",
            "not yet",
            "remains unclear",
            "remains unknown"
        ],

        "Limitation": [
            "limitation",
            "limitations",
            "limitation of",
            "limited by",
            "limited to",
            "challenge",
            "challenges"
        ],

        "Future Research": [
            "future work",
            "future research",
            "future studies",
            "in the future",
            "further research",
            "further studies",
            "future direction",
            "future directions"
        ]
    }

    # Avoid very generic or weak sentences
    ignored_phrases = [
        "improve the quality",
        "improve the effectiveness",
        "improve the performance",
        "additional information",
        "additional features",
        "limited number of",
        "limited resources"
    ]

    for paper in papers:

        sentences = split_sentences(paper["text"])

        for sentence in sentences:

            sentence_lower = sentence.lower()

            # Skip weak/generic matches
            if any(
                phrase in sentence_lower
                for phrase in ignored_phrases
            ):
                continue

            matched_keyword = None
            matched_type = None

            # Search strongest patterns first
            for gap_type, keywords in patterns.items():

                for keyword in keywords:

                    if keyword in sentence_lower:
                        matched_keyword = keyword
                        matched_type = gap_type
                        break

                if matched_keyword:
                    break

            if matched_keyword:

                # Assign strength
                if matched_type == "Research Gap":
                    strength = "High"

                elif matched_type == "Future Research":
                    strength = "High"

                else:
                    strength = "Medium"

                signal = {
                    "paper": paper["title"],
                    "type": matched_type,
                    "strength": strength,
                    "evidence": sentence,
                    "keyword": matched_keyword
                }

                # Avoid duplicate evidence
                duplicate = any(
                    existing["evidence"] == sentence
                    for existing in gap_signals
                )

                if not duplicate:
                    gap_signals.append(signal)

    # Strong signals first
    strength_order = {
        "High": 0,
        "Medium": 1
    }

    gap_signals.sort(
        key=lambda x: strength_order.get(
            x["strength"],
            2
        )
    )

    return gap_signals


def compare_gap_signals(gap_signals):

    opportunities = []

    for signal in gap_signals:

        evidence = signal["evidence"]
        evidence_lower = evidence.lower()

        if (
            "new disease classes" in evidence_lower
            or "new images" in evidence_lower
            or "new dataset" in evidence_lower
            or "new datasets" in evidence_lower
        ):

            opportunities.append({
                "title": "Expand Plant Disease Datasets",
                "description":
                    "Develop larger and more diverse datasets "
                    "containing additional plant diseases, "
                    "images and environmental conditions.",
                "gap_type": "Dataset"
            })

        elif (
            "severity" in evidence_lower
            or "possibility" in evidence_lower
        ):

            opportunities.append({
                "title": "Disease Severity Estimation",
                "description":
                    "Extend disease detection from simple "
                    "classification toward estimating disease severity.",
                "gap_type": "Application"
            })

        elif (
            "flowers" in evidence_lower
            or "fruits" in evidence_lower
            or "stems" in evidence_lower
        ):

            opportunities.append({
                "title": "Beyond Leaf-Based Detection",
                "description":
                    "Extend plant disease analysis from leaf images "
                    "to flowers, fruits and stems.",
                "gap_type": "Scope"
            })

        elif (
            "architecture" in evidence_lower
            or "model" in evidence_lower
            or "deep learning" in evidence_lower
        ):

            opportunities.append({
                "title": "Explore Improved Model Architectures",
                "description":
                    "Investigate alternative deep learning architectures "
                    "and modeling approaches for plant disease detection.",
                "gap_type": "Methodology"
            })

    # Remove duplicate opportunities
    unique = []

    for opportunity in opportunities:

        if not any(
            existing["title"] == opportunity["title"]
            for existing in unique
        ):
            unique.append(opportunity)

    return unique