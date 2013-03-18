#!/bin/python
# ~/fabfile.py
# A Fabric file for carrying out various administrative tasks.
# Tim Sutton, Jan 2013

# To use this script make sure you have fabric and fabtools.
# pip install fabric fabtools

import os
from fabric.api import *
from fabric.contrib.files import contains, exists, append, sed
import fabtools

# Usage fab localhost [command]
#    or fab remote [command]
#  e.g. fab localhost update

# This will get replaced in various places, for a generic site, it may be
# all you need to change...
PROJECT_NAME = 'catalogue'

def captured_local(command):
    """A wrapper around local that always returns output."""
    return local(command, capture=True)


def localhost():
    """Set up things so that commands run locally.

    To run locally do e.g.::

        fab localhost show_environment

    """
    env.run = captured_local
    env.hosts = ['localhost']
    _all()


def remote():
    """Set up things so that commands run remotely.
    To run remotely do e.g.::

        fab -H 188.40.123.80:8697 remote show_environment

        or if you have configured env.hosts, simply

        fab remote show_environment

    """
    env.hosts = ['foo.bar:8697']
    env.run = run
    _all()


# You are supposed to be able to run stuff using fabtools.vagrant
# but it didnt work for me when I tested it. This is an alternative approach
# from fabtools.vagrant import vagrant

def _get_vagrant_config():
    """
    Parses vagrant configuration and returns it as dict of ssh parameters
    and their values
    """
    result = local('vagrant ssh-config', capture=True)
    conf = {}
    for line in iter(result.splitlines()):
        parts = line.split()
        conf[parts[0]] = ' '.join(parts[1:])

    return conf


def vagrant():
    """
    Set up things so that commands run on vagrant vm.
    """

    env.settings = 'vagrant'
    # get vagrant ssh setup
    vagrant_config = _get_vagrant_config()
    #print vagrant_config
    env.key_filename = vagrant_config['IdentityFile']
    env.hosts = ['%s:%s' % (vagrant_config['HostName'], vagrant_config['Port'])]
    env.host_string = env.hosts[0]
    env.user = vagrant_config['User']
    env.run = run
    _all()


def _all():
    """Things to do regardless of whether command is local or remote."""

    # Key is hostname as it resolves by running hostname directly on the server
    # value is desired web site url to publish the repo as.

    repo_site_names = {
        'spur': '%s.localhost' % PROJECT_NAME,
        'waterfall': '%s.localhost' % PROJECT_NAME,
        'maps.linfiniti.com': '%s.linfiniti.com' % PROJECT_NAME,
        'owl': 'test.catalogue.sansa.org.za',
        # vagrant vm
        'precise64': '%s.localhost' % PROJECT_NAME}

    with hide('output'):
        env.user = env.run('whoami')
        env.hostname = env.run('hostname')
        if env.hostname not in repo_site_names:
            print 'Error: %s not in: \n%s' % (env.hostname, repo_site_names)
            exit()
        else:
            # sitename for apache venv
            env.repo_site_name = repo_site_names[env.hostname]
            # where to check the repo out to
            env.webdir = '/home/web'
            # repo uri
            env.git_url = 'git@github.com:timlinux/%s.git' % PROJECT_NAME
            # checkout name for repo
            env.repo_alias = PROJECT_NAME
            # user wsgi should run as (will be created if needed)
            env.wsgi_user = 'catalogue'
            # Deploy dir - e.g. /home/web/foo
            env.code_path = os.path.join(env.webdir, env.repo_alias)
            show_environment()

###############################################################################
# Next section contains helper methods tasks
###############################################################################


def replace_tokens(conf_file):
    env.run(
        'cp %(conf_file)s.templ %(conf_file)s' % {
            'conf_file': conf_file})
    # We need to replace these 3 things in the conf file:
    # [SERVERNAME] - web site base url e.g. foo.com
    # [ESCAPEDSERVERNAME] - the site base url with escaping e.g. foo\.com
    # [SITEBASE] - dir under which the site is deployed e.g. /home/web
    # [SITENAME] - should match env.repo_alias
    # [SITEUSER] - user apache wsgi process should run as
    # [CODEBASE] - concatenation of site base and site name e.g. /home/web/app
    escaped_name = env.repo_site_name.replace('.', '\\\.')
    fastprint('Escaped server name: %s' % escaped_name)
    sed('%s' % conf_file, '\[SERVERNAME\]', env.repo_site_name)
    sed('%s' % conf_file, '\[ESCAPEDSERVERNAME\]', escaped_name)
    sed('%s' % conf_file, '\[SITEBASE\]', env.webdir)
    sed('%s' % conf_file, '\[SITENAME\]', env.repo_alias)
    sed('%s' % conf_file, '\[SITEUSER\]', env.wsgi_user)
    sed('%s' % conf_file, '\[CODEBASE\]', env.code_path)


#
# We should get rid of this its not needed
#

