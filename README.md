# AgeRating

## App downloader

### Setup
1. Install the [PlaystoreDownloader](https://github.com/ClaudiuGeorgiu/PlaystoreDownloader)
2. Copy scripts into the PlaystoreDownloader folder

### Usage
* Make sure the configuration file is updated according to describtion in the [configuration](https://github.com/ClaudiuGeorgiu/PlaystoreDownloader#-configuration)
```Python
python app_review_downloader.py [-h] [-t CATEGORY] [-n NUMBER] [-d DETAIL] [-c COLLECTION] [-r N_REVIEWS]
```

#### Available parameters

* `-n` is the number of apps to be downloaded. Default = 5.
* `-r` is the number of reviews to be downloaded. Default = 3000.
* `-c` is the collection of apps. Default = "APPLICATION".
```
TOP_FREE = 'topselling_free',                           TOP_PAID = 'topselling_paid',
NEW_FREE = 'topselling_new_free',                       NEW_PAID = 'topselling_new_paid',
GROSSING = 'topgrossing',                               TRENDING = 'movers_shakers',
TOP_FREE_GAMES = 'topselling_free_games',               TOP_PAID_GAMES = 'topselling_paid_games',
TOP_GROSSING_GAMES = 'topselling_grossing_games',       NEW_FAMILY = 'topselling_new_family'
```
* `-t` is the category of apps.
```
APPLICATION = 'APPLICATION',                            ANDROID_WEAR = 'ANDROID_WEAR',
ART_AND_DESIGN = 'ART_AND_DESIGN',                      AUTO_AND_VEHICLES = 'AUTO_AND_VEHICLES',
BEAUTY = 'BEAUTY',                                      BOOKS_AND_REFERENCE = 'BOOKS_AND_REFERENCE',
BUSINESS = 'BUSINESS',                                  COMICS = 'COMICS',
COMMUNICATION = 'COMMUNICATION',                        DATING = 'DATING',
EDUCATION = 'EDUCATION',                                ENTERTAINMENT = 'ENTERTAINMENT',
EVENTS = 'EVENTS',                                      FINANCE = 'FINANCE',
FOOD_AND_DRINK = 'FOOD_AND_DRINK',                      HEALTH_AND_FITNESS = 'HEALTH_AND_FITNESS',
HOUSE_AND_HOME = 'HOUSE_AND_HOME',                      LIBRARIES_AND_DEMO = 'LIBRARIES_AND_DEMO',
LIFESTYLE = 'LIFESTYLE',                                MAPS_AND_NAVIGATION = 'MAPS_AND_NAVIGATION',
MEDICAL = 'MEDICAL',                                    MUSIC_AND_AUDIO = 'MUSIC_AND_AUDIO',
NEWS_AND_MAGAZINES = 'NEWS_AND_MAGAZINES',              PARENTING = 'PARENTING',
PERSONALIZATION = 'PERSONALIZATION',                    PHOTOGRAPHY = 'PHOTOGRAPHY',
PRODUCTIVITY = 'PRODUCTIVITY',                          SHOPPING = 'SHOPPING',
SOCIAL = 'SOCIAL',                                      SPORTS = 'SPORTS',
TOOLS = 'TOOLS',                                        TRAVEL_AND_LOCAL = 'TRAVEL_AND_LOCAL',
VIDEO_PLAYERS = 'VIDEO_PLAYERS',                        WEATHER = 'WEATHER',
GAME = 'GAME',                                          GAME_ACTION = 'GAME_ACTION',
GAME_ADVENTURE = 'GAME_ADVENTURE',                      GAME_ARCADE = 'GAME_ARCADE',
GAME_BOARD = 'GAME_BOARD',                              GAME_CARD = 'GAME_CARD',
GAME_CASINO = 'GAME_CASINO',                            GAME_CASUAL = 'GAME_CASUAL',
GAME_EDUCATIONAL = 'GAME_EDUCATIONAL',                  GAME_MUSIC = 'GAME_MUSIC',
GAME_PUZZLE = 'GAME_PUZZLE',                            GAME_RACING = 'GAME_RACING',
GAME_ROLE_PLAYING = 'GAME_ROLE_PLAYING',                GAME_SIMULATION = 'GAME_SIMULATION',
GAME_SPORTS = 'GAME_SPORTS',                            GAME_STRATEGY = 'GAME_STRATEGY',
GAME_TRIVIA = 'GAME_TRIVIA',                            GAME_WORD = 'GAME_WORD',
FAMILY = 'FAMILY',                                      FAMILY_ACTION = 'FAMILY_ACTION',
FAMILY_BRAINGAMES = 'FAMILY_BRAINGAMES',                FAMILY_CREATE = 'FAMILY_CREATE',
FAMILY_EDUCATION = 'FAMILY_EDUCATION',                  FAMILY_MUSICVIDEO = 'FAMILY_MUSICVIDEO',
FAMILY_PRETEND = 'FAMILY_PRETEND'
```
#### Output paths
* Apk files: ./Downloads
* App list: ./Downloads/App_list
* Reviews: ./Downloads/Reviews

#### Example 1
* To download 200 top free apps and 3,000 reviews for each app in Education category: 
```Python
python app_review_downloader.py -c TOP_FREE -t EDUCATION -n 200
```
#### Example 2
* To download 100 top new release apps and 2,000 reviews for each app:
```Python
python app_review_downloader.py -c NEW_FREE -n 100 -r 2000
```
Note that the `CATEGARY` will be set to "Application" as there is no category for newly release apps in Play Store.
#### Example 3
* To download 100 top new released `FAMILY` apps and 1,000 reviews for each app:
```Python
python app_review_downloader.py -c NEW_FAMILY -t FAMILY -n 100 -r 2000
```

