import random
import logging
import traceback
import variables
from ldap3 import Server, Connection, SUBTREE


sigma1 = variables.sigma1
sigma2 = variables.sigma2
delta1 = variables.delta1
delta2 = variables.delta2
ldap_domain_sigma = variables.ldap_domain_sigma

LDAP_AUTH_DOMAIN = domain = 'sigma'  # или 'delta'
LDAP_AUTH_HOSTS = [sigma1, sigma2] if domain == ldap_domain_sigma else [delta1, delta2]
LDAP_AUTH_SUFFIX = '@{}.sbrf.ru'.format(domain)
LDAP_AUTH_SEARCH_BASE = 'dc={},dc=sbrf,dc=ru'.format(domain)
ldap3_auth = 'ldap3_auth'

LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
    "EmployeeID": "EmployeeID"
}


def get_ldap_info(username=None, password=None, ldap3_type=None, client_ue=None):
    ldap_host = LDAP_AUTH_HOSTS[round(random.random())]
    bind_dn = '{}{}'.format(username, LDAP_AUTH_SUFFIX)
    logging.info(f'bind_dn - {bind_dn}')
    server = Server(ldap_host)

    if ldap3_type == ldap3_auth:
        filter = f'(&(objectCategory=Person)(objectClass=User)(mail={client_ue}))'
    else:
        employee_id_filter = str()
        #for personal_number in [employee.personal_number for employee in User.objects.filter(is_visible=True)]:
        #    employee_id_filter += f"(EmployeeID={personal_number})"
        employee_id_filter += f"(EmployeeID=1951853)"
        filter = f"(&(objectCategory=Person)(objectClass=User)(|{employee_id_filter}))"

    employees = {}
    personal_info = {'first_name': '',
                     'last_name': '',
                     'EmployeeID': ''}

    users_info = get_ldap3_users_info(
        Connection(server, user=bind_dn, password=password),
        filter
    )

    if users_info:
        for entry in users_info:
            userinfo = {}
            if 'attributes' in list(entry):
                for k, v in LDAP_AUTH_USER_FIELDS.items():
                    userinfo[k] = entry['attributes'][v]

                if str(username).lower() == str(userinfo['username']).lower():
                    personal_info['first_name'] = userinfo['first_name']
                    personal_info['last_name'] = userinfo['last_name']
                    personal_info['EmployeeID'] = userinfo['EmployeeID']

                employees[userinfo['EmployeeID']] = {'username': userinfo['username'],
                                                     'first_name': userinfo['first_name'],
                                                     'last_name': userinfo['last_name'],
                                                     'email': userinfo['email']}
    return {'personal_info': personal_info, 'employees': employees}


def get_ldap3_users_info(connection, filter):
    if connection.bind():
        try:
            connection.search(search_base=LDAP_AUTH_SEARCH_BASE,
                              search_filter=filter,
                              search_scope=SUBTREE, attributes=list(LDAP_AUTH_USER_FIELDS.values()), paged_size=250)
            return connection.response
        except Exception as e:
            traceback.format_exc()
            logging.error(e)
    return []
