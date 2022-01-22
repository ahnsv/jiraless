FROM python:3.8-slim-buster
WORKDIR /usr/app
COPY . /usr/app/github_svc/
ADD ./__init__.py /usr/app/github_svc/__init__.py
WORKDIR /usr/app/github_svc
RUN pip install --upgrade pip && \
    pip install pytest pytest-dotenv && \
    pip install -r requirements.txt
WORKDIR /usr/app
CMD python3 -m github_svc.src.entrypoints.redis