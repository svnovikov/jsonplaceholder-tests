FROM python:3

ENV TESTMOUNTDIR ${TESTMOUNTDIR:-/usr/src/app}
WORKDIR /usr/src/app

COPY requirements.txt ./
COPY test-requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r test-requirements.txt

COPY ./src ./src
RUN pycodestyle ./src

ENTRYPOINT ["pytest", "--junit-xml", "$TESTMOUNTDIR/test_result.xml"]
