# 1. Use official Python base image
FROM python:3.11-slim

# 2. Set work directory
WORKDIR /app

# 3. Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your project
COPY . .

# 5. Set environment variables
ENV PYTHONUNBUFFERED=1

# 6. Expose FastAPI port
EXPOSE 8000

# 7. Command to run FastAPI (not agent)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
