from pathlib import Path
import pandas as pd
import numpy as np
from datasets import load_dataset
from sentence_transformers.losses import CosineSimilarityLoss
from setfit import SetFitModel, SetFitTrainer

INPUT_DIR = Path("input")

if __name__ == "__main__":
    dataset = load_dataset("ethos", "multilabel", trust_remote_code=True)

    features = dataset["train"].column_names
    features.remove("text")

    dataset = dataset.map(
        lambda record: {"labels": [record[feature] for feature in features]},
    )
    train = dataset["train"]

    num_samples = 8
    samples = np.concatenate(
        [np.random.choice(np.where(train[f])[0], num_samples) for f in features]
    )
    train_dataset = train.select(samples)
    print(train_dataset)
    eval_dataset = train.select(np.setdiff1d(np.arange(len(train)), samples))

    model_id = "sentence-transformers/paraphrase-mpnet-base-v2"

    model = SetFitModel.from_pretrained(model_id, multi_target_strategy="one-vs-rest")
    trainer = SetFitTrainer(
        model=model,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        loss_class=CosineSimilarityLoss,
        num_iterations=20,
        column_mapping={"text": "text", "labels": "label"},
    )
    trainer.train()

    trainer.model.save_pretrained("output")
    model = SetFitModel.from_pretrained("output")

    preds = model(
        [
            "Je suis de confession juive",
            "Je n'aime pas que tu me parles mal de la couleur de ma peau",
        ]
    )

    print([[f for f, p in zip(features, pred) if p > 0.5] for pred in preds])


# l = [
#     "temps",
#     "quantité",
#     "autre",
#     "végétarien",
#     "prix",
#     "régimes spéciaux",
#     "qualité",
#     "implication des parents",
#     "remerciements",
#     "variété",
#     "implication des enfants",
#     "encadrement",
#     "lieu",
#     "éducation à l'alimentation",
#     "goût",
#     "bruit",
# ]
