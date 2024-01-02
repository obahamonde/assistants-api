FROM node:16.11.1-alpine3.14

WORKDIR /app


COPY app/package.json .
RUN npm install

COPY app/ ./

RUN npm run build && npm prune --production 

FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
