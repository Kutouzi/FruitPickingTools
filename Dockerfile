FROM python:3

WORKDIR /usr/src/fruit

COPY requirements.txt ./
RUN ["pip","install","--no-cache-dir","-r","./requirements.txt"]

COPY . .

VOLUME ["/usr/src/fruit/output/"]
VOLUME ["/usr/src/fruit/logs/"]
VOLUME ["/usr/src/fruit/charaMap/"]
VOLUME ["/usr/src/fruit/var/"]

EXPOSE 80/tcp

CMD ["python","./FruitPickingTools.py"]