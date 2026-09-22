"""Superset config for agent audit log dashboard"""

# Enable CSV upload
ENABLE_PROXY_FIX = True
ALLOW_FILE_UPLOAD = True

# CSV upload settings (for audit logs)
ALLOWED_EXTENSIONS = {'csv', 'json', 'xlsx', 'xls'}
CSV_UPLOAD_CHUNK_SIZE = 10 * 1024 * 1024  # 10MB

# Allow localhost
CORS_ORIGINS = ['*']
