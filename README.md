# Functional requirements

## Minimum requirements:

1. Registration and authorisation of users to see only their photos;
2. The main page that tells about the service (available to all users) and the photo album page (only for registered users);
3. Ability to upload photos;
4. Ability to create folders for grouping photos (you can also create folders in folders);
5. Uploaded photos can be stored in the cloud (e.g. s3).

## Additional tasks:

1. Add the ability to share individual photos;
2. Add the ability to share entire folders (several users have access and they all see all the photos in the folder);
3. Send emails when a photo is uploaded to a shared folder;
4. Add the ability to control who can delete photos and folders from a shared folder (by default, only the person who created and shared the folder).

# Run locally:

You need .env file in **app** folder in order to run the application.

```.env
SECRET_KEY="yoursecret" secret for wtforms
SQLALCHEMY_DATABASE_URI="" # your database provider
```

With Docker

```bash
sudo docker built -t yourname .
sudo docker run yourname
```