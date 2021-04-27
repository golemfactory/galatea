FROM python:3.8-slim

ENV WORK_DIR /work
ENV APP_DIR /classifier
ENV MODELS_DIR $APP_DIR/models
ENV MODELS_JSON $APP_DIR/models.json

# Create volume for input/output files
VOLUME $WORK_DIR

# Install dependencies
WORKDIR $APP_DIR
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Download models
COPY download_models.py .
COPY models.json .
RUN python download_models.py && rm -rf /root/.cache/huggingface

# Set up classifier server
COPY classifier.py .
ENTRYPOINT ["python", "classifier.py", "run"]
