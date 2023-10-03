FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /image_upload_project
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000