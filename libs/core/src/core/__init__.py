"""Core domain logic for the URL shortener."""

from .base62 import ALPHABET, BASE, decode_base62, encode_base62

__all__ = ["ALPHABET", "BASE", "decode_base62", "encode_base62"]
