<a name="unreleased"></a>

## [Unreleased]

<a name="v0.5.2"></a>

## v0.5.2 - 2022-02-03

### :bug: Bug Fixes

- remove extension from archive segment filename
- always flush event queue on stop ([#24](https://github.com/jooola/earhorn/issues/24))
- linting
- don't use stderr.readline
- log formatting
- update apt packages list in ci
- no tests yet
- tests module not yet created

### :gear: CI/CD

- docker-publish does not need publish job

### :rocket: Features

- use event handler and checks during startup
- add stream url precheck ([#20](https://github.com/jooola/earhorn/issues/20))
- more logging for silence listener
- more logging for archiver
- create docker image and publish it ([#19](https://github.com/jooola/earhorn/issues/19))
- use realtime input ([#10](https://github.com/jooola/earhorn/issues/10))
- silence detect ([#9](https://github.com/jooola/earhorn/issues/9))
- warn when no action will be taken
- allow url to be specified using env var
- initial work

[unreleased]: https://github.com/jooola/earhorn/compare/v0.5.2...HEAD