#!/bin/sh
# start redis daemon, and run tests, kill the daemon when tests are complete
# Author: Elan Ruusamäe <glen@delfi.ee>
# $Id$

export REDIS_SERVER_PORT=$((6380 + RANDOM % 10))

cat > redis.conf <<EOF
bind 127.0.0.1

daemonize no
#pidfile redis.pid
port $REDIS_SERVER_PORT
bind 127.0.0.1
timeout 300
loglevel warning
logfile stdout

#databases 16
#save 900 1
#save 300 10
#save 60 10000
#rdbcompression yes
#dbfilename dump.rdb
#dir .
#appendonly no
#appendfsync everysec
#vm-enabled no
#vm-swap-file redis.swap
#vm-max-memory 0
#vm-page-size 32
#vm-pages 134217728
#vm-max-threads 4
#glueoutputbuf yes
#hash-max-zipmap-entries 64
#hash-max-zipmap-value 512
#activerehashing yes
EOF

# kill any previous daemon
kill $(cat redis.pid 2>/dev/null) 2>/dev/null
# setup hook to terminate on shutdown
trap 'set -x;kill $(cat redis.pid)' 1 2 3 15 EXIT QUIT

/usr/sbin/redis-server redis.conf &
rc=$?
pid=$!
echo $pid > redis.pid
[ $rc = 0 ] || exit $rc

# it fails to report bind errors on startup, so wait for some and then see if pid is up
sleep 2
if ! kill -0 $pid; then
	exit 1
fi

# now can really execute tests
phpunit .
# exit with phpunit exitcode
exit $?
