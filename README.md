# digests

The `digests` service serves content displayed at https://elifesciences.org/digests

While an article [may contain a digest](https://elifesciences.org/articles/59007#digest), a digest is also 
[a separate thing](https://elifesciences.org/digests/59007/a-long-history-of-lichen-mimicry) with a friendlier title, 
a cover image and its own production workflow managed by the Features team and coordinated using the elife-bot.

The workflow to get content in to the `digests` service is roughly:

1. Features team creates a zip file containing a digest `.docx` file and a digest image and they place the zip file into an S3 bucket.
2. `elife-bot` runs an [IngestDigest workflow](https://github.com/elifesciences/elife-bot/blob/develop/workflow/workflow_IngestDigest.py) that:
    * produces a simplifed `.docx` file and emails it to the Features team for production
    * copies the *digest image* to an output bucket
    * copies the *`.docx`* to an output bucket
    * transforms the `.docx` to JATS XML that is posted to the Typesetter's API endpoint
3. a VoR article zip file is eventually ingested that contains the final digest and the elife-bot will include the `IngestDigestToEndpoint` activity that:
    * will POST digest JSON content to the `digest` service endpoint as 'unpublished'
    * fetch the digest image via the IIIF server in order to include the image dimensions into the digest JSON
4. when that article is published the `elife-bot` workflow executes a `PublishDigest` activity that issues a POST to the `digests` service, setting the digest to 'published'

In case the digest was edited in the typesetter's interface between steps 2 and 3, it will use the content of the digest from the JATS XML of the article itself and not the original digest `.docx` file.

## Install a new dev package

For consistency of environment, use the `venv` container:

```
docker-compose run venv pipenv install --dev uwsgi-tools
docker-compose run venv pipenv lock
```

## Run a test

```
docker-compose build
docker-compose run wsgi venv/bin/pytest app/digests/tests/test_digest_api.py
```

Images currently have to be re-built for modifications to any part of the code to be noticed.

## Copyright & Licence

The `digests` project is [MIT licenced](LICENCE.txt).
