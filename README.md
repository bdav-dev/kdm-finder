# KDM-Finder
Find KDMs in your emails 

`Project language: English`

Current Version: `1.1`


## Short Description
KDM-Finder is an application developed for cinemas, simplifying the search for KDMs (Key Delivery Messages) within an email account.

A KDM (Key Delivery Message) is required to play an encrypted DCP movie. KDMs are typically provided as `.xml` files.

The application is written in Python and uses the PyQt6 UI library.



## Platform
KDM-Finder should work on all platforms which support Python and PyQt6.
However, the application was only tested on Linux (Ubuntu 22.04).

Functionality under macOS or Windows has not been tested.



## Use KDM-Finder

### Dependencies
Make sure you have the following software installed:
- Python
- PyQt6 (can be installed with `pip install PyQt6`)
- On Linux: `libxcb-cursor0` (can be installed with `sudo apt install libxcb-cursor0`)

### Run and Install
To use KDM-Finder, download the source code of the latest version from GitHub using one of the following methods:
- Download as a `.zip` file: https://github.com/bdav-dev/kdm-finder/archive/refs/heads/main.zip
- Download via `git clone https://github.com/bdav-dev/kdm-finder.git`

#### Run
1. If needed, unzip the `.zip` file.
2. Execute the python file `main.py` located in the root directory of the project. On Linux, this can be done with `python3 path/to/main.py`

#### Install (Linux)
A `.desktop` file is provided (in the root directory of the project) to install KDM-Finder on Linux systems.

Modify the `Exec` and the `Icon` properties, pointing them to the correct files in your KDM-Finder installation:
- The `Exec` property should point the the `main.py` file
- The `Icon` property should point the the `kdm_finder_icon.png` file

Copy the `kdm_finder.desktop` file to
- `~/.local/share/applications/`, if you want to install KDM-Finder for the current user
- `/usr/share/applications/`, if you want to install KDM-Finder system-wide for all users



## Functionality

### Email
The connection to your email account is established via IMAP. KDM-Finder needs the following information to establish an email connection:
- IMAP server
- email address
- password

> **Note**<br/>
> On a Gmail account, the password is not the password to your google account. You need to enter an 'app password'.<br/>
> Read this article to learn how to create one: https://support.google.com/accounts/answer/185833?hl=en

You can also specify ...
- ... how many emails KDM-Finder should fetch for the search (sorted by receipt time, most recent are fetched first).
- ... if KDM-Finder should automatically start the search on application startup.

### Search
KDM-Finder fetches the latest emails and determines if an email contains a KDM. An email is considered to contain a KDM if
- the email content, subject, sender or attachment contain (case ignored) `kdm` or `key` and
- the email has an attachment with `.zip` or `.xml` as the file extension.

When all emails are fetched, the found KDMs are displayed in a list. For each KDM the following information is displayed:
- The filename (with extension) of the attachment
- The sender of the email
- The subject of the email

A 'View' button is also present for each KDM, making it possible to view the entire email.

### Save
You can select the KDMs you want to save by clicking on them in the list.
When you selected all KDMs you want to save, click the 'Save selected' button.

Now, you can locate to a directory in your file system in which the KDMs should be saved.

> **Note**<br/>
> If you save a `.zip` file, the contents of the file will be extracted and saved, rather than the `.zip` file itself.


## Known Issues
- The application windows don't appear in the middle of the screen on Linux when using Wayland