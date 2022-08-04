FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./deployment_scripts /deployment_scripts

WORKDIR /goallens

COPY Pipfile Pipfile.lock /goallens/
RUN pip install pipenv && pipenv install --system && \
    adduser --disabled-password --no-create-home goallens && \
    chmod -R +x /deployment_scripts && \
    mkdir -p /vol/web/static_prod
    # chown -R goallens:goallens /vol && \
    # chmod -R 755 /vol

COPY . /goallens/
EXPOSE 8000

ENV PATH="/deployment_scripts:$PATH"

# USER goallens

CMD ["run.sh"]