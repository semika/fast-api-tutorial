FROM python:3

WORKDIR /app

COPY requirements.txt ./
COPY main.py ./

#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

## Start FastAPI with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD [ "fastapi", "dev", "./main.py"]