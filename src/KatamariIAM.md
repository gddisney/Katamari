import hashlib
import logging
import uuid
from datetime import datetime, timedelta
from typing import Optional, List
import ssl  # For handling certificates (CBA)
import os

from KatamariDB import KatamariMVCC  # Import the KatamariMVCC system

logging.basicConfig(level=logging.INFO)


class User:
    def __init__(self, username: str, password_hash: Optional[str] = None, roles: List[str] = None, certificate: Optional[str] = None, is_service_account: bool = False):
        self.username = username
        self.password_hash = password_hash
        self.certificate = certificate
        self.roles = roles if roles else []
        self.is_service_account = is_service_account
        self.api_key = None  # API key support for service accounts
        self.created_at = datetime.utcnow()

class Role:
    def __init__(self, role_name: str, permissions: List[str] = None):
        self.role_name = role_name
        self.permissions = permissions if permissions else []
        self.created_at = datetime.utcnow()


class KatamariIAM:
    """Identity and Access Management (IAM) module using KatamariMVCC."""

    def __init__(self):
        self.katamari_mvcc = KatamariMVCC()  # Initialize the KatamariMVCC store
        self.token_expiry = timedelta(hours=1)  # Session token expiry duration
        self.api_key_expiry = timedelta(days=30)  # API key expiry duration for service accounts

    # Utility to hash passwords
    def hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    # Load and verify x.509 certificates for Certificate-Based Authentication (CBA)
    def load_certificate(self, certificate_path: str) -> Optional[str]:
        """Load an x.509 certificate from a file for CBA."""
        try:
            with open(certificate_path, 'r') as cert_file:
                return cert_file.read()
        except Exception as e:
            logging.error(f"Error loading certificate: {e}")
            return None

    def verify_certificate(self, cert_str: str, ca_cert_path: str) -> bool:
        """Verify a client certificate against a trusted CA certificate."""
        try:
            # Create an SSL context to load and verify certificates
            context = ssl.create_default_context(cafile=ca_cert_path)
            context.load_verify_locations(cafile=ca_cert_path)
            cert = ssl.PEM_cert_to_DER_cert(cert_str)
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = False
            context.load_cert_chain(certfile=cert_str)
            return True
        except ssl.SSLError as e:
            logging.error(f"Certificate verification failed: {e}")
            return False

    # Create a user account
    async def create_user(self, username: str, password: str, roles: List[str] = None):
        """Create a new user with password-based authentication."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            if self.katamari_mvcc.get(f"user:{username}", tx_id):
                raise ValueError("Username already exists")

            password_hash = self.hash_password(password)
            user = User(username, password_hash, roles)
            
            # Store user data
            self.katamari_mvcc.put(f"user:{username}", {
                "username": username,
                "password_hash": user.password_hash,
                "roles": user.roles,
                "created_at": user.created_at.isoformat()
            }, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"User {username} created successfully.")
        except Exception as e:
            logging.error(f"Error creating user {username}: {e}")
            self.katamari_mvcc.commit(tx_id)

    # Create a service account with API key
    async def create_service_account(self, account_name: str, roles: List[str] = None):
        """Create a new service account with an API key."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            if self.katamari_mvcc.get(f"service:{account_name}", tx_id):
                raise ValueError("Service account already exists")

            # Generate API key for the service account
            api_key = str(uuid.uuid4())
            service_account = User(account_name, roles=roles, is_service_account=True)
            service_account.api_key = api_key

            # Store service account data
            self.katamari_mvcc.put(f"service:{account_name}", {
                "account_name": account_name,
                "api_key": api_key,
                "roles": service_account.roles,
                "is_service_account": True,
                "created_at": service_account.created_at.isoformat(),
                "api_key_expiry": (datetime.utcnow() + self.api_key_expiry).isoformat()
            }, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"Service account {account_name} created with API key.")
            return api_key
        except Exception as e:
            logging.error(f"Error creating service account {account_name}: {e}")
            self.katamari_mvcc.commit(tx_id)
            return None

    # Authenticate user using password
    async def authenticate_user(self, username: str, password: str) -> str:
        """Authenticate a user with password-based authentication and return a session token."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            user_data = self.katamari_mvcc.get(f"user:{username}", tx_id)
            if not user_data:
                raise ValueError("User not found")

            if self.hash_password(password) != user_data["password_hash"]:
                raise ValueError("Invalid password")

            # Generate session token
            token = str(uuid.uuid4())
            expiry_time = datetime.utcnow() + self.token_expiry
            self.katamari_mvcc.put(f"session:{token}", {
                "username": username,
                "expires_at": expiry_time.isoformat()
            }, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"User {username} authenticated. Session token: {token}")
            return token
        except Exception as e:
            logging.error(f"Authentication failed for {username}: {e}")
            self.katamari_mvcc.commit(tx_id)
            return None

    # Authenticate user using certificate-based authentication (CBA)
    async def authenticate_user_with_certificate(self, username: str, certificate: str, ca_cert_path: str) -> str:
        """Authenticate a user with a certificate and return a session token."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            user_data = self.katamari_mvcc.get(f"user:{username}", tx_id)
            if not user_data or not user_data.get("certificate"):
                raise ValueError("User or certificate not found")

            if not self.verify_certificate(certificate, ca_cert_path):
                raise ValueError("Certificate verification failed")

            # Generate session token
            token = str(uuid.uuid4())
            expiry_time = datetime.utcnow() + self.token_expiry
            self.katamari_mvcc.put(f"session:{token}", {
                "username": username,
                "expires_at": expiry_time.isoformat()
            }, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"User {username} authenticated via CBA. Session token: {token}")
            return token
        except Exception as e:
            logging.error(f"Certificate-based authentication failed for {username}: {e}")
            self.katamari_mvcc.commit(tx_id)
            return None

    # Authenticate service account using API key
    async def authenticate_service_account(self, account_name: str, api_key: str) -> str:
        """Authenticate a service account using an API key and return a session token."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            account_data = self.katamari_mvcc.get(f"service:{account_name}", tx_id)
            if not account_data:
                raise ValueError("Service account not found")

            if api_key != account_data["api_key"]:
                raise ValueError("Invalid API key")

            # Check API key expiry
            expiry_time = datetime.fromisoformat(account_data["api_key_expiry"])
            if datetime.utcnow() > expiry_time:
                raise ValueError("API key has expired")

            # Generate session token
            token = str(uuid.uuid4())
            token_expiry = datetime.utcnow() + self.token_expiry
            self.katamari_mvcc.put(f"session:{token}", {
                "account_name": account_name,
                "expires_at": token_expiry.isoformat(),
                "is_service_account": True
            }, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"Service account {account_name} authenticated. Session token: {token}")
            return token
        except Exception as e:
            logging.error(f"Authentication failed for service account {account_name}: {e}")
            self.katamari_mvcc.commit(tx_id)
            return None

    # Validate session token for user or service account
    async def validate_token(self, token: str) -> bool:
        """Validate a session token for a user or service account."""
        tx_id = self.katamari_mvcc.begin_transaction()
        session_data = self.katamari_mvcc.get(f"session:{token}", tx_id)
        if not session_data:
            logging.error(f"Session token {token} not found.")
            return False

        expiry_time = datetime.fromisoformat(session_data["expires_at"])
        if datetime.utcnow() > expiry_time:
            logging.info(f"Session token {token} has expired.")
            return False

        logging.info(f"Session token {token} is valid.")
        return True

    # Create a role and assign permissions
    async def create_role(self, role_name: str, permissions: List[str] = None):
        """Create a new role with a set of permissions."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            if self.katamari_mvcc.get(f"role:{role_name}", tx_id):
                raise ValueError("Role already exists")

            role = Role(role_name, permissions)
            
            # Store role data
            self.katamari_mvcc.put(f"role:{role_name}", {
                "role_name": role.role_name,
                "permissions": role.permissions,
                "created_at": role.created_at.isoformat()
            }, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"Role {role_name} created successfully.")
        except Exception as e:
            logging.error(f"Error creating role {role_name}: {e}")
            self.katamari_mvcc.commit(tx_id)

    # Assign a role to a user
    async def assign_role_to_user(self, username: str, role_name: str):
        """Assign a role to a user."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            user_data = self.katamari_mvcc.get(f"user:{username}", tx_id)
            if not user_data:
                raise ValueError("User not found")

            role_data = self.katamari_mvcc.get(f"role:{role_name}", tx_id)
            if not role_data:
                raise ValueError("Role not found")

            roles = user_data.get("roles", [])
            if role_name not in roles:
                roles.append(role_name)
                user_data["roles"] = roles
                self.katamari_mvcc.put(f"user:{username}", user_data, tx_id)

            self.katamari_mvcc.commit(tx_id)
            logging.info(f"Role {role_name} assigned to user {username}.")
        except Exception as e:
            logging.error(f"Error assigning role {role_name} to user {username}: {e}")
            self.katamari_mvcc.commit(tx_id)

    # Revoke a session token
    async def revoke_token(self, token: str):
        """Revoke a session token."""
        tx_id = self.katamari_mvcc.begin_transaction()
        try:
            if self.katamari_mvcc.get(f"session:{token}", tx_id):
                self.katamari_mvcc.put(f"session:{token}", {"revoked": True}, tx_id)
                self.katamari_mvcc.commit(tx_id)
                logging.info(f"Session token {token} revoked.")
            else:
                logging.error(f"Token {token} not found.")
        except Exception as e:
            logging.error(f"Error revoking token {token}: {e}")
            self.katamari_mvcc.commit(tx_id)

