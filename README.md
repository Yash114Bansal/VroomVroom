# Vroom Vroom - Car Sharing App

Vroom Vroom is a car-sharing application designed specifically for AKGEC College, providing a convenient way for students and faculty to share rides within the campus and nearby areas. With features like real-time location sharing, push notifications, and secure authentication, Vroom Vroom aims to streamline the process of carpooling and enhance the commuting experience for everyone at AKGEC.

## Key Features

- **Authentication using JWT**: Secure user authentication ensures that only authorized individuals can access the app.
- **Push Notifications via FCM**: Instant notifications keep users informed about ride updates, bookings, and cancellations.
- **Real-Time Location Sharing**: Users can share their real-time location with others, facilitating easy meetup points and efficient coordination.
- **Chat Functionality with Websockets**: Integrated chat feature enables seamless communication between drivers and passengers.
- **Cash Payment Recording**: Recording of cash payments for rides, providing transparency and accountability.
- **Real-Time Drive Matching**: Utilizing PostGIS for efficient drive matching based on location proximity and timing.
- **Document Verification**: Users can complete the document verification process by submitting required identification documents, ensuring the safety and security of all participants.

## Screenshots

![Screenshot](docs/screens.png)

## Installation

To run Vroom Vroom locally, follow these steps:

1. Clone the repository: `git clone https://github.com/Yash114Bansal/VroomVroom/`
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the project root directory with the following content:

- `SECRET_KEY`: Django secret key for security.
- `DEBUG`: Boolean flag indicating whether debug mode is enabled (`True` or `False`).
- `CLOUDINARY_URL`: URL for Cloudinary integration.
- `CLOUD_NAME`: Cloudinary cloud name.
- `API_KEY`: Cloudinary API key.
- `API_SECRET`: Cloudinary API secret.
- `EMAIL_HOST_USER`: Email host username for sending emails.
- `EMAIL_HOST_PASSWORD`: Email host password.
- `OTP_API_KEY`: API key for OTP verification (2Factor.in).
- `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY`: Google OAuth2 client ID for social authentication.
- `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET`: Google OAuth2 client secret.
- `FCM_API_KEY`: API key for Firebase Cloud Messaging (FCM) for push notifications.


4. Set up the database: `python manage.py migrate`
5. Run the development server: `python manage.py runserver`

Make sure to configure your environment variables, database settings, and other configurations as needed.

## Usage

1. Register an account or log in using your credentials.
2. Complete the document verification process by submitting required identification documents.
3. Explore available rides or create your own ride if you're a driver.
4. Book rides that match your preferences and requirements.
5. Communicate with other users via chat to coordinate pickup and drop-off points.
6. Enjoy a comfortable and cost-effective ride-sharing experience within AKGEC College.

Document verification ensures the safety and security of all users by validating their identities and confirming eligibility to participate in the car-sharing community.

## Docker Installation

To run Vroom Vroom using Docker, follow these steps:

1. Ensure Docker and Docker Compose are installed on your system.
2. Clone the repository: `git clone https://github.com/Yash114Bansal/VroomVroom/`
3. Navigate to the project directory: `cd vroom_vroom`
4. Create a `.env` file in the project root directory with the content mentioned above.
5. Build and start the containers: `docker-compose up --build`

## Contributing

Contributions to Vroom Vroom are welcome! If you encounter any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
