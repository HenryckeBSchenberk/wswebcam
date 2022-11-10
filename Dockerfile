FROM python:latest as builder
WORKDIR /app
COPY requirements.txt .

RUN pip install --user --no-warn-script-location -r requirements.txt

FROM python:latest
RUN apt-get update

COPY --from=builder /root/.local /root/.local

WORKDIR /app
COPY . .
ENV PATH=/root/.local:$PATH
ENTRYPOINT ["python", "-m", "src.wswebcam.server"]