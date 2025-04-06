> [!CAUTION]
> The project is still in development. Use it on your own risk.

# Color palette

[Pixelied](https://pixelied.com/colors/palette-visualizer/f72585-b5179e-7209b7-560bad-480ca8-3a0ca3-3f37c9-4361ee-4895ef-4cc9f0)

# Tech stack

- plain HTML (with Jinja templates), regular CSS and JS for frontend
- the backend runs on Flask
- images are stored on the Backblaze B2 cloud provider
- SQLite is a database solution, but it easily replaceable

# Functional requirements

## Minimum requirements:

- [x] Registration and authorisation of users to see only their photos;
- [x] The main page that tells about the service (available to all users) and the photo album page (only for registered users);
- [x] Ability to upload photos;
- [x] Ability to create folders for grouping photos (you can also create folders in folders);
- [x] Uploaded photos can be stored in the cloud (e.g. s3).

## Additional tasks:

- [ ] Add the ability to share individual photos;
- [ ] Add the ability to share entire folders (several users have access and they all see all the photos in the folder);
- [ ] Send emails when a photo is uploaded to a shared folder;
- [ ] Add the ability to control who can delete photos and folders from a shared folder (by default, only the person who created and shared the folder).

# Run locally:

You need .env file in **app** folder in order to run the application.

```.env
SECRET_KEY="yoursecret" # secret for wtforms
SQLALCHEMY_DATABASE_URI="" # your database provider
B2_KEY_ID="" # API key id of a bucket
B2_KEY="" # API key
BUCKET_ID="" # id of a bucket
```

1. Clone the repository

```bash
git clone https://github.com/LostHopes/photo-album-practice.git photo-album
cd photo-album
```


2. Create and activate virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install uv and update python package manager

```bash
pip install --upgrade pip uv
```

4. Install dependencies and run the project

```bash
uv sync --all-groups
uv run src/wsgi.py
```

## With Docker

```bash
sudo docker built -t yourname .
sudo docker run yourname
```

# Testing an app

Configuration can be modified in **pyproject.toml** file

```bash
pytest
```

# Known issues

- [x] Remove particular photo by filename or id

# License

The project licensed under MIT. (See [LICENSE](LICENSE))

# Contribute

Any contribution is appreciated. Feel free to open an issue or PR

# References

1. [B2SDK Documentation](https://b2-sdk-python.readthedocs.io)
2. [Writing GitHub Workflows](https://docs.github.com/en/actions/writing-workflows)
3. [Pytest Documentation](https://docs.pytest.org)
4. [Docker Documentation](https://docs.docker.com)
5. [Uv Documentation](https://docs.astral.sh/uv/)
6. [Flask Documentation](https://flask.palletsprojects.com)