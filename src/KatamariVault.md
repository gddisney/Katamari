# KatamariVault: Secure Credential Storage System

**KatamariVault** is a secure credential management system designed to store, retrieve, and manage sensitive credentials such as API keys, passwords, access tokens, and other secrets. It integrates seamlessly with **KatamariKMS** for encryption and key management, ensuring all credentials are stored securely using AES-256 encryption.

## Key Features

- **AES-256 Encryption**: All credentials stored in **KatamariVault** are encrypted with AES-256, ensuring maximum security.
- **Version Control**: Built on top of **KatamariMVCC**, every stored credential has full version control, making it possible to track changes, rollback, or retrieve previous versions.
- **Secure Retrieval**: Credentials can be securely retrieved using access policies and can be decrypted on the fly using the correct key version.
- **Integration with KatamariKMS**: **KatamariVault** works directly with **KatamariKMS** to ensure key management is tightly coupled with secure storage.
- **Role-Based Access Control (RBAC)**: Manage who has access to which credentials using roles defined in **KatamariIAM**.
  
## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Storing Credentials](#storing-credentials)
  - [Retrieving Credentials](#retrieving-credentials)
  - [Rotating Credentials](#rotating-credentials)
- [Version Control](#version-control)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Installation

Install **KatamariVault** as part of the **Katamari Ecosystem**. 

```bash
git clone https://github.com/gddisney/katamari.git
cd katamari
pip install -r requirements.txt
```

This will install all necessary dependencies, including **KatamariMVCC** and **KatamariKMS**.

## Configuration

**KatamariVault** requires minimal configuration to get started. Ensure the following YAML configuration is present:

```yaml
vault:
  key_store_path: ./vault_keys
  default_encryption_key: my_vault_key
```

The **KatamariVault** uses a combination of **KatamariKMS** for key management and **KatamariMVCC** for version control, ensuring both encryption and transactional integrity for your stored secrets.

## Usage

### Storing Credentials

Storing credentials is simple. Once the vault is initialized, credentials are encrypted using the AES-256 key stored in **KatamariKMS**.

```python
from KatamariVault import KatamariVault

vault = KatamariVault()
vault.store_secret("api_key", "super_secret_key_value")
```

This will encrypt and store the `api_key` in the vault.

### Retrieving Credentials

To retrieve a stored credential:

```python
retrieved_key = vault.get_secret("api_key")
print(retrieved_key)
```

The key will be decrypted automatically and returned for use.

### Rotating Credentials

Credential rotation is handled through the **KatamariVault** and **KatamariKMS** integration, allowing seamless encryption key rotation.

```python
vault.rotate_secret("api_key")
```

This will rotate the stored credential, encrypting it with a new versioned key from **KatamariKMS**.

## Version Control

With **KatamariMVCC**, every credential has version control, allowing you to:

- Retrieve older versions of a credential.
- Audit changes made to stored secrets.
- Rollback to previous versions if needed.

```python
old_version = vault.get_secret("api_key", version=1)
```

## Examples

### Storing and Rotating an API Key

```python
# Initialize the vault and store a credential
vault = KatamariVault()
vault.store_secret("api_key", "my_original_api_key")

# Rotate the credential for security
vault.rotate_secret("api_key")

# Retrieve the latest API key
latest_api_key = vault.get_secret("api_key")
print(latest_api_key)
```

### Storing and Retrieving Database Credentials

```python
vault.store_secret("db_password", "my_db_password")
db_password = vault.get_secret("db_password")
print(f"Database password: {db_password}")
```

## Contributing

We welcome contributions to **KatamariVault**! Follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License

**KatamariVault** is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

**KatamariVault** is an essential part of the **Katamari Ecosystem**, offering a robust, secure solution for managing credentials and secrets. It seamlessly integrates with **KatamariKMS**, **KatamariIAM**, and other components to provide a fully encrypted, version-controlled, and scalable approach to credential management in modern, distributed systems.
