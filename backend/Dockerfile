FROM python:latest
WORKDIR /backend
COPY . .
RUN pip install -r requirements.txt
RUN python -m prisma generate
RUN prisma db push
RUN python -m Utils.AddNewStatement
EXPOSE 8000
CMD ["python", "main.py"]