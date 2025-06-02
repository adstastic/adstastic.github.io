---
layout: post
title: "TIL: Downloading a postgres DB"
tags: til databases dev
---

I'm working on a website built with [NextJS](https://nextjs.org/), deployed on [Vercel](https://vercel.com), and using [Payload](https://payloadcms.com/) as the CMS. The schemas are defined in TypeScript and Payload automatically applies changes[^danger] so I want a copy of the DB in case I need to restore it.

[pg_dump](https://www.postgresql.org/docs/current/app-pgdump.html) is the tool for this job - all it needs is a connection string.

```
$ pg_dump $POSTGRES_URL
pg_dump: error: server version: 15.10; pg_dump version: 14.15 (Homebrew)
pg_dump: error: aborting because of server version mismatch
```

So I tried
```
$ brew upgrade pg_dump   
==> Downloading https://formulae.brew.sh/api/formula.jws.json
==> Downloading https://formulae.brew.sh/api/cask.jws.json
Error: No available formula with the name "pg_dump". Did you mean pgpdump, pedump or bgpdump?
```

Right, it comes as part of `postgresql`
```
$ brew upgrade postgresql
Warning: Formula postgresql was renamed to postgresql@14.
Warning: postgresql@14 14.15 already installed
```

It seems to default to `postgresql@14`, so I brew installed `postgresql@15`. Let's see if that worked

```
$ pg_dump -V
pg_dump (PostgreSQL) 14.15 (Homebrew)
```

We need to replace the reference to 14 with 15.
```
$ brew unlink postgresql@14
Unlinking /opt/homebrew/Cellar/postgresql@14/14.15... 2165 symlinks removed.

$ brew link postgresql@15
Linking /opt/homebrew/Cellar/postgresql@15/15.10... 1600 symlinks created.

$ pg_dump -V
pg_dump (PostgreSQL) 15.10 (Homebrew)
```
Success!

And finally...
```
pg_dump $POSTGRES_URL > db.sql
```

Now I separately need to back up the media, as that's stored in [Vercel Blob](https://vercel.com/docs/storage/vercel-blob).

[^danger]: Including destructive changes that will wipe your data! The price to pay for serverless, I guess.