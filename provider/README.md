# Provider

---

## Run classifier locally

### 0. Prepare environment

```bash
$ cd provider
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
```

### 1. Download model

```bash
$ python download_model.py nateraw/bert-base-uncased-emotion ./models/emotion
```

### 2. Run the classifier

```bash
$ python run_classifier.py ./models/emotion/ ./the_queen_sample.txt ./output.txt
$ cat output.txt 
{'sadness': 0.19551274180412292, 'joy': 0.6668532490730286, 'love': 0.061145614832639694, 'anger': 0.051483768969774246, 'fear': 0.02209818735718727, 'surprise': 0.0029064537957310677}
```
