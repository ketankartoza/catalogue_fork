FROM kartoza/pg-backup:9.4
MAINTAINER Rischan Mafrur <rischann@kartoza.com>

ADD backups.sh /backups.sh
RUN chmod 755 /backups.sh

CMD ["/start.sh"]