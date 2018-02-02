# Shop

## Running using Docker image

```bash
docker run -p 9000:9000 pygo/shop
```

It will by accessible here [127.0.0.1:9000](http://127.0.0.1:9000)

To run tests using docker:

```bash
docker run pygo/shop test
```

## Running manually

#### Requirements:

* Python 3.6.x
* NodeJS 9.x
* Yarn

#### Clonning repository:

```bash
git clone https://github.com/dmrz/shop.git
```

#### Building and running:

```bash
cd shop
make
```

Once it's done, you can run it with the following command:

```bash
make run
```

To run tests:

```bash
make test
```
