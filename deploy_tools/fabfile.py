from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/lucamel/todolist.git'


def deploy(folder=''):
    if not folder:
        folder = env.host

    site_folder = f'/home/{env.user}/sites/{folder}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(source_folder)
    _create_or_update_dotenv(source_folder, env.host)
    _update_static_files(source_folder)
    _update_database(source_folder)

    if(input("Is first deploy? [Y|n] ") == "Y"):
        print('\n***** \n\nConfiguring nginx virtualhost and gunicorn ... \n\n*****\n\n')
        _set_nginx_virtualhost(source_folder, folder, env.host)
        _set_gunicorn(source_folder, folder)
        _restart_server(folder)
    else:
        if(input("Do you want to restart gunicorn? [Y|n] ") == "Y"):   
            _restart_gunicorn(folder)

    print('\n===== \n\nDeploy completed!! \n\n===== \n\n')


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _create_or_update_dotenv(source_folder, site_name):
    append(f'{source_folder}/.env', f'SITENAME={env.host}')
    append(f'{source_folder}/.env', f'DJANGO_DEBUG=False')
    append(f'{source_folder}/.env', f'DJANGO_STATIC_FILES_DIR="assets"')
    append(f'{source_folder}/.env', f'DJANGO_ALLOWED_HOSTS=[{site_name}]')
    append(f'{source_folder}/.env', f'WEBPACK_STATS_FILE="webpack-stats-prod.json"')
    append(f'{source_folder}/.env', f'EMAIL_HOST="smtp.mailtrap.io"')
    append(f'{source_folder}/.env', f'EMAIL_HOST_USER="3fdb140d8ed5d7"')
    append(f'{source_folder}/.env', f'EMAIL_PORT="2525"')
    append(f'{source_folder}/.env', f'EMAIL_HOST_PASSWORD=4a5e23299267e7')
    current_contents = run('cat .env')  
    if 'DJANGO_SECRET_KEY' not in current_contents:  
        new_secret = ''.join(random.SystemRandom().choices(  
            'abcdefghijklmnopqrstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')

def _update_static_files(source_folder):
    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_folder):    
    run(f'cd {source_folder}'
    ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )

def _set_nginx_virtualhost(source_folder, folder, site_name):
    run(f'sed "s/SITENAME/{site_name}/g" {source_folder}/deploy_tools/nginx.template.conf | sudo tee /etc/nginx/sites-available/{folder}')
    run(f'sed "s/FOLDERNAME/{folder}/g" /etc/nginx/sites-available/{folder} | sudo tee /etc/nginx/sites-available/{folder}')
    run(f'sudo ln -s ../sites-available/{folder} /etc/nginx/sites-enabled/{folder}')

def _set_gunicorn(source_folder, folder):
    run(f'sed "s/FOLDERNAME/{folder}/g" {source_folder}/deploy_tools/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-{folder}.service')

def _restart_server(folder):
    run('sudo systemctl daemon-reload && sudo systemctl reload nginx')
    run(f'sudo systemctl enable gunicorn-{folder} && sudo systemctl start gunicorn-{folder}')

def _restart_gunicorn(folder):
    run(f'sudo systemctl restart gunicorn-{folder}')