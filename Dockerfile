FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 0

RUN curl -sL https://deb.nodesource.com/setup_9.x | bash -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN apt-get update && apt-get install -y --force-yes yarn nodejs

RUN mkdir /code
COPY . /code/shop
WORKDIR /code/shop

# Cleanup
RUN rm -f db.sqlite3
RUN find . -name "__pycache__" -exec rm -rf {} 2> /dev/null \; 2> /dev/null || true
RUN find . -name ".cache" -exec rm -rf {} 2> /dev/null \; 2> /dev/null || true
RUN rm -rf .git
RUN rm -rf .mypy_cache
RUN rm -rf .ropeproject

RUN pip install -r requirements/local.txt
RUN python shop/manage.py migrate -v 0 --noinput
RUN python shop/manage.py loaddata -v0 fixtures/initial_users.json
RUN python shop/manage.py loaddata -v0 fixtures/initial_products.json

WORKDIR /code/shop/frontend
# Cleanup
RUN rm -rf dist
RUN rm -rf node_modules
RUN rm -f webpack-stats.json

RUN yarn --emoji false
RUN yarn build

WORKDIR /code/shop
EXPOSE 9000
ENTRYPOINT [ "sh", "entry_point.sh" ]
