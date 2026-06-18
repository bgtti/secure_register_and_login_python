"""
Changes of collision of a thread reference by the way it is now designed:
8 charts = 2.8 trillion possibilities. Chances of collision with 1 million generated references is about 0.018%. That increases to 1.8% with 10 million and to 36% with 50 million. If your system generates 10'000 new threads per day, it would take 2.7 years to get 10 million threads, and 27 years to reach 100 million threads (where the problem of collision becomes very likely).

"""
# Python/Flask libraries
import secrets
import string

def generate_thread_reference(prefix="REF", length=8):
    """
    Generates a random public-facing reference string, used for example, for a message thread.

    Returns the generated reference which consists of:
    - a prefix (default: "REF")
    - a hyphen ("-")
    - a random sequence of uppercase letters and digits

    The random portion uses cryptographically secure randomness
    via Python's `secrets` module.

    ----------------------------------------------------------

    :param prefix (str): [optional] Prefix added before the random code.Default is "REF".
    :param length (int): [optional] Length of the random code section. Default is 8.

    ----------------------------------------------------------
    Example usage:

    ```python
    reference = generate_thread_reference()
    print(reference) # --> REF-A7X92Q98
    ```
    
    Custom prefix example:

    ```python
    reference = generate_thread_reference(prefix="MSG")
    print(reference) # --> MSG-T8P4RX45
    ```

    Custom length example:

    ```python
    reference = generate_thread_reference(length=10)
    print(reference) # --> REF-91KD7QX2LP
    ```
    """
    alphabet = string.ascii_uppercase + string.digits
    code = "".join(secrets.choice(alphabet) for _ in range(length))
    return f"{prefix}-{code}"