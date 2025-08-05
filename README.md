# Draft SMS "NAS"

This is a command line tool that allows you to send, load and remove files from and to your TP-Link MR series router draft SMS inbox (tested only on my TL-MR150 and works only for LTE routers with a SIM card). It doesn't require custom firmware (mine is 1.3.0 0.9.1 v0001.0 Build 220315)

This project was created more as a proof of concept and file transfer speeds are really low (especially removing files), but it was still a fun thing to make.

It uses my [fork](https://github.com/mikolaj44/TP-Link-Archer-C6U-Draft-SMS) of the [tplinkrouterc6u package](https://github.com/AlexandrErohin/TP-Link-Archer-C6U) that adds more SMS functionality.

### Don't send "large" files! 100 KB is almost a large file for this system! Besides the speed, the router's internal memory is very small, probably a few MB in size.

### Remember that when using this program your draft inbox will be cleared in order to prepare the memory!
## Installation

Just clone this project and enter in your virtual environment:

```bash
  pip install /path/to/draft-sms-nas
```
You can also install it globally with pipx or however you like.
## Usage

Enter this console command in your virtual environment or globally, depending on how you installed it:

```bash
  smsnas
```

This will open up a text interface to work with files:

<img width="1103" height="793" alt="image" src="https://github.com/user-attachments/assets/a91d1118-5f55-4570-875c-81af8422b10c" />

### user_config.json

You can safely edit this file.

```json
  "url": "192.168.1.1",        your router url
  "show-warnings": true        show warnings on startup
```

If you set a non-string or wrong IPv4 format url then it will prompt you to set it.

### program_config.json

I don't recommend editing this file unless you are facing some issues with your model.

**is_initial_setup**: if true it will clear your draft inbox to prepare the memory, then it's set to false - you can manually set it to true in order to clear it.

**num_messages_per_page**: maximum number of messages that fit on one page in the draft inbox, this will be automatically determined if it's <= 0 or a non-number. This value is 8 for my router.

**num_messages_to_send_to_find_num_per_page**: the program will send this many messages to determine how much are on a page, this value **won't** be automatically set.

max_bytes_per_message: max number of 1-byte utf-8 characters you can send in a message. This number is 1430 for my router and it **won't** be automatically set.

#### Important detail: you can only send about 730 characters in the browser router page because the input box won't allow more, but the tplinkrouterc6u library can send more through API requests.

```json
  "is_initial_setup": true,
  "num_messages_per_page": 0,
  "num_messages_to_send_to_find_num_per_page": 15,  
  "max_bytes_per_message": 1430,
```
