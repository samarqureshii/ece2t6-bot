from __future__ import annotations

import logging
import configparser
import os
import discord

import ece2t6_bot.bot as bot


def _load_config(path: str = 'config.ini') -> configparser.ConfigParser:
    config = configparser.ConfigParser()

    if not os.path.isfile(path):
        raise Exception(f'Config does not exist at {path}, please copy config.example.ini to {path}!')
    
    config.read(path)

    return config


def _setup_logging(log_level: int | str) -> logging.Logger:
    if isinstance(log_level, str):
        log_level = logging.getLevelName(log_level)

    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = discord.utils._ColourFormatter()    # shamelessly stealing Discord's formatter

    handler.setFormatter(formatter)
    logger.setLevel(log_level)
    logger.addHandler(handler)

    return logging.getLogger('launcher')    # yes, separation of concerns, but this is convenient


def run():
    config = _load_config()
    logger = _setup_logging(config['Launcher']['LogLevel'])

    logger.info('ece2t6-bot launching!')

    bot.run_bot(config['Discord']['Token'])


if __name__ == '__main__':
    run()
