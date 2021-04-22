"""
We'll add something interesting a bit later now let's mock the response
"""

from typing import Dict


def classify_text(text: str) -> Dict:
    return {
        "results": [
            {
                "classifier_id": "distilbart-cnn-12-6",
                "summary_text": " ".join(text.lower().split()[:10])
            },
            {
                "classifier_id": "bert-base-uncased-emotion",
                "summary_list": [
                    { "label": "love", "score": 0.005923508666455746, },
                    { "label": "joy", "score": 0.38369229435920715, },
                    { "label": "surprise", "score": 0.6015767455101013, },
                ]
            },
        ],
    }
