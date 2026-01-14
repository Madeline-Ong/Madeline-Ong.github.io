FROM python:3.11.11-bullseye

RUN apt-get update && apt-get install -y iputils-ping && apt-get clean

ARG PROJECT_PATH=/app
ENV TZ="Asia/Singapore"

RUN set -eux; \
    # Creating the path 
    mkdir -p $PROJECT_PATH; \
    SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history"; \
    mkdir /commandhistory; \
    touch /commandhistory/.bash_history; \
    # chown -R $USERNAME:$USERNAME /commandhistory; \
    echo "$SNIPPET" >> "/root/.bashrc"; \
# Install git inside vm
    apt update; \
    apt install git -y;
 
COPY requirements.txt $PROJECT_PATH

COPY test_192.json /test_192.json

RUN set -eux; \
    pip3 install \
    -r $PROJECT_PATH/requirements.txt