def setup_vagrant():
    """We use vagrant for deploying virtual machines easily."""
    #http://files.vagrantup.com/precise64.box
    fabtools.require.deb.package('vagrant')
    env.run(
        'vagrant box add "Ubuntu precise 64" '
        'http://files.vagrantup.com/precise64.box')
    env.run('vagrant box init "Ubuntu precise 64"')

#
# We should get rid of this its not needed
#

def start_vagrant():
    env.run('vagrant box up')
    fastprint('You can ssh in to your vagrant box using "vagrant ssh"')


def setup_mapserver():
    # Clone and replace tokens in mapserver map file
    conf_dirs = [
        '%s/resources/server_config/mapserver/mapfiles/' % (env.code_path),
        '%s/resources/server_config/mapserver/apache-include/' % (
            env.code_path)]
    for conf_dir in conf_dirs:
        for myFile in os.listdir(conf_dir):
            myExt = os.path.splitext(myFile)[1]
            conf_file = os.path.join(conf_dir, myFile)

            if myExt == '.templ':
                replace_tokens(conf_file)

    # We also need to append 900913 epsg code to the proj epsg list
    epsg_path = '/usr/share/proj/epsg'
    epsg_code = (
        '<900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_'
        '0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs')
    epsg_id = '900913'
    if not contains(epsg_path, epsg_id):
        append(epsg_path, epsg_code, use_sudo=True)


def setup_postgres():
    # Ensure we have ubuntu-gis repos
    fabtools.require.deb.ppa('ppa:ubuntugis/ubuntugis-unstable')
    # Ensure we have a mailserver setup for our domain
    # Note that you may have problems if you intend to run more than one
    # site from the same server
    fabtools.require.postfix.server(env.repo_site_name)
    # Note - no postgis installation
    fabtools.require.postgres.server()


def setup_website():
    """Initialise or update the git clone.

    e.g. to update the server

    fab -H 10.1.1.0:8697 remote setup_website

    or if you have configured env.hosts, simply

    fab remote setup_website
    """

    # Find out if the wsgi user exists and create it if needed e.g.
    fabtools.require.user(
        env.wsgi_user,
        create_group=env.wsgi_user,
        system=True,
        comment='System user for running the wsgi process under')

    if not exists(env.webdir):
        sudo('mkdir -p %s' % env.plugin_repo_path)
        sudo('chown %s.%s %s' % (env.user, env.user, env.webdir))

    # Clone and replace tokens in apache conf

    conf_file = (
        '%s/resources/server_config/apache/%s.apache.conf' % (
            env.code_path, env.repo_alias))

    env.run(
        'cp %(conf_file)s.templ %(conf_file)s' % {
            'conf_file': conf_file})

    replace_tokens(conf_file)

    with cd('/etc/apache2/sites-available/'):
        if exists('%s.apache.conf' % env.repo_alias):
            sudo('a2dissite %s.apache.conf' % env.repo_alias)
            fastprint('Removing old apache2 conf', False)
            sudo('rm %s.apache.conf' % env.repo_alias)

        sudo('ln -s %s .' % conf_file)

    # wsgi user needs pg access to the db
    if not fabtools.postgres.user_exists(env.wsgi_user):
        fabtools.postgres.create_user(
            env.wsgi_user,
            password='',
            createdb=False,
            createrole=False,
            connection_limit=20)

    grant_sql = 'grant all on schema public to %s;' % env.wsgi_user
    # assumption is env.repo_alias is also database name
    env.run('psql %s -c "%s"' % (env.repo_alias, grant_sql))
    grant_sql = (
        'GRANT ALL ON ALL TABLES IN schema public to %s;' % env.wsgi_user)
    # assumption is env.repo_alias is also database name
    env.run('psql %s -c "%s"' % (env.repo_alias, grant_sql))
    grant_sql = (
        'GRANT ALL ON ALL SEQUENCES IN schema public to %s;' % env.wsgi_user)
    env.run('psql %s -c "%s"' % (env.repo_alias, grant_sql))

    #with cd(env.code_path):
        # run the script to create the sites view
        #env.run('psql -f sql/3-site-view.sql %s' % env.repo_alias)

    # Add a hosts entry for local testing - only really useful for localhost
    hosts = '/etc/hosts'
    if not contains(hosts, env.repo_site_name):
        append(hosts, '127.0.0.1 %s' % env.repo_site_name, use_sudo=True)
    if not contains(hosts, 'www.' + env.repo_site_name):
        append(hosts,
               '127.0.0.1 %s' % 'www.' + env.repo_site_name,
               use_sudo=True)
        # Make sure mod rewrite is enabled
    sudo('a2enmod rewrite')
    # Enable the vhost configuration
    sudo('a2ensite %s.apache.conf' % env.repo_alias)

    # Check if apache configs are ok - script will abort if not ok
    sudo('/usr/sbin/apache2ctl configtest')

    fabtools.require.service.restarted('apache2')

    #Setup a writable media dir for apache
    media_path = '%s/django_project/core/media' % env.code_path
    if not exists(media_path):
        sudo('mkdir %s' % media_path)
        sudo('chown %s.%s %s' % (env.wsgi_user, env.wsgi_user, env.code_path))


