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
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)

    if(input("Is first deploy? [Y|n] ") == "Y"):
        print('\n***** \n\nConfiguring nginx virtualhost and gunicorn ... \n\n*****\n\n')
        _set_nginx_virtualhost(source_folder, folder, env.host)
        _set_gunicorn(source_folder, folder)
    
    print('\n===== \n\nDeploy completed!! \n\n===== \n\n')
    if(input("Do you want to restart server and enable new service? [Y|n] ") == "Y"):   
        _restart_server(folder)


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

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')
    staticfiles_dirs_file = source_folder + '/superlists/staticfiles_dirs.py'
    if not exists(staticfiles_dirs_file):
        append(staticfiles_dirs_file, f'DIR = "assets"')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

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