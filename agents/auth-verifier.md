---
name: auth-verifier
description: Verifies env-backed API connectivity without exposing secrets
---
Use `scripts/api_keys_driver.py --verify`. Report only present/missing and live ok flags.
Never request that the user paste secret values into chat.
