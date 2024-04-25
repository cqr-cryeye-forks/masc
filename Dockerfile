FROM kalilinux/kali-rolling:latest

ENV PYTHONUNBUFFERED=1

WORKDIR /wd

RUN apt update
RUN apt install -y bash git python3-dev gcc g++ libc-dev ca-certificates \
    libffi-dev libssl-dev clamav curl libmagic-dev pandoc python3-lxml python3-pip

# [dependencies]-[BEGIN]
COPY ./requirements.txt ./requirements.txt

RUN pip install --user --upgrade --no-cache-dir --requirement ./requirements.txt

#RUN pip install python-magic bs4 yara-python watchdog termcolor pypandoc progress pyclamd urllib3==1.24.3 libmagic
#RUN ln -s /usr/local/lib/python3.6/dist-packages/usr/lib/libyara.so /usr/lib/libyara.so
RUN ln -s /usr/local/lib/python3.11/dist-packages/usr/lib/libyara.so /usr/lib/libyara.so
# [dependencies]-[END]

### MITM PROXY ###
RUN git clone --depth 1 https://github.com/cqr-cryeye-org/mitm-cert
RUN python3 -m pip install certifi requests
RUN cert_path=$(python3 -m certifi) && cp mitm-cert/mitmproxy-ca-cert.crt ${cert_path}
RUN sh mitm-cert/change_certificates.sh
RUN printf "yes\n1\n" | dpkg-reconfigure ca-certificates
RUN update-ca-certificates
RUN apt remove git -y
RUN apt-get install proxychains4 -y
### MITM PROXY ###

COPY --chmod=777 entrypoint.sh ./entrypoint.sh

#RUN chmod +x entrypoint.sh

# Can do this, because have dockerignore.
COPY setup.py setup.py
COPY dicts dicts
COPY signatures signatures
COPY masc.conf masc.conf
COPY masc.py masc.py

COPY app app

ENTRYPOINT ["bash", "entrypoint.sh"]
