#!/bin/bash

SRC_DIR_NAME=test
APP_NAME=test
DEST_DIR=/opt/webeye/ituiniu/$APP_NAME/
SSH_USER=test
SSH_HOST=test


if [ $(basename "$PWD") == "deploy" ]; then
    cd ..
fi

if [ $(basename "$PWD") != $SRC_DIR_NAME ]; then
    echo "please run in project root or deploy folder"
    exit 1
fi

echo "generate COMMIT_POINT file...."
git log -1 > COMMIT_POINT


echo "begin to rsync files...."
for host in $SSH_HOST; do
    echo "sync $host"
    rsync -avzh --delete --exclude-from=rsync-excludes.txt * $SSH_USER@$host:$DEST_DIR
done

rm COMMIT_POINT

RESTART=y

if [ "$RESTART" == "y" ]; then
    echo "rsync done, begin to restart app...."
    for host in $SSH_HOST; do
        echo "restart $host"
        ssh $SSH_USER@$host "cd $DEST_DIR;pipenv run supervisorctl restart $APP_NAME:\*"
    done
fi

echo "all done !!!"
