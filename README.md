Placement Portal v2

Uses:
Flask for backend
Sqlite db
Vue for frontend/UI
Redis for caching
Redis+Celery for scheduling tasks, async work.

to run :
run backend, frontend, redis and celery(I used docker):

. for backend, enable virutalenv. Then go inside backend folder and run "flask --app app:create run"
. for frontend simple go in frontend folder then run "npm run dev"
. for celery and redis, use docker/ system specific instructions.
Thanks!
