FROM vikings/yach:python-baseimage-v1
RUN     mkdir /evaluation
WORKDIR /evaluation
COPY    requirements.txt /evaluation/
RUN     pip3 install -r requirements.txt
COPY    *.py /evaluation/
COPY    models /evaluation/models
CMD ["gunicorn","--reload", "-w", "8", "-b", "0.0.0.0:5000","--timeout","120","--log-level","info", "main:app"]

