import re


def detect_methods(text):

    methods = []

    method_patterns = {
        "Traditional / Shallow Machine Learning":
            r"\bshallow learning\b|\btraditional machine learning\b",

        "Deep Learning":
            r"\bdeep learning\b",

        "Transfer Learning":
            r"\btransfer learning\b",

        "Convolutional Neural Networks (CNN)":
            r"\bconvolutional neural networks?\b|\bCNNs?\b",

        "Support Vector Machine (SVM)":
            r"\bsupport vector machines?\b|\bSVM\b",

        "K-Nearest Neighbors (KNN)":
            r"\bk-nearest neighbors?\b|\bKNN\b",

        "Random Forest":
            r"\brandom forest\b",

        "K-Means Clustering":
            r"\bk-means clustering\b|\bk-means\b",

        "Gray-Level Co-occurrence Matrix (GLCM)":
            r"\bgray[- ]level co[- ]occurrence matrix\b|\bGLCM\b",

        "Data Augmentation":
            r"\bdata augmentation\b|\baugmentation\b"
    }

    for method, pattern in method_patterns.items():

        if re.search(pattern, text, re.IGNORECASE):

            methods.append(method)

    return methods