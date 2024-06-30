import os
import yaml

project_dir = os.getcwd()
MOUNTPOINT_PREFIX = os.environ.get("MOUNTPOINT_PREFIX", project_dir)
with open(os.path.join(MOUNTPOINT_PREFIX, 'common_settings.yml'), 'r') as f:
    local_settings = yaml.safe_load(f)

sigma1 = local_settings['SIGMA1']
sigma2 = local_settings['SIGMA2']
delta1 = local_settings['DELTA1']
delta2 = local_settings['DELTA2']
ldap_domain_sigma = local_settings['LDAP_DOMAIN_SIGMA']
