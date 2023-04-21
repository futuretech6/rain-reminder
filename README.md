# Rain Reminder

Get an email if it will rain tomorrow.

## How to use

1. fork this repo
2. acquire an API key at https://home.openweathermap.org/api_keys and fill it as a GitHub secret with the name "APIKEY"
3. change the ["config.toml"](/config.toml) to match your location(s), you can use https://www.google.com/maps/@{lat},{lon} to locate

There will be an email sent by the GitHub Actions bot to you at 20:30 (utc+8) if it's rainy tomorrow.
