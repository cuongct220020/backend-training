FROM python:3.9

WORKDIR /api

# Copy and install stable (base) requirements
COPY requirements/base-requirements.txt base-requirements.txt
RUN pip install --no-cache-dir -r base-requirements.txt

# Copy and install development
COPY requirements/dev-requirements.txt dev-requirements.txt
RUN pip install --no-cache-dir -r dev-requirements.txt

COPY . .

CMD ["python3", "main.py"]
