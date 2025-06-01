FROM python:3.13.3-slim
RUN groupadd -r db_admin && useradd -r -g db_admin standart

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip

WORKDIR /app/main_service
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
USER standart

ENV PYTHONPATH=/app/main_service
CMD ["python", "-m", "main"]