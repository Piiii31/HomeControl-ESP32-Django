# HomeControl ESP32 with Django

This repository contains a Django application designed to receive infrared (IR) signals from ESP32 devices and store them in a PostgreSQL database. This application enables users to control their home devices remotely by capturing and managing IR signals efficiently.

## :dart: About ##

The **HomeControl ESP32-Django** project allows users to send IR signals from ESP32 devices to a Django backend. The backend processes these signals and stores them in a PostgreSQL database for future reference and control. This integration facilitates smart home functionalities by allowing users to interact with their home appliances remotely.

## :sparkles: Features ##

- **Receive IR Signals**: Capture IR signals sent from ESP32 devices.
- **Database Storage**: Store the captured signals in a PostgreSQL database for easy access and management.
- **Remote Control**: Control home appliances using the stored IR signals.
- **User-friendly Interface**: A simple web interface for managing and controlling IR signals.

## :rocket: Technologies ##

The following technologies were used to build this project:

- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [ESP32](https://www.espressif.com/en/products/hardware/esp32/overview)

## :white_check_mark: Requirements ##

To run this project, you'll need:

- [Python](https://www.python.org/) installed on your machine.
- [PostgreSQL](https://www.postgresql.org/) installed and configured.
- Basic knowledge of Django and RESTful APIs.

## :checkered_flag: Running the Project ##

1. Clone the repository to your local machine:

    ```bash
    $ git clone https://github.com/Piiii31/HomeControl-ESP32-Django.git
    ```

2. Navigate to the project directory:

    ```bash
    $ cd HomeControl-ESP32-Django
    ```

3. Install the dependencies:

    ```bash
    $ pip install -r requirements.txt
    ```

4. Create and configure your PostgreSQL database, and update the database settings in `settings.py`.

5. Apply migrations:

    ```bash
    $ python manage.py migrate
    ```

6. Run the Django server:

    ```bash
    $ python manage.py runserver
    ```

7. Access the application at `http://localhost:8000/` to start controlling your devices.

## :memo: License ##

This project is licensed under the MIT License. For more details, see the [LICENSE](LICENSE) file.

## :handshake: Contributions ##

Contributions are welcome! Feel free to open an issue or submit a pull request.

## :mailbox_with_mail: Contact ##

For any inquiries, feel free to reach out: [Piiii31](mailto:meddeb65@gmail.com)

---

<p align="center">
  Made with :heart: by <a href="https://github.com/Piiii31" target="_blank">Piiii31</a>
</p>
