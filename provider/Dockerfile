FROM python:3.8-slim

ENV WORK_DIR /work
ENV APP_DIR /classifier
ENV MODELS_DIR $WORK_DIR/models
ENV MODELS_JSON $WORK_DIR/models.json

# Create volume for input/output files
VOLUME $WORK_DIR

# Install dependencies
WORKDIR $APP_DIR
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Set up classifier server
COPY classifier.py .
ENTRYPOINT ["python", "classifier.py", "run"]
