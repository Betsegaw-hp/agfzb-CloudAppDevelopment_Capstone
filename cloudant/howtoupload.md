# CouchDB/Cloudant Bulk Data Import Guide

This document outlines the steps to import JSON data into CouchDB or IBM Cloudant using the `_bulk_docs` endpoint with IAM authentication.

## Prerequisites
- **CouchDB/Cloudant Database URL:** (e.g., `https://<account>.cloudant.com`)
- **IAM API Key:** For Cloudant authentication
- **Curl Installed:** Command-line tool for data transfer
- **jq Installed (Optional):** For JSON manipulation

---

## Steps to Import Data

### 1. Prepare the JSON Data
Ensure your JSON file (`dealerships.json`) follows this format:

```json
{
  "docs": [
    { "name": "Dealer 1", "location": "City A" },
    { "name": "Dealer 2", "location": "City B" }
  ]
}
```

🔎 **Note:** The data must be wrapped in a `"docs"` array.

### 2. Obtain the IAM Access Token

Run the following command to generate an access token:

```bash
IAM_API_KEY="your-iam-api-key"

IAM_TOKEN=$(curl -X POST "https://iam.cloud.ibm.com/identity/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "apikey=$IAM_API_KEY&grant_type=urn:ibm:params:oauth:grant-type:apikey" | jq -r '.access_token')
```

📌 **Tip:** Install `jq` using `sudo apt-get install jq` (Linux) or `brew install jq` (macOS).

### 3. Create the Database (If Needed)

Ensure the target database exists. Create it if it doesn't:

```bash
curl -X PUT "$COUCH_URL/dealerships" \
  -H "Authorization: Bearer $IAM_TOKEN"
```

### 4. Import the JSON Data

Use the `_bulk_docs` endpoint to import the data:

```bash
curl -X POST "$COUCH_URL/dealerships/_bulk_docs" \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "Content-Type: application/json" \
  -d @dealerships.json
```

### 5. Handling a Flat JSON Array (Optional)

If the JSON file is a flat array, wrap it in `"docs"`:

```bash
jq '{docs: .}' dealerships.json > dealerships_fixed.json
```

Then import:

```bash
curl -X POST "$COUCH_URL/dealerships/_bulk_docs" \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "Content-Type: application/json" \
  -d @dealerships_fixed.json
```

---

## Troubleshooting

- **Unauthorized Error:** Check IAM API Key and regenerate the token.
- **`docs` Error:** Ensure the JSON is wrapped in the `"docs"` array.
- **Database Not Found:** Create the database before importing.

---

## References
- [CouchDB Documentation](https://docs.couchdb.org/)
- [IBM Cloudant Documentation](https://cloud.ibm.com/docs/Cloudant)

---

**End of Guide**

