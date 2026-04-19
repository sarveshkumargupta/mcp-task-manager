FROM python:3.11-slim

# Install uv
RUN pip install uv

WORKDIR /app

# Copy pyproject.toml
COPY pyproject.toml .

# Create data directory
RUN mkdir -p data

# Install dependencies using uv
RUN uv pip install -e .

# Copy source code
COPY src/ src/

# Expose port
EXPOSE 9000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "src/server.py"]
