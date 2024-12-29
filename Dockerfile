FROM python:3.11-slim

WORKDIR /usr/app/src

ARG LANG='en_US.UTF-8'

# Download and Install Dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        # build-essentials \
        locales \
        python3-pip \
        python3-yaml \
        rsyslog systemd systemd-cron sudo \
    && apt-get clean

RUN pip3 install --upgrade pip
RUN pip3 install streamlit
RUN pip install langchain
RUN pip3 install streamlit streamlit-js-eval
RUN pip install python-dotenv
RUN pip install langchain-groq
RUN pip install PyPDF2

#RUN pip install --no-cache-dir -r requirements.txt

COPY ./ .

EXPOSE 8501

# Tell the image what to do when it starts as a container
CMD ["streamlit", "run", "main.py"]
