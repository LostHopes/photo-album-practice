FROM python:latest

WORKDIR /app
SHELL [ "/bin/bash", "-c" ]

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY pyproject.toml uv.lock /app/

RUN python -m venv $VIRTUAL_ENV\
    && source $VIRTUAL_ENV/bin/activate\
    && pip install uv\
    && uv sync
    
COPY . /app/
EXPOSE 5000
CMD [ "python", "src/wsgi.py" ]



