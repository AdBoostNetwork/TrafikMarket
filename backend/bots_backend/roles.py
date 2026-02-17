import json
from pathlib import Path
from functools import lru_cache

# roles.py лежит в .../backend/bots_backend/roles.py
# корень проекта = parents[2]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ADMINS_PATH = PROJECT_ROOT / "data" / "admins.json"
TMP_PATH = PROJECT_ROOT / "data" / "admins.json.tmp"


@lru_cache(maxsize=1)
def _load_roles() -> dict:
    """
    Читает и валидирует data/admins.json.

    Формат:
    {
      "CEO": [int, ...],
      "admins": {
        "<admin_id>": {"adm_name": "<русский текст>"}
      }
    }
    """
    with ADMINS_PATH.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("admins.json must be a JSON object")

    ceo = data.get("CEO")
    admins = data.get("admins")

    if not isinstance(ceo, list) or not all(isinstance(x, int) for x in ceo):
        raise ValueError('"CEO" must be list[int]')

    if not isinstance(admins, dict):
        raise ValueError('"admins" must be an object: { "<id>": {"adm_name": "..."} }')

    norm_admins: dict[str, dict] = {}
    for k, v in admins.items():
        if not isinstance(k, str) or not k.isdigit():
            raise ValueError('admin ids must be digit-strings, e.g. "123456789"')
        if not isinstance(v, dict):
            raise ValueError('each admin must be an object: {"adm_name": "..."}')

        adm_name = v.get("adm_name")
        if not isinstance(adm_name, str) or not adm_name.strip():
            raise ValueError('admin "adm_name" must be a non-empty string')

        norm_admins[k] = {"adm_name": adm_name.strip()}

    return {"CEO": ceo, "admins": norm_admins}


def _reload_roles_cache() -> None:
    """Сбрасывает lru_cache, чтобы следующее чтение взяло свежий файл."""
    _load_roles.cache_clear()


def _write_roles(data: dict) -> None:
    """Атомарная запись admins.json через временный файл."""
    ADMINS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with TMP_PATH.open("w", encoding="utf-8-sig") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    TMP_PATH.replace(ADMINS_PATH)


def is_ceo(user_id: int) -> bool:
    roles = _load_roles()
    return user_id in roles["CEO"]


def is_admin(user_id: int) -> bool:
    roles = _load_roles()
    return (user_id in roles["CEO"]) or (str(user_id) in roles["admins"])


def get_admin_name(user_id: int) -> str | None:
    roles = _load_roles()
    if user_id in roles["CEO"]:
        return "CEO"
    record = roles["admins"].get(str(user_id))
    return record["adm_name"] if record else None


def list_admins() -> dict[int, str]:
    roles = _load_roles()
    return {int(k): v["adm_name"] for k, v in roles["admins"].items()}


def add_admin(admin_id: int, adm_name: str) -> bool:
    """
    Добавляет админа по id.
    Возвращает False, если admin_id уже существует или является CEO.
    """
    roles = _load_roles()
    admin_key = str(admin_id)
    name = adm_name.strip()

    if admin_id in roles["CEO"]:
        return False
    if admin_key in roles["admins"]:
        return False

    new_admins = dict(roles["admins"])
    new_admins[admin_key] = {"adm_name": name}

    new_data = {"CEO": list(roles["CEO"]), "admins": new_admins}

    _write_roles(new_data)
    _reload_roles_cache()
    return True


def remove_admin(admin_id: int) -> bool:
    """
    Удаляет админа по id.
    Возвращает False, если admin_id не найден.
    """
    roles = _load_roles()
    admin_key = str(admin_id)

    if admin_key not in roles["admins"]:
        return False

    new_admins = dict(roles["admins"])
    del new_admins[admin_key]

    new_data = {"CEO": list(roles["CEO"]), "admins": new_admins}

    _write_roles(new_data)
    _reload_roles_cache()
    return True


def update_admin_name(admin_id: int, adm_name: str) -> bool:
    """
    Меняет adm_name админа по id.
    Возвращает False, если admin_id не найден.
    """
    roles = _load_roles()
    admin_key = str(admin_id)

    if admin_key not in roles["admins"]:
        return False

    new_admins = dict(roles["admins"])
    new_admins[admin_key] = {"adm_name": adm_name.strip()}

    new_data = {"CEO": list(roles["CEO"]), "admins": new_admins}

    _write_roles(new_data)
    _reload_roles_cache()
    return True
