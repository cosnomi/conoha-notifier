import os

# These values are fixed in effect. No need to be configured by users.
const_config = {
    'CONOHA_TOKEN_URL': 'https://identity.tyo2.conoha.io/v2.0/tokens',
    'CONOHA_DATE_FORMAT': '%Y-%m-%dT%H:%M:%SZ'
}


def read_config():
    # These values must be assigned by users as the environment variables.
    env_config_key_list = [
        'CONOHA_API_USER', 'CONOHA_API_PW', 'CONOHA_TENANT_ID',
        'CONOHA_ACCOUNT_SERVICE_URL'
    ]
    config = {}
    for config_key in env_config_key_list:
        config[config_key] = os.environ[config_key]
    return config