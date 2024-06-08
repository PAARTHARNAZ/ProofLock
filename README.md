# ProofLock

ProofLock is a Zero-Knowledge Proof (ZKP) based secure authentication system designed to demonstrate a Proof of Concept (PoC) for cryptographic authentication using techniques inspired by the NARWAL system. The primary objective of ProofLock is to ensure secure authentication without revealing any sensitive information, thus maintaining user privacy and preventing replay attacks.

## Basis of the Project

This project is based on the concepts presented in the NARWAL (Non-interactive and Authentication Randomized Warranted Authentication Layers) system, which focuses on secure, zero-knowledge proof-based authentication mechanisms. You can find more detailed information in the [NARWAL.pdf](NARWAL.pdf) document included in this repository.

## Features

- **Zero-Knowledge Proof Authentication**: Ensures that the server can authenticate users without seeing their actual passwords.
- **Challenge-Response Mechanism**: Prevents replay attacks by using unique challenges for each authentication attempt.
- **Secure Enrollment**: Allows users to enroll securely with their passwords hashed and stored as public keys.
- **Client-Side Response Computation**: Simulates the client-side computation for zero-knowledge proofs.

## Getting Started

### Prerequisites

- Python 3.x
- `pycryptodome` library for cryptographic functions

Install the required library using pip:

```bash
pip install pycryptodome
```

### Usage

1. **Clone the Repository**

```bash
git clone https://github.com/PAARTHARNAZ/ProofLock.git
cd ProofLock
```

2. **Initialize the System**

Initialize the system by generating a prime group and a base element.

```python
secure_auth = SecureAuth()
secure_auth.initialize_system()
```

3. **Enroll a Participant**

Enroll a new participant by providing an identifier and a secret (password).

```python
secure_auth.enroll("Alex", "TossACoinToYourWitcher")
```

4. **Generate a Challenge**

Generate a random challenge for the enrolled participant.

```python
challenge = secure_auth.generate_challenge("Alex")
```

5. **Client-Side Response Computation**

Compute the response values (c, z) on the client side using the challenge.

```python
c, z = secure_auth.client_compute_response("Alex", "TossACoinToYourWitcher", challenge)
```

6. **Verify the Participant**

Verify the participant's identity using the challenge and the computed response values.

```python
secure_auth.verify("Alex", "TossACoinToYourWitcher", challenge, c, z)
```

### Example

Here is a complete example of enrolling and verifying participants:

```python
# Initialize the system
secure_auth = SecureAuth()
secure_auth.initialize_system()

# Enroll participants
secure_auth.enroll("Alex", "TossACoinToYourWitcher")
secure_auth.enroll("Will", "Hello")

# Alex's verification
challenge = secure_auth.generate_challenge("Alex")
c, z = secure_auth.client_compute_response("Alex", "TossACoinToYourWitcher", challenge)
secure_auth.verify("Alex", "TossACoinToYourWitcher", challenge, c, z)

# Will's verification
challenge = secure_auth.generate_challenge("Will")
c, z = secure_auth.client_compute_response("Will", "Hello", challenge)
secure_auth.verify("Will", "Hello", challenge, c, z)

# Verification with incorrect password
challenge = secure_auth.generate_challenge("Alex")
c, z = secure_auth.client_compute_response("Alex", "wrongpassword", challenge)
secure_auth.verify("Alex", "wrongpassword", challenge, c, z)
```

## File Structure

- `prooflock.py`: Main implementation of the ProofLock system.
- `README.md`: Project documentation.
- `NARWAL.pdf`: Detailed research paper on the NARWAL system.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The NARWAL system for providing the foundational concepts and techniques for zero-knowledge proof-based authentication.
- The contributors to the `pycryptodome` library for cryptographic functions in Python.

## Authors

- **[PAARTHARNAZ](https://github.com/PAARTHARNAZ)**


Secure access, zero knowledge.

