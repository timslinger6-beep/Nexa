from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


class DataService:
    """
    Persistentes Profil-/Datensystem für Nexa.
    Daten werden getrennt vom Nexa-Quellcode als JSON gespeichert.
    """

    def __init__(self, root: str | Path | None = None):
        if root is None:
            root = Path(__file__).resolve().parent

        self.root = Path(root)
        self.data_root = self.root / "data"
        self.profiles_root = self.data_root / "profiles"

        self.profiles_root.mkdir(parents=True, exist_ok=True)

        self.profile_name: str | None = None
        self.data: dict[str, Any] = {}

    def _safe_name(self, name: str) -> str:
        name = str(name).strip()

        if not name:
            raise ValueError("Profilname darf nicht leer sein.")

        if not re.fullmatch(r"[A-Za-z0-9_.-]+", name):
            raise ValueError(
                "Profilname darf nur Buchstaben, Zahlen, _, - und . enthalten."
            )

        return name

    def _profile_path(self) -> Path:
        if self.profile_name is None:
            raise RuntimeError("Es wurde noch kein Profil geöffnet.")

        return self.profiles_root / f"{self.profile_name}.json"

    def open(self, profile: str) -> dict[str, Any]:
        self.profile_name = self._safe_name(profile)
        path = self._profile_path()

        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as file:
                    loaded = json.load(file)

                if not isinstance(loaded, dict):
                    raise ValueError("Profildatei enthält kein Objekt.")

                self.data = loaded

            except (json.JSONDecodeError, OSError, ValueError):
                self.data = {}

        else:
            self.data = {}

        return dict(self.data)

    def get(self, key: str, default: Any = None) -> Any:
        if self.profile_name is None:
            raise RuntimeError("Zuerst muss ein Profil mit data.open() geöffnet werden.")

        return self.data.get(str(key), default)

    def set(self, key: str, value: Any) -> None:
        if self.profile_name is None:
            raise RuntimeError("Zuerst muss ein Profil mit data.open() geöffnet werden.")

        self.data[str(key)] = value

    def delete(self, key: str) -> bool:
        if self.profile_name is None:
            raise RuntimeError("Zuerst muss ein Profil mit data.open() geöffnet werden.")

        key = str(key)

        if key in self.data:
            del self.data[key]
            return True

        return False

    def has(self, key: str) -> bool:
        if self.profile_name is None:
            raise RuntimeError("Zuerst muss ein Profil mit data.open() geöffnet werden.")

        return str(key) in self.data

    def all(self) -> dict[str, Any]:
        if self.profile_name is None:
            raise RuntimeError("Zuerst muss ein Profil mit data.open() geöffnet werden.")

        return dict(self.data)

    def save(self) -> None:
        path = self._profile_path()
        temporary = path.with_suffix(".tmp")

        with temporary.open("w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=2
            )

        temporary.replace(path)

    def reset(self) -> None:
        if self.profile_name is None:
            raise RuntimeError("Zuerst muss ein Profil geöffnet werden.")

        self.data = {}

    def exists(self, profile: str) -> bool:
        name = self._safe_name(profile)
        return (self.profiles_root / f"{name}.json").exists()

    def delete_profile(self, profile: str) -> bool:
        name = self._safe_name(profile)
        path = self.profiles_root / f"{name}.json"

        if not path.exists():
            return False

        path.unlink()

        if self.profile_name == name:
            self.profile_name = None
            self.data = {}

        return True

    def list_profiles(self) -> list[str]:
        return sorted(
            path.stem
            for path in self.profiles_root.glob("*.json")
            if path.is_file()
        )


data_service = DataService()
