# SocialnetworkToolkit

The purpose of this project is to furnish different tools to grab contents, post automatically and the future versions follow/ unfollow/ like users on differents social network.

## Requirement

  - Python 3.7
  - Sqlite
  - Firefox
  - Geckodriver

To install the different libraries for Python :

```shell
pip install -r requirements.txt
```

## Apply migration

```shell
alembic upgrade head
```

## Different applications

### grab_image_instagram.py

The purpose is to retrieve image in a public instagram account. For this content, the description is saved and modified (the tags with **#insta** is deleted, and the words begin by **@** are deleted)

The images are saved in Sqlite with the date of publication and the md5 of the picture.
The images are savec in filesystem too.

|Parameter | Description|
|----------|-------------|
|--username=USERNAME | Define the username of the public account|
|--url_target=URL| Define the url to attached at this picture when the picture is posted on Pinterest or added to the message in Twitter|
|--headless | Enable the headless mode in Firefox|

## post_pinterest.py

The purpose is to post images and its description in Pinterest. The script uses images saved in database by taking the oldest and not already posted.

If the description exceed 500 characters, it will be ignored

|Parameter | Description|
|----------|-------------|
|--username=USERNAME | Define the username to connect to Pinterest|
|--password=PASSWORD| Define the password to connect to Pinterest|
|--board=BOARD| Select the board in Pinterest where the image will be posted|
|--simulate| Don't publish the picture, don't flag in database|
|--headless | Enable the headless mode in Firefox|

## post_twitter.py

The purpose is to post images and its description in Twitter. The script uses images saved in database by taking the oldest and not already posted.

If the description exceed 240 characters, it will be ignored

|Parameter | Description|
|----------|-------------|
|--username=USERNAME | Define the username to connect to Twitter|
|--password=PASSWORD| Define the password to connect to Twitter|
|--simulate| Don't publish the picture, don't flag in database|
|--headless | Enable the headless mode in Firefox|

## random_sleep.py
Create a random sleep between 5 min and 45 minutes.
The purpose is to use in crontab and avoid to post the message at the same time.
