# Image Upload Project

This project is a Django application that allows users to upload images and generate thumbnails based on their account tiers. The application provides endpoints for image uploading, viewing images, and generating expiring links for images.

## Setup

### Docker:

1.  Install docker <https://docs.docker.com/get-docker/>
2.  Clone the repository and inside main folder run the following command:

```
docker run
```

### Without Docker

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/Felooo8/image-upload-project
   cd image_upload_project
   ```

2. Install Python3:

   https://www.python.org/downloads/

3. Install the project dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Create and apply database migrations:

   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Create a superuser for accessing the admin interface:

   ```
   python manage.py createsuperuser
   ```

   Follow the prompts to create a superuser.

6. Run the development server:

   ```
   python manage.py runserver
   ```

   The application will be accessible at `http://127.0.0.1:8000/`.

## Usage

1. Open the application in a web browser.

2. Create a user account and log in.

3. Upload an image using the "Upload Image" feature.

4. View your uploaded images and associated thumbnails by visiting the "My Images" section.

5. Access the admin interface by appending `/admin` to the application URL, and log in using the superuser credentials.

## Expiring Link Feature

The application supports generating expiring links for uploaded images. When uploading an image, users can specify the expiration time for the link (in seconds) using the `expiration` parameter.

To generate an expiring link for a specific image, use the `/api/images/<image_id>/expiring-link/` endpoint. The generated link will expire after the specified time (in body of POST request), providing temporary access to the image.

## API Endpoints

- `POST /api/upload/`: Endpoint for uploading an image. Supports image upload as a form data parameter named "image". Optionally, you can include an "expiration" parameter to create an expiring link to the image. The "expiration" parameter should be an integer representing the number of seconds after which the link will expire. Valid values for "expiration" are between 300 and 30000 seconds.

- `GET /api/images/`: Endpoint for listing user-uploaded images and associated thumbnails.

- `GET /api/images/<image_id>/expiring-link/`: Endpoint for generating an expiring link to a specific image.

## Tests

To run the tests for this project:

```
python manage.py test
```

This will execute all the tests and display the results.

## Admin Interface

Access the admin interface at `/admin` and log in with your superuser credentials. The admin interface allows you to manage users, images, thumbnails, and account tiers.

Feel free to explore the features and functionalities provided by the application!
