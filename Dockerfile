
FROM astrocrpublic.azurecr.io/astronomer/astro-runtime:13.5.1


# Copy requirements.txt into the image
COPY requirements.txt ./

# Install Python packages from requirements.txt

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
