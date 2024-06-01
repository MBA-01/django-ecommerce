# GlobItem

GlobItem is an innovative e-commerce platform dedicated to showcasing and selling unique cultural accessories and handcrafted products from around the world. The platform leverages Django, a high-level Python web framework, to provide a robust and scalable solution for both buyers and sellers. Our mission is to connect artisans with a global audience, promoting cultural heritage and supporting fair trade practices.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
GlobItem specializes in cultural products from different countries, providing a platform for artisans to reach a global market and for consumers to access unique, culturally significant items. We aim to preserve cultural heritage and provide a fair trade marketplace for artisans.

## Features
- **User Registration and Authentication**: Secure processes for users to register and log in.
- **Product Management**: Comprehensive catalog management for artisans to list their products.
- **Shopping Cart and Wishlist**: User-friendly interfaces for managing purchases and favorite items.
- **Order Placement and Management**: Seamless checkout process with multiple payment options.
- **Product Reviews and Ratings**: User-generated reviews to help buyers make informed decisions.
- **Blog and Content Management**: Integrated blog for sharing cultural stories and insights.
- **Web Scraping for Product Data**: Automated web scraping to aggregate product data from various sources.
- **Security and Privacy**: GDPR compliance, SSL/TLS encryption, and secure payment gateways.
- **Support for Artisans**: Fair trade practices, marketing tools, and training resources.

## Technology Stack
- **Backend**: Django (Python web framework)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript
- **Other Tools**: BeautifulSoup, Requests, Pandas, Celery, Redis, Gunicorn, Nginx

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Docker: Containerization platform
- Python: Programming language
- Virtualenv: Virtual environment tool for Python
- Git: Version control system

### Step-by-Step Instructions

1. **Clone the Project Repository**
    ```bash
    git clone https://github.com/MBA-01/django-ecommerce.git
    cd django-ecommerce
    ```

2. **Set Up Virtual Environment**
    ```bash
    # Install virtualenv if not already installed
    pip install virtualenv

    # Create a virtual environment
    virtualenv venv

    # Activate the virtual environment
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Docker**
    Ensure Docker is installed and running on your system.

5. **Download Docker Images**
    Download the necessary Docker images by running:
    ```bash
    docker-compose pull
    ```

6. **Build and Run the Docker Containers**
    Build and start the Docker containers using Docker Compose:
    ```bash
    docker-compose up --build
    ```

    This command will build the Docker image for the Django application and start the containers for both the web application and the PostgreSQL database.

7. **Access the Application**
    Once the containers are running, you can access the GlobItem website by navigating to `http://localhost:8000` in your web browser.

## Usage
- **Admin Panel**: Access the admin panel at `http://localhost:8000/admin` to manage products, users, orders, and more.
- **User Registration**: Users can register and log in to manage their profiles, browse products, add items to the cart, and place orders.
- **Product Management**: Artisans can list and manage their products with detailed descriptions, images, and cultural stories.

## Testing
### Manual Testing
All testing during the development phase was performed manually to ensure the basic functionality of the application. This included:
- Functional Testing: Verifying that each feature works according to the requirements.
- Integration Testing: Ensuring that different components interact correctly.
- User Acceptance Testing: Validating that the application meets the needs of end users.

### Future Improvements
To enhance the reliability and maintainability of the application, the following automated testing strategies should be considered:
1. **Unit Testing**: Using Django's testing framework and Pytest to ensure individual components work as expected.
2. **Integration Testing**: Using Django's testing framework and Pytest to verify interactions between components.
3. **End-to-End Testing**: Using Selenium to simulate user behavior and validate application flows.
4. **Performance Testing**: Implementing automated performance tests to ensure the application can handle expected loads.
5. **Coverage Analysis**: Using Coverage.py to measure and improve test coverage.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the terms of the [Custom License](LICENSE).

## Contact
- **Author:** Mohamed El Bachrioui
- **Email:** Medelbachriouijr@gmail.com

Thank you for using GlobItem!
