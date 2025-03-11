FROM python:latest

WORKDIR /app
SHELL [ "/bin/bash", "-c" ]

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app/src

COPY pyproject.toml uv.lock /app/

RUN python -m venv $VIRTUAL_ENV\
    && source $VIRTUAL_ENV/bin/activate\
    && pip install uv\
    && uv sync --group prod
    
COPY . /app/
EXPOSE 5000
CMD [ "gunicorn", "--workers 2", "wsgi:app", "--bind", "0.0.0.0:5000", "--chdir", "src"]