import hashlib
import os
from Crypto.Util import number

class SecureAuth:
    def __init__(self):
        self.participants = {}  # Stores participants' public keys
        self.prime_group = None  # The prime number defining the cryptographic group
        self.base_element = None  # A generator of the group
        self.challenges = {}  # Store challenges to prevent replay attacks

    def initialize_system(self):
        """
        Initialize the system by generating a prime group and a base element.
        """
        self.prime_group = number.getPrime(512)  # Generating a 512-bit prime number for the group
        self.base_element = os.urandom(1)[0] % (self.prime_group - 2) + 2  # Ensuring base_element is within group bounds
        print(f"System Initialized:\nPrime Group = {self.prime_group}\nBase Element = {self.base_element}")

    def enroll(self, identifier, secret):
        """
        Enroll a new participant by calculating and storing their public key.
        """
        if not self.prime_group or not self.base_element:
            print("Error: System not initialized.")
            return

        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
        public_key = pow(self.base_element, int(hashed_secret, 16), self.prime_group)
        self.participants[identifier] = public_key
        print(f"Participant '{identifier}' enrolled with public key: {public_key}")

    def generate_challenge(self, identifier):
        """
        Generate a random challenge for a participant.
        """
        if identifier not in self.participants:
            print("Participant not enrolled.")
            return None

        challenge = number.getPrime(128)
        self.challenges[identifier] = challenge
        print(f"Generated challenge for '{identifier}': {challenge}")
        return challenge

    def verify(self, identifier, secret, challenge, response_c, response_z):
        """
        Verify a participant's identity using a challenge-response model.
        """
        if identifier not in self.participants:
            print("Participant not enrolled.")
            return False

        if identifier not in self.challenges or self.challenges[identifier] != challenge:
            print("Invalid or expired challenge.")
            return False

        del self.challenges[identifier]  # Prevent replay attacks

        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
        y = self.participants[identifier]
        g = self.base_element
        p = self.prime_group

        # Compute T'
        T_prime = (pow(y, response_c, p) * pow(g, response_z, p)) % p
        computed_c = int(hashlib.sha256((str(y) + str(T_prime) + str(challenge)).encode()).hexdigest(), 16)

        if computed_c == response_c:
            print(f"Verification successful for participant '{identifier}'.")
            return True
        else:
            print(f"Verification failed for participant '{identifier}'.")
            return False

    def client_compute_response(self, identifier, secret, challenge):
        """
        Compute the response values (c, z) on the client side.
        """
        if identifier not in self.participants:
            print("Participant not enrolled.")
            return None, None

        hashed_secret = hashlib.sha256(secret.encode()).hexdigest()
        x = int(hashed_secret, 16)
        y = self.participants[identifier]
        g = self.base_element
        p = self.prime_group

        # Random number r
        r = int.from_bytes(os.urandom(16), 'big') % (p - 1)
        T = pow(g, r, p)
        c = int(hashlib.sha256((str(y) + str(T) + str(challenge)).encode()).hexdigest(), 16)
        z = (r - c * x) % (p - 1)

        print(f"Computed response for '{identifier}': c = {c}, z = {z}")
        return c, z

# Example usage
secure_auth = SecureAuth()
secure_auth.initialize_system()
secure_auth.enroll("Alex", "TossACoinToYourWitcher")

# Simulate client-side computation of response
challenge = secure_auth.generate_challenge("Alex")
c, z = secure_auth.client_compute_response("Alex", "TossACoinToYourWitcher", challenge)
secure_auth.verify("Alex", "TossACoinToYourWitcher", challenge, c, z)

# Incorrect password verification
challenge = secure_auth.generate_challenge("Alex")
c, z = secure_auth.client_compute_response("Alex", "wrongpassword", challenge)
secure_auth.verify("Alex", "wrongpassword", challenge, c, z)

secure_auth.enroll("Will", "Hello")

# Simulate client-side computation of response
challenge = secure_auth.generate_challenge("Will")
c, z = secure_auth.client_compute_response("Will", "Hello", challenge)
secure_auth.verify("Will", "Hello", challenge, c, z)

# Incorrect password verification
challenge = secure_auth.generate_challenge("Will")
c, z = secure_auth.client_compute_response("Will", "wrongpassword", challenge)
secure_auth.verify("Will", "wrongpassword", challenge, c, z)
