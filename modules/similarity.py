import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource
def load_model():

    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    return model


def create_embedding(text):

    model = load_model()

    embedding = model.encode(
        text,
        convert_to_numpy=True
    )

    return embedding


def calculate_similarity(text1, text2):

    embedding1 = create_embedding(text1)

    embedding2 = create_embedding(text2)

    similarity = cosine_similarity(
        [embedding1],
        [embedding2]
    )[0][0]

    return round(
        float(similarity * 100),
        2
    )


def compare_papers(papers):

    results = []

    for i in range(len(papers)):

        for j in range(i + 1, len(papers)):

            score = calculate_similarity(
                papers[i]["text"],
                papers[j]["text"]
            )

            results.append(
                {
                    "paper_1": papers[i]["title"],
                    "paper_2": papers[j]["title"],
                    "similarity": score
                }
            )

    return results