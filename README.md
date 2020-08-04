<h1 align="center">Welcome to reddit grab saved 👋</h1>
<p>
  <a href="https://github.com/mmohammadi9812/reddit-grab-saved/blob/master/LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/mmohammadi9812" target="_blank">
    <img alt="Twitter: mmohammadi9812" src="https://img.shields.io/twitter/follow/mmohammadi9812.svg?style=social" />
  </a>
</p>

> It grabs your saved posts and comments from reddit and saves them in csv and excel (xls) format

## Installation

``` sh
git clone https://github.com/mmohammadi9812/reddit-grab-saved
cd reddit-grab-saved
#python3 -m venv venv && source venv/bin/activate # (if you want to install it in a seperate environment)
pip3 install -r requirements.txt
```

## Usage

Go to [reddit apps page](https://reddit.com/prefs/apps/) and make an script app.
It will create a reddit app for you and will give you an id and a secret.
Create a `.env` file in folder of project and fill it with these lines:

``` sh
export CLIENT_ID=<your app client id>
export CLIENT_SECRET=<your app client secret>
export USER_AGENT="linux:<id>:1.0 (by /u/<username>)"
export REDDIT_USER_NAME=<your user name>
export REDDIT_PASSWORD=<your password>
```
Change right side of export lines with your app id and secret and other needed info

Then it's ready to run:

```sh
python3 main.py
```

## Author

👤 **Mohamamd Mohammadi**

* Twitter: [@mmohammadi9812](https://twitter.com/mmohammadi9812)
* Github: [@mmohammadi9812](https://github.com/mmohammadi9812)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/mmohammadi9812/reddit-grab-saved/issues). 

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Mohamamd Mohammadi](https://github.com/mmohammadi9812).<br />
This project is [MIT](https://github.com/mmohammadi9812/reddit-grab-saved/blob/master/LICENSE) licensed.

***
