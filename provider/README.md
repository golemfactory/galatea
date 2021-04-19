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

### 1. Download models

```bash
$ python download_model.py sentiment-analysis nateraw/bert-base-uncased-emotion ./models/emotion
$ python download_model.py summarization sshleifer/distilbart-cnn-12-6 ./models/summary
```

### 2. Run the classifier

```bash
$ python run_classifier.py sentiment-analysis ./models/emotion/ ./the_queen_sample.txt ./output.txt
$ cat output.txt 
{'sadness': 0.19551274180412292, 'joy': 0.6668532490730286, 'love': 0.061145614832639694, 'anger': 0.051483768969774246, 'fear': 0.02209818735718727, 'surprise': 0.0029064537957310677}
$ python run_classifier.py summarization ./models/summary/ ./the_queen_sample.txt ./output.txt
$ cat output.txt 
The Queen hosted a ceremony in which the Earl Peel stood down as Lord Chamberlain . She accepted her former aide's wand and office insignia at a private event at Windsor Castle . The duke's funeral will take place at Windsor on Saturday . A royal official said members of the family would continue to undertake engagements .
```
