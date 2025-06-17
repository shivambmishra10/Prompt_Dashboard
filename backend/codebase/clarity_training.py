# clarity_training.py
# Training examples for Clarity of Requirements

CLARITY_EXAMPLES = [
    {
        "vague": "Create a login system",
        "clarified": "Develop a user authentication system for a web application. Users should be able to register with an email and password, log in, and log out. Passwords must be securely hashed using bcrypt. The system should validate credentials, provide clear error messages for invalid attempts, and prevent duplicate registrations. Use Flask for the backend and SQLite for storage."
    },
    {
        "vague": "Build a todo app",
        "clarified": "Create a full-stack todo list application where users can add, edit, delete, and mark tasks as complete. The app should support user authentication, persistent storage using PostgreSQL, and a responsive React frontend. Include input validation and error handling for all user actions."
    },
    {
        "vague": "Fetch weather data",
        "clarified": "Write a Python script that retrieves current weather data for a given city using the OpenWeatherMap API. The script should accept a city name as input, handle API errors gracefully, and print the temperature, humidity, and weather description in a readable format."
    },
    {
        "vague": "Send email notifications",
        "clarified": "Implement a function in Node.js that sends email notifications to users when their account settings change. Use the nodemailer library with Gmail SMTP. The function should accept recipient email, subject, and message body as parameters, and handle errors such as invalid email addresses or failed sends."
    },
    {
        "vague": "Generate a report",
        "clarified": "Develop a script in Python that generates a PDF sales report from a CSV file. The report should include total sales, top-selling products, and a summary chart. Use pandas for data processing and ReportLab for PDF generation. Handle missing or malformed data gracefully."
    },
    {
        "vague": "Create a chatbot",
        "clarified": "Build a customer support chatbot using Python and the Rasa framework. The bot should answer FAQs, escalate complex queries to a human agent, and log all conversations to a database. Include intent recognition, entity extraction, and fallback handling for unrecognized inputs."
    },
    {
        "vague": "Image upload feature",
        "clarified": "Add an image upload feature to an existing Django web app. Users should be able to upload JPEG or PNG images up to 5MB. Store images in AWS S3 and save URLs in the database. Validate file type and size, and display error messages for invalid uploads."
    },
    {
        "vague": "Export data",
        "clarified": "Implement a feature in a React app that allows users to export their profile data as a downloadable CSV file. The export should include all user fields, handle special characters, and provide feedback if the export fails."
    },
    # Add more high-quality examples as needed
]
