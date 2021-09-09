# Changelog
It`s a test program. So changelog is a big mess.

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]
 
## [0.1.4] - 2021-08-30
### Added
 - Add possibility for user to export reminders into csv file 
 
### Fixed
- change some tests
- piplock
- conflicts

## [0.1.3] - 2021-08-29
### Added
 - Implement possibility for user to add many different emails 
 
### Fixed
- change pipfile, piplock, change email test

## [0.1.2] - 2021-08-29
### Added
 - Create tests for user categories
 
### Fixed
- change pipfile

## [0.1.1] - 2021-08-28
### Added
 - Create email notifications for user reminders
 
### Fixed
- celery doesnt work with redis, need to change broke from redis to rabbitMQ

## [0.1.0] - 2021-08-27

### Added
- Create CRUD for user reminders and category
- Create test for user reminders
### Fixed
- conflicts with branch dev
## [0.0.9] - 2021-08-26

### Added
- User can create his own reminders


## [0.0.8] - 2021-08-25

### Added
- Add email confirmation for user email

### Fixed

- add DS_Store to .gitignore


## [0.0.7] - 2021-08-23

### Added
- Create endpoint for change password

### Fixed

- add DS_Store to .gitignore
## [0.0.6] - 2021-08-22

### Added

- Create endpoints for change email

### Fixed
- Add change into user profile test

## [0.0.5] - 2021-08-21

### Added
- add database in settings
- add path verify and sign up
- add two views VerifyJsonWebToken and SignUpView
- add SignUp serializer
- create token.py
- add sign up tests

### Fixed

- remove username from required fields
- add small note re point

## [0.0.4] - 2021-08-20

### Added
- Create user profile

### Fixed
- Change task
- Add different url to Reminder

- Attempt to fix the version being read dynamically in `setup.py`

## [0.0.3] - 2021-08-19

### Added

- Install django-restframework,
- django-cors-headers
- add urls ot Remind url
- add JWT token
- add test JWT token

## [0.0.2] - 2021-08-18

### Added

- Create new app
- add custom user
- add it in settings
- register user in admin site

### Fixed

- add .data in .gitignore

## [0.0.1] - 2021-08-18
### Added

- Create git repository
- add pipfile
- .gitignore
- install django!



[0.0.1]: https://github.com/InkSmile/RemindMe/commit/906c056cc414426b3c4738c19ce91bcc93b25f7d
[0.0.2]: https://github.com/InkSmile/RemindMe/commit/9f8f805101ebf909ace46da04656419014a133fd
[0.0.3]: https://github.com/InkSmile/RemindMe/commit/9a0dd86410e891341ef16fe1e7ce4b7036c8d696
[0.0.4]: https://github.com/InkSmile/RemindMe/commit/d971c4e2c1c023ef6aeed4c70cd54bf3bb45508e
[0.0.5]: https://github.com/InkSmile/RemindMe/commit/3bffa9c6bd52501166a8bee2409acac14affe8ec
[0.0.6]: https://github.com/InkSmile/RemindMe/commit/403a221a103685b64f600c2f03e2eafc49495a32
[0.0.7]: https://github.com/InkSmile/RemindMe/commit/4ce9485439ce38562be001edad72a458d084607b
[0.0.8]: https://github.com/InkSmile/RemindMe/commit/822ac6dd787b5929780946f3608b5a17c9fe4ea2
[0.0.9]: https://github.com/InkSmile/RemindMe/commit/2492b8d49212e8af8c3dbfeda680c18faf3db6de
[0.1.0]: https://github.com/InkSmile/RemindMe/commit/f70f4d2f636ae15e009c6d988d49da38bcaf7025
[0.1.1]: https://github.com/InkSmile/RemindMe/commit/836f68ee1e9084820428573a3622762d01abcd5d
[0.1.2]: https://github.com/InkSmile/RemindMe/commit/2ea1bc534d526e90caa4d47fbdc392ed283af4c9
[0.1.3]: https://github.com/InkSmile/RemindMe/commit/756bdd6826e7f556a56e40be29558b48af115786
[0.1.4]: https://github.com/InkSmile/RemindMe/commit/f63ca019ec53f613af04d44b7f697283c0fcc7eb