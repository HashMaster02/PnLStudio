FROM python:3.11.14-slim-trixie
WORKDIR /backend
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y libatomic1 && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -r requirements.txt
RUN python -m prisma generate
RUN prisma db push
RUN python -m Utils.AddNewStatement trades/synthetic
EXPOSE 8000
CMD ["python", "main.py"]