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
$ python download_models.py ./models.json ./models
Downloading model 'nateraw/bert-base-uncased-emotion' into 'models/emotion'... Done.
Downloading model 'sshleifer/distilbart-cnn-12-6' into 'models/summary'... Done.
All models downloaded.
```

### 2. Start the classifier (server)

```bash
$ python classifier.py run ./models.json ./models
Loading models... Done.
Server listening on socket ipc:///tmp/classifier.sock...

```

### 3. Classify text

```bash
$ python classifier.py submit ./the_queen_sample.txt ./output.txt
$ cat output.txt 
{"emotion": [{"label": "sadness", "score": 0.19551274180412292}, {"label": "joy", "score": 0.6668532490730286}, {"label": "love", "score": 0.061145614832639694}, {"label": "anger", "score": 0.051483768969774246}, {"label": "fear", "score": 0.02209818735718727}, {"label": "surprise", "score": 0.0029064537957310677}], "summary": {"summary_text": " The Queen hosted a ceremony in which the Earl Peel stood down as Lord Chamberlain . She accepted her former aide's wand and office insignia at a private event at Windsor Castle . The duke's funeral will take place at Windsor on Saturday . A royal official said members of the family would continue to undertake engagements ."}}
```
