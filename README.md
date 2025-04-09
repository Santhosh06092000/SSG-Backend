# SSG-Backend

## Solution

I created a **POST API** that accepts **CSV** or **XLSX** files and returns a generated **XLSX** file using the **Pandas** library.

Implemented a `SecretSantaGenerator` class to handle assignment generation and validation logic.

I also created a `file_handler` utility to read the uploaded files.

The generator logic works by cloning the input DataFrame and shuffling it.
Then, it checks that:

- No one is assigned to themselves.
- If a previous year file is provided, the same person is not assigned again.

The generator makes up to **100 attempts** to create valid assignments. If it fails, it raises an error.

Finally, I stream the generated file as a downloadable **XLSX** response from the API.

---

## Installation and Run

1. **Clone or Download the Code**

   - Clone the repository or download the code from GitHub.

2. **Create Virtual Environment**
   - Run the following command to create a virtual environment:
     ```
     python -m venv .venv
     ```
   - Activate the Virtual Environment:
     ```
     source .venv/Scripts/activate
     ```
3. **Install Dependencies**

   - Install the necessary Python packages using:
     ```
     pip install -r requirements.txt
     ```

4. **Run the Application**

   - Start the FastAPI application with:
     ```
     uvicorn main:app --reload
     ```

5. **Verify with Swagger**
   - Check if the application runs smoothly by visiting the Swagger documentation at:
     [http://localhost:8000/docs#/](http://localhost:8000/docs#/)
