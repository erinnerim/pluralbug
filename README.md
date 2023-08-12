
# Table of Contents

1.  [Pluralbug 🐞: A Pluralkit for Matrix](#org57531f0)
    1.  [nio-template](#org1adb03f)
    2.  [Setup](#org6f845b2)
        1.  [Notes on Current Limitations and Further Improvements](#org7eda6c9)
    3.  [Bot Commands](#orgc4e31c0)


<a id="org57531f0"></a>

# Pluralbug 🐞: A Pluralkit for Matrix

This project intends to port [pluralkit](https://pluralkit.me/) to [Matrix](https://matrix.org/). Pluralbug is a bot that can be invited into a room in Matrix. It keeps track of custom display names and their associated profile images and fronts specified messages with the custom system members information, allowing a system to present and maintain multiple "pseudo-accounts" under one Matrix user.


<a id="org1adb03f"></a>

## nio-template

The implementation of Pluralbug is based on the [nio-template](https://github.com/anoadragon453/nio-template) project by github user anoadragon453, which is a template for creating bots with the [matrix-nio](https://github.com/poljar/matrix-nio) Matrix client library. Thank you for your contribution to this software. More information on the specifics of implementation can be found in the documentation of that project, and by the [documentation](https://matrix-nio.readthedocs.io/en/latest/#api-documentation) for matrix-nio.


<a id="org6f845b2"></a>

## Setup

1.  Create a copy of `sample.config.yaml` named `config.yaml`.
2.  Change the `user_id`, `user_password` and `homeserver_url` and other relevant information in `config.yaml`.
    1.  Think of a name for your new pluralbug. For instance, if your username is "alice", you could name your bug "alicebug".
    2.  Register a new matrix user with that name, e.g. `alicebug` and generate a secure password (you can use the command `./nkey` included in this repository for a randomized 16-digit password). Make sure to register that user on your homeserver, i.e. sign up for a new account with the username and password of your bug.
    3.  Place those entries in the `user_id`, `user_password` fields of your new `config.yaml` file to those of the userbug instance you just created.
    4.  Change the `homeserver_url` field in your `config.yaml` file to the url of the homeserver on which you are hosting your userbug, e.g. `https://matrix.org` or your own homeserver.
3.  Follow the installation instructions for nio-template as they pertain to this repository. In so doing, creating a python virtual environment.
    1.  `cd pluralbug` to change to the root directory of this project.
    2.  `python -m venv ./venv/` to create a virtual environment to install pluralbug within.
        Note, you may need to install python, pip, and virtualenv in order for this to work.
    3.  `source ./venv/bin/activate` to activate the newly created virtual environment.
        Note, depending on your terminal emulator, this will likely prepend a `(venv)` to your command prompt, so you know the virtual environment is now active.
    4.  `pip install -e .` to, according to nio-template, "properly install this script into your python environment".
4.  With this virtual environment still activated, the execute the `./pluralbug_run` command.
5.  Invite the pluralbug user to a matrix room.


<a id="org7eda6c9"></a>

### Notes on Current Limitations and Further Improvements

-   You may need to grant your bug moderator privileges in your matrix room for the intended effects, for instance, auto-deleting messages. In some situations, this might require asking your room admin to grant your bot moderator privileges, or at least the privileges to delete other people's messages in the room.
-   Depending on your matrix client, you may see a host of notifications that your bug has deleted such-and-such message. These notification might be annoying or disruptive to the visual flow of conversation. In some clients, such as Element, these may be disabled on a per-room basis. However, other users will still see these notifications unless they also configure their clients similarly.
-   If you invite your bug to a room, *other users in that room will also have the ability to use your bug*, in ways such as sending messages via your bug using the same commands that you do, or even deleting previous messages. Support for verifying the username of a given post before executing bot commands is a possible improvement for future releases of pluralbug. As far as I know, there is not a way to have the intended support for pluralbug, i.e. replacing user messages, without granting room-wide access to the same, from the admin side.
    -   Note that in some circumstances, this may result in unintended behavior for other users in the room; pluralbug might delete their messages when they don't want them to, if their message happens to match the command prefix of your bot!
-   Conflicts with multiple pluralbug users in the same room could lead to unintended or even undefined behavior, and is largely untested at this stage. It is recommended to customize your command prefix beyond the default to at least mitigate these conflicts.
-   Your pluralbug must be running at all times in order to access its functionality. As this is not persistent across reboots to your client system, activating your virtual environment and running the `pluralbug_run` command every time you wish to communicate over matrix could be tedious.
    -   A possible iteration could create a systemd service to run pluralbug as a daemon. One could also run pluralbug on a separate always-on server. If you host your own matrix server, you could theoretically run pluralbug on the same server. But if you have multiple users hosted on your server who wish to use pluralbug, they would also require separate processes for each of them.
        -   Alternatively, mlutiple users in a given room could agree to share the same process. A practical application of this approach would probably require support for multiple command prefixes in a single instance, which pluralbug does not currently support.
-   If you wish to improve on any of these features, or have ideas for other features or improvements, please send a pull request! Your skills will be greatly appreciated.


<a id="orgc4e31c0"></a>

## Bot Commands

Customize the bot commands to your convenience in `bot_commands.yaml`.

-   The default command prefix for pluralbug is `-pb`. This can be changed in `config.yaml`.
-   "-pb sw" for "switch". Example: "-pb sw"
    -   "-pb sw name /path/to/file" switches user and changes pfp simultaneously.
    -   "-pb sw name" switches user only. Previously updated pfp associated with that user will be changed also. If no image has been set for that user, then the pfp will be default.
-   "-pb re" for "react". Example "-pb re ⭐"
-   "-pb del" for "delete". Example "-pb del <message>" will immediately delete its own message. Used mainly for testing purposes.
-   "-pb r" for "replace". This is usually the most common command to be used. Example "-pb r <message>" will delete this message and replace it with one sent by pluralbug containing the same text.
-   "-pb help" to display options.
-   "-pb pfp" to change profile picture. Currently only .png images are accepted. Example:
    -   "-pb pfp name *path/to/file*" will change the profile picture for the current (pseudo) user.

