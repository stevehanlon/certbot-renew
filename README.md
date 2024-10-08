# certbot-renewal

Certbot renewal is a wordpress plugin which will create the .well-known/acme-challenge files via the REST API.

This is a script for generating certificates on a local machine. They still need to be copied to the webserver perhaps by modifying the scripts in the `./shell` subfolder.

## Installation

Copy the files into wp-content/plugins/certbot-renewal.

## Usage

The shell folder has some example methods for launching the script. Set up an application password on the wordpress site and then create a config .ini file. The script will look for config.ini or the filename can be passed in RENEW_CONFIG. Check the `example_script` for details.

config.ini: 

```ini
[wordpress]
domain = example.com
username = USERNAME
application_password = PASSWORD
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
