# Richie site factory

This repository is a workbench for NAU to develop
themed sites based on [Richie](https://github.com/openfun/richie), the CMS
for Open Education.
This repository is based on France Université Numérique openfun [richie-site-factory](https://github.com/openfun/richie-site-factory) repo.

## Prerequisite

First, make sure you have a recent version of Docker and [Docker
Compose](https://docs.docker.com/compose/install) installed on your laptop:

```
$ docker -v
  Docker version 19.03.10, build 9424aeaee9

$ docker-compose --version
  docker-compose version 1.25.5, build 8a1c60f6
```

## Getting started

First, you need to activate the site on which you want to work. We provide
a script that will list existing sites and let you choose one:

```bash
$ bin/activate
Select an available site to activate:
[1] demo (default)
[2] nau
Your choice: 2

# Check your environment with:
$ make info
RICHIE_SITE: nau
```

Once your environment is set, start the full project by running:

```bash
$ make bootstrap
```

This command builds the containers, starts the services and performs
database migrations. It's a good idea to use this command each time you are
pulling code from the project repository to avoid dependency-related or
migration-related issues.

Once the bootstrap phase is finished, you should be able to view the site at
[localhost:8080](http://localhost:8080)

> If you've just bootstrapped this project, you are probably planning to use AWS
> to store and distribute your media and static files. Luckily for you, we've
> cooked `terraform` scripts and a documentation for you! Read more about it:
> [docs/aws.md](./docs/aws.md)

## Usage

### Managing services

If you need to build or rebuild the containers, use:

```
$ make build
```

> Note that if the services are already running, you will need to stop them
> first and then restart them to fire up your newly built containers.

To start the development stack (_via_ Docker compose), use:

```
$ make run
```

You can inspect logs (in follow mode) with:

```
$ make logs
```

You can stop all services with:

```
$ make stop
```

If you need to stop and remove containers (to drop your database for example),
there is a command for that:

```
$ make down
```

### Housekeeping

Once the CMS is up and running, you can create a superuser account:

```
$ make superuser
```

To perform database migrations, use:

```
$ make migrate
```

You can create a basic demo site by running:

```
$ make demo-site
```

> Note that if you don't create the demo site and start from a blank CMS, you
> will get some errors requesting you to create some required root pages. So it
> is easier as a first approach to test the CMS with the demo site.

### Going further

To see all available commands, run:

```
$ make help
```

## Contributing

This project is intended to be community-driven, so please, do not hesitate to
get in touch if you have any question related to our implementation or design
decisions.

We try to raise our code quality standards and expect contributors to follow the
recommandations from our
[handbook](https://openfun.gitbooks.io/handbook/content).

### Upgrading to a newer richie version

Upgrading one or many projects to a newer version of [richie](https://github.com/openfun/richie)
is automated.

For example, to upgrade a specific site (NAU), test its build after upgrade to 2.9.0 richie version
and commit all changes:

```
bin/upgrade 2.9.0 nau --build --commit
```

To upgrade a list of 3 sites but without testing the build or committing the changes:

```
bin/upgrade 2.9.0 nau othersite2 othersite3
```

To upgrade all the sites handled in the site factory:

```
bin/upgrade 2.9.0 --build --commit
```

### Making a release

Making a release is automated. The choice between a minor or a revision type of release is
determined by the presence of an addition, a change or a removal. A revision release is made
if only fixes are present in the changelog, otherwise a minor release is made.

For example, to release a specific site and commit all changes:

```
bin/release nau --commit
```

If you consider that the changelog contains breaking changes, you can force a major release
by passing the parameter `--major`.


To release a list of 3 sites but without committing the changes:

```
bin/release nau --major
```

To release all the sites handled in the site factory:

```
bin/release --commit
```

After merging release commits to the master branch, you can tag them automatically by running:

```
bin/tag -c
```

## License

This work is released under the GNU Affero General Public License v3.0 (see
[LICENSE](./LICENSE)).
