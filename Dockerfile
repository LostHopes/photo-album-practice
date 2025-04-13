FROM python:3.13-slim AS install

WORKDIR /app
SHELL [ "/bin/bash", "-c" ]

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app/src

COPY pyproject.toml uv.lock /app/

RUN python -m venv $VIRTUAL_ENV \
   && source $VIRTUAL_ENV/bin/activate \
   && pip install uv \
   && uv sync --group prod \
   && pip install gunicorn

FROM python:3.13-slim

WORKDIR /app

COPY src/ /app/src/

COPY --from=install /app/.venv /app/.venv

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV PYTHONPATH=/app/src

EXPOSE 5000

CMD ["gunicorn", "--workers=2", "wsgi:app", "--bind", "0.0.0.0:5000", "--chdir", "src"]