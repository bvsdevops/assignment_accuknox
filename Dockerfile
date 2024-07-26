FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    fortune-mod \
    cowsay

RUN git clone https://github.com/nyrahul/wisecow.git .

RUN chmod +x /app/wisecow.sh

EXPOSE 4499

CMD ["./wisecow.sh"]