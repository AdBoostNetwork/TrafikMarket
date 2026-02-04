import json
from pathlib import Path
from functools import lru_cache

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
ADMINS_PATH = DATA_DIR / "admins.json"
TMP_PATH = DATA_DIR / "admins.json.tmp"


@lru_cache(maxsize=1)
def load_roles() -> dict[str, list[int]]:
    """
    Контракт файла data/admins.json:
    {
      "admins": [int, ...],
      "CEO": [int, ...]
    }
    """
    with ADMINS_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise ValueError("admins.json must be an object")

    admins = data.get("admins", [])
    ceo = data.get("CEO", [])

    if not isinstance(admins, list) or not all(isinstance(x, int) for x in admins):
        raise ValueError('"admins" must be list[int]')

    if not isinstance(ceo, list) or not all(isinstance(x, int) for x in ceo):
        raise ValueError('"CEO" must be list[int]')

    return {"admins": admins, "CEO": ceo}


def reload_roles_cache() -> None:
    """
    Гарантия: после вызова следующий load_roles() перечитает файл с диска.
    """
    load_roles.cache_clear()


def _write_roles(data: dict[str, list[int]]) -> None:
    """
    Атомарная запись: сначала во временный файл, затем replace().
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with TMP_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    TMP_PATH.replace(ADMINS_PATH)


def is_ceo(user_id: int) -> bool:
    roles = load_roles()
    return user_id in roles["CEO"]


def is_admin(user_id: int) -> bool:
    roles = load_roles()
    # CEO считается админом автоматически
    return (user_id in roles["admins"]) or (user_id in roles["CEO"])


def add_admin(admin_id: int) -> bool:
    """
    Добавляет админа по id.
    Меняет JSON и сбрасывает кеш.
    Возвращает False, если такой id уже есть в admins (или в CEO).
    """
    if not isinstance(admin_id, int):
        raise TypeError("admin_id must be int")

    current = load_roles()

    # не даём добавлять CEO повторно как админа (по смыслу он и так админ)
    if admin_id in current["CEO"] or admin_id in current["admins"]:
        return False

    # НЕ мутируем current (он может быть кешированным объектом!)
    new_admins = list(current["admins"])
    new_admins.append(admin_id)
    new_admins.sort()

    new_data = {"admins": new_admins, "CEO": list(current["CEO"])}

    _write_roles(new_data)
    reload_roles_cache()
    return True


def remove_admin(admin_id: int) -> bool:
    """
    Удаляет админа по id.
    Меняет JSON и сбрасывает кеш.
    Возвращает False, если id не найден в admins.
    """
    if not isinstance(admin_id, int):
        raise TypeError("admin_id must be int")

    current = load_roles()

    if admin_id not in current["admins"]:
        return False

    new_admins = [x for x in current["admins"] if x != admin_id]
    new_data = {"admins": new_admins, "CEO": list(current["CEO"])}

    _write_roles(new_data)
    reload_roles_cache()
    return True
