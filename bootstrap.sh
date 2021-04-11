#!/bin/sh
export FLASK_APP=app
export FLASK_ENV=development

case $1 in 
    shell)
            flask shell
        ;;
    init)
            flask db init
        ;;
    migrate)
            flask db migrate
        ;;
    upgrade)
            flask db upgrade
        ;;
    database-seed)
            flask database-seed
        ;;
    sync-teams)
            flask sync-teams $2
        ;;
    sync-players)
            flask sync-players $2
        ;;
    sync-games)
            flask sync-games $2 $3 $4
        ;;
    sync-season)
            flask sync-season $2 $3 $4
        ;;
    sync-new-games)
            flask sync-new-games
        ;;
    *)
            flask run
        ;;
esac