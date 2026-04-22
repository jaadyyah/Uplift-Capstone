kill -TERM $(cat /tmp/gunicorn.pid)

while kill -0 $(cat /tmp/gunicorn.pid) 2>/dev/null; do
    sleep 0.5
done

gunicorn -w 4 app:app -b 0.0.0.0:8000 --pid /tmp/gunicorn.pid --daemon