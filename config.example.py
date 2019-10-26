# To use this file rename it to config.py

class Config(object):
    DEBUG = False
    
    # Path where audio files are stored
    # AUDIO_PATH = ''

    # Path where audio validator can save its data
    # DATA_PATH = ''

    # Available languages that have data and can be validated
    # AVAILABLE_LANGUAGES = [
    #     {
    #         'code': 'et',
    #         'name': 'Estonian'
    #     }
    #     ...
    # ]

    # Languages that are displayed as checkboxes on the validation page
    VALIDATION_LANGUAGES = [
        {
            'code': 'et',
            'name': 'Estonian'
        },
        {
            'code': 'en',
            'name': 'English'
        },
        {
            'code': 'fi',
            'name': 'Finnish'
        },
        {
            'code': 'ur',
            'name': 'Urdu'
        },
        {
            'code': 'de',
            'name': 'German'
        },
        {
            'code': 'es',
            'name': 'Spanish'
        },
        {
            'code': 'lv',
            'name': 'Latvian'
        },
        {
            'code': 'ru',
            'name': 'Russian'
        },
        {
            'code': 'OTHER',
            'name': 'Other'
        },
        {
            'code': 'NO_LANGUAGE',
            'name': 'No language'
        }
    ]

    # How many audio files to display on page
    ITEMS_ON_PAGE = 10
