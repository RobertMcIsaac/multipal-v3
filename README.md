## Setup
Next.js with supabase server-side auth
Supabase CLI (for dev) - postreSQL
FastApi (synchronous with plans to adjust to async in future)
SQLModel
Alembic

## Running the project

Web
``` bash
npm run dev
```

api (FastApi)
```bash
fastapi dev src/main.py
```


## Guides

Next.js:
https://nextjs.org/docs/app/getting-started/installation

Supabase server-side auth for Next.js:
https://supabase.com/docs/guides/auth/server-side/nextjs

FasApi project structure: 
https://supabase.com/docs/guides/auth/server-side/nextjs

Supbase connecting to DB:
https://supabase.com/docs/guides/database/connecting-to-postgres

Supabase CLI setup:
https://supabase.com/docs/reference/cli/introduction
https://supabase.com/docs/guides/local-development

FastApi concurrency and async / await:
https://fastapi.tiangolo.com/async/

FastApiand SQL DBs:
https://fastapi.tiangolo.com/tutorial/sql-databases/

Switching from sync to async with FastApi and SQLModel:
https://www.linkedin.com/pulse/moving-from-sync-async-fastapi-sqlmodelwhat-you-need-know-vertrees-eowtc/