#!/bin/bash

SRC_DIR_NAME=plutus
APP_NAME=plutus
DEST_DIR=/opt/webeye/ituiniu/$APP_NAME/
SSH_USER=test
SSH_HOST=127.0.0.1
SSH_ALIAS=test


if [ $(basename "$PWD") == "deploy" ]; then
    cd ..
fi

if [ $(basename "$PWD") != $SRC_DIR_NAME ]; then
    echo "please run in project root or deploy folder"
    exit 1
fi


RESTART=y

echo "generate COMMIT_POINT file...."
git log -1 > COMMIT_POINT


echo "begin to rsync files...."
#rsync -avzh --delete --exclude-from=rsync-excludes.txt * $SSH_USER@$SSH_HOST:$DEST_DIR
rsync -avzh --delete --exclude-from=rsync-excludes.txt * $SSH_ALIAS:$DEST_DIR

rm COMMIT_POINT


if [ "$RESTART" == "y" ]; then
    echo "rsync done, begin to restart app...."
    #ssh $SSH_USER@$SSH_HOST "cd $DEST_DIR;pipenv run supervisorctl restart $APP_NAME:*"
    ssh $SSH_ALIAS "cd $DEST_DIR;pipenv run supervisorctl restart $APP_NAME:*;"
fi

echo "all done !!!"
