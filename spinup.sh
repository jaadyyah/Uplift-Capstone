if [ -f "/tmp/gunicorn.pid" ]; then
    PID=$(cat /tmp/gunicorn.pid)
    kill -TERM $PID
    while kill -0 $PID 2>/dev/null; do
        sleep 0.5
    done
    sleep 1
fi

gunicorn -w 4 app:app -b 0.0.0.0:8000 --pid /tmp/gunicorn.pid --daemon