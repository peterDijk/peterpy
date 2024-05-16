## PeterPy

A project to practice the language, design patterns and best practices

### Prerequisits:

- install poetry

### To run:

`.env`: `localhost` values for the HOST vars
`$ docker compose build`
`$ docker compose up -d`
`$ poetry run peterpy`

### Run with Docker

`.env`: container names (`mysql`, `kafka1`) values for the HOST vars
`$ docker compose build`
`$ docker compose up -d`

To switch between the 2 methods, stop en remove all containers then build again

#### To use auto restarts during development

`$ docker compose watch` keep terminal open
`$ docker compose logs -f` in another terminal

- [x] setup service, health check endpoint
- [x] setup logger using yaml config
- [x] organize routes
- [x] add typing ~~enforcing~~ hinting only in python
- [x] dev tooling, lint formatting etc
- [x] implement Repository Pattern with in memory data
- [x] implement service
- [x] add product to global repository
- [x] add entity encode with to_json method, pass in response
- [x] can't create product same name
- [x] catch not found error, proper response
- [x] setup Postman with automation for list of product creation
- [x] implement Abstract Base Class
- [x] dockerize
- [x] add app restart mechanism on code change (also within docker container)
- [x] add database container to docker setup
- [x] setup Kafka stack, produce message on add product
- [x] connect database
- [x] setup and implement ORM in database-repository
- [x] organize db connection
- [x] setup database-session + commit in aiohttp-middleware (1 commit per request). in middleware try/catch with rollback in catch. app start open connection, app shutdown close connection
- [ ] setup dependency injection in app start so handler doesnt need to setup repo + service every request
- [ ] add test-tooling and unit tests
- [ ] add pagination to /list
- [ ] setup migrations (use Flyway)
- [ ] input validation
- [ ] add custom exceptions
- [ ] Github Actions (linting, testing)
- ...
