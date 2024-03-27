# KDM-Finder
Find KDMs in your emails

`Project language: English`



## Short Description
KDM-Finder is an application developed for cinemas, simplifying the search for KDMs (Key Delivery Messages) within an email account.

A KDM (Key Delivery Message) is required to play an encrypted DCP movie. This is typically is provided as a `.xml` file.

The application is written in Python and uses the PyQt6 UI library.



## Platform
KDM-Finder should work on all platforms supporting Python and PyQt6. However, the application was only tested on Linux (Ubuntu 22.04). 

Functionality under macOS or Windows has not been tested.



## Use KDM-Finder

### Dependencies
Make sure you have Python and PyQt6 installed. The latter can be installed with `pip install PyQt6`.

The application is tested with:
- Python 3.10.12
- PyQt6 6.6.1

### Run and Install
To use KDM-Finder, download the source code of the latest version from GitHub (as a `.zip` file or via `git clone`).

You can also use this link: https://github.com/bdav-dev/kdm-finder/archive/refs/heads/main.zip

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
- `/usr/share/applications/`, if you want to install KDM-Finder system wide for all users


## Functionality
### Email
The connection to your email account is established via IMAP. KDM-Finder needs the following information to establish an email connection:
- IMAP server
- email address
- password

> Note: On a Gmail account, the password is not the password to your google account. You need to enter an 'app password'. Read this article to learn how to create one: https://support.google.com/accounts/answer/185833?hl=en


You can also specify ...
- ... how many emails KDM-Finder should fetch for the search (sorted by receipt time, latest first).
- ... if KDM-Finder should automatically start the search on application startup.

### Search
KDM-Finder fetches the latest emails and determines if an email contains a KDM. An email is considered contain a KDM if
- the email content, subject or sender contain (case ignored) `kdm` or `key` and
- the email has an attachment with `.zip` or `.xml` as the file extension.

When all emails are fetched, the found KDMs are displayed in a list. For each KDM the following information is displayed:
- The filename (with extension) of the attachment
- The sender of the email
- The subject of the email

A 'View' button is also present for each KDM, making it possible to view the entire email.

### Save
You can select the KDMs you want to save by clicking on them in the list. When you selected all KDMs you want to save, click the 'Save selected' button.

Now, you can locate to a directory in your file system in which the KDMs should be saved.

> Note: If you save a `.zip` file, the contents of the file will be extracted and saved, rather than the `.zip` file itself.
