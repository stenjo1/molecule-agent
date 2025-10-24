FROM continuumio/miniconda3

WORKDIR /app

COPY environment.yml .
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "vs-agent", "/bin/bash", "-c"]

COPY . .

RUN mkdir -p /app/data

VOLUME ["/app/data"]

CMD ["conda", "run", "-n", "vs-agent", "python", "demo.py"]