FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY server.py .

# Install dependencies using uv
RUN uv pip install --system -e .

# Expose the port
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]
