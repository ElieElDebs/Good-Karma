
# Configuration

This directory contains essential configuration files for the Morlana backend application.

## Files Overview

### `config.yml` (or `.env`)
- **Purpose**: Store environment variables and application settings
- **Example**:
```yaml
database_url: postgresql://user:password@localhost:5432/morlana
api_port: 3000
api_key: your_secret_key_here
```
- **Best Practice**: Never commit sensitive data. Use `.env.example` as a template.

### `.env.example`
- **Purpose**: Template file showing required environment variables
- **Usage**: Copy to `.env` and fill in your local values
- **Example**:
```
DATABASE_URL=
API_PORT=
API_KEY=
```

## Getting Started

1. **Copy the example file**:
```bash
cp .env.example .env
```

2. **Update values** for your local environment

3. **Add to `.gitignore`**:
```
.env
*.local
```

## Contributing

- Always provide `.example` files for configuration templates
- Document each variable's purpose and format
- Keep secrets out of version control
- Test configuration changes before committing
