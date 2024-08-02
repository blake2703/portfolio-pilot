import os

class Config:
    pass

class DevConfig(Config):
    pass

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}