def tail_errors():
    """Tail the apache error log ot see if anything is failing.


    To run e.g.::

        fab -H 188.40.123.80:8697 remote tail_errors

    or if you have configured env.hosts, simply

        fab remote tail_errors
    """
    sudo('tail /var/log/apache2/%s.error.log' % PROJECT_NAME)


def setup_venv():
    """Initialise or update the virtual environmnet.


    To run e.g.::

        fab -H 188.40.123.80:8697 remote setup_venv

    or if you have configured env.hosts, simply

        fab remote setup_venv
    """

    with cd(env.code_path):
        # Ensure we have a venv set up
        fabtools.require.python.virtualenv('venv')
        env.run('venv/bin/pip install -r requirements-prod.txt')


def update_git_checkout(branch='master'):
    """Make sure there is a read only git checkout.

    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'

    To run e.g.::

        fab -H 188.40.123.80:8697 remote update_git_checkout

    or if you have configured env.hosts, simply

        fab remote update_git_checkout

    """
    fabtools.require.deb.package('git')
    if not exists(env.webdir):
        fastprint('Repo checkout does not exist, creating.')
        user = env.run('whoami')
        sudo('sudo mkdir %s' % env.webdir)
        sudo('chown %s.%s %s' % (user, user, env.webdir))
        with cd(env.webdir):
            env.run('git clone %s %s' % (env.git_url, env.repo_alias))
    else:
        fastprint('Repo checkout does exist, updating.')
        with cd(env.code_path):
            # Get any updates first
            env.run('git fetch')
            # Get rid of any local changes
            env.run('git reset --hard')
            # Get back onto master branch
            env.run('git checkout master')
            # Remove any local changes in master
            env.run('git reset --hard')
            # Delete all local branches
            env.run('git branch | grep -v \* | xargs git branch -D')

    with cd(env.code_path):
        if branch != 'master':
            env.run('git branch --track %s origin/%s' % (branch, branch))
            env.run('git checkout %s' % branch)
        else:
            env.run('git checkout master')
        env.run('git pull')
        env.run('./runcollectstatic.sh')
        wsgi_file = 'django_project/core/wsgi.py'
        env.run('touch %s' % wsgi_file)


def install_server():
    """Ensure that the target system has a usable apache etc. installation.

    Args:
        None

    Returns:
        None

    Raises:
        None
    """

    #### NOTE THIS IS INCOMPLETE STILL ####

    clone = env.run('which pdflatex')
    if '' == clone:
        env.run('sudo apt-get install git cgi-mapserver texlive-latex-extra'
                'python-sphinx texinfo dvi2png')

###############################################################################
# Next section contains actual tasks
###############################################################################


def deploy(branch='master'):
    """Do a fresh deployment of the site to a server.

    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'.

    To run e.g.::

        fab -H 188.40.123.80:8697 remote deploy

        or to package up a specific branch (in this case v1)

        fab -H 88.198.36.154:8697 remote deploy:v1

    For live server:

        fab -H 5.9.140.151:8697 remote deploy

    or if you have configured env.hosts, simply

        fab remote deploy
    """

    update_git_checkout(branch)
    setup_venv()
    setup_postgres()
    setup_website()
    setup_mapserver()



def build_documentation(branch='master'):
    """Create a pdf and html doc tree and publish them online.

    Args:
        branch: str - a string representing the name of the branch to build
            from. Defaults to 'master'.

    To run e.g.::

        fab -H 188.40.123.80:8697 remote build_documentation

    or to package up a specific branch (in this case minimum_needs)

        fab -H 88.198.36.154:8697 remote build_documentation:version-1_1

    or if you have configured env.hosts, simply

        fab remote build_documentation

    .. note:: Using the branch option will not work for branches older than 1.1
    """

    ### Still needs to be tested ###

    update_git_checkout(branch)
    install_server()

    dir_name = os.path.join(env.webdir, env.repo_alias, 'docs')
    with cd(dir_name):
        # build the tex file
        env.run('make latex')

    dir_name = os.path.join(env.webdir, env.repo_alias,
                            'docs', 'build', 'latex')
    with cd(dir_name):
        # Now compile it to pdf
        env.run('pdflatex -interaction=nonstopmode %s.tex' % env.repo_alias)
        # run 2x to ensure indices are generated?
        env.run('pdflatex -interaction=nonstopmode %s.tex' % env.repo_alias)


def show_environment():
    """For diagnostics - show any pertinent info about server."""
    fastprint('\n-------------------------------------------------\n')
    fastprint('User: %s\n' % env.user)
    fastprint('Host: %s\n' % env.hostname)
    fastprint('Site Name: %s\n' % env.repo_site_name)
    fastprint('Dest Path: %s\n' % env.webdir)
    fastprint('Wsgi User: %s\n' % env.wsgi_user)
    fastprint('Git Url: %s\n' % env.git_url)
    fastprint('Repo Alias: %s\n' % env.repo_alias)
    fastprint('-------------------------------------------------\n')
