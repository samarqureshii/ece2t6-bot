from __future__ import annotations

import logging
import configparser
import os

import ece2t6_bot.bot as bot


def _load_config(path: str = 'config.ini'):
    config = configparser.ConfigParser()

    if not os.path.isfile(path):
        raise Exception(f'Config does not exist at {path}, please copy config.example.ini to {path}!')
    
    config.read(path)

    return config


def _setup_logging(log_level: int | str):
    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level)

    logging.basicConfig(
        level=log_level,
        format='[%(asctime)s] [%(module)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def run():
    config = _load_config()
    _setup_logging(config['Launcher']['LogLevel'])

    logging.info('ece2t6-bot launching!')

    bot.run_bot(config['Discord']['Token'])


if __name__ == '__main__':
    run()
