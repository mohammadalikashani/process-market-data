import os
from collections.abc import Generator
from typing import Any

from src.configs.base_config import BaseConfig


class Configuration:
    _config_class = BaseConfig

    @classmethod
    def _get_all_base_classes(cls, class_: type) -> set:
        base_class_set = set(class_.__bases__)
        all_base_class_set = {class_}
        all_base_class_set.update(base_class_set)
        for base in base_class_set:
            all_base_class_set.update(cls._get_all_base_classes(base))
        return all_base_class_set

    @classmethod
    def _get_all_annotated_fields(cls, class_: type) -> dict:
        all_base_classes = cls._get_all_base_classes(class_)
        all_inherited_fields = {}
        for base in all_base_classes:
            if hasattr(base, "__annotations__"):
                for key, value in base.__annotations__.items():
                    all_inherited_fields[key] = value

        return all_inherited_fields

    @classmethod
    def _walk_all_parent_dirs(cls, path: str) -> Generator:
        """
        Yield directories starting from the given directory up to the root
        """
        if not os.path.exists(path):
            raise OSError("Starting path not found")

        if os.path.isfile(path):
            path = os.path.dirname(path)

        last_dir = None
        current_dir = os.path.abspath(path)
        while last_dir != current_dir:
            yield current_dir
            parent_dir = os.path.abspath(os.path.join(current_dir, os.path.pardir))
            last_dir, current_dir = current_dir, parent_dir

    @classmethod
    def _find_dotenv(cls, filename: str, alternative_env_search_dir: str | None) -> str:
        from dotenv import find_dotenv

        file_path = ""
        try:
            file_path = find_dotenv(filename=filename)
        except Exception:
            print("Warning: First try to find .env file failed!")
        if len(file_path) == 0 and alternative_env_search_dir is not None:
            for dirname in cls._walk_all_parent_dirs(alternative_env_search_dir):
                check_path = os.path.join(dirname, filename)
                if os.path.isfile(check_path):
                    return check_path

        return file_path

    @classmethod
    def apply(
            cls,
            cls_type: type | None = None,
            is_test: bool = False,
            alternative_env_search_dir: str | None = None,
            silent: bool = False,
    ) -> None:
        cls._inject_config(alternative_env_search_dir, cls_type, is_test, silent)

    @classmethod
    def _inject_config(cls, alternative_env_search_dir, cls_type: type | None, is_test, silent):
        from dotenv import dotenv_values, load_dotenv

        if cls_type:
            cls._config_class = cls_type
        if alternative_env_search_dir is None and not silent:
            print(
                "Warning: alternative_env_search_dir is set to None. .env files can not be found when venv dir located"
                "\noutside of project main directory. you can use alternative_env_search_dir=__file__ to avoid it."
                "\n use silent = True to suppress this warning",
            )
        filename = ".env.test" if is_test else ".env"
        dotenv_values = dotenv_values(
            cls._find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir),
        )
        all_annotated_fields = cls._get_all_annotated_fields(cls._config_class)
        for env_attr in dotenv_values:
            if not hasattr(cls._config_class, env_attr):
                # set .env field to class to replace with env values in next loop
                setattr(cls._config_class, env_attr, None)
        load_dotenv(cls._find_dotenv(filename=filename, alternative_env_search_dir=alternative_env_search_dir))
        for attr_name in dir(cls._config_class):
            if attr_name.startswith("__") or callable(getattr(cls._config_class, attr_name)):
                continue

            from_env = os.getenv(attr_name)
            if not from_env:
                continue

            annotated_type = all_annotated_fields.get(attr_name)

            try:
                final_value = cls._set_value_for_class(cls._config_class, attr_name, from_env, annotated_type)
                setattr(cls._config_class, attr_name, final_value)

            except Exception as e:
                raise Exception(
                    f"Configuration field format Exception: "
                    f"For field {attr_name} got {from_env}  expected {annotated_type!s}.",
                ) from e

    @classmethod
    def config(cls) -> type[BaseConfig]:
        return cls._config_class

    @classmethod
    def _set_value_for_class(
            cls,
            class_: type,
            attr_name: str,
            env_value: str,
            annotated_field_class: type | None = None,
    ) -> Any:
        class_value = getattr(class_, attr_name)
        if annotated_field_class:
            if type(annotated_field_class).__name__ != "_GenericAlias" and issubclass(annotated_field_class, str):
                return env_value
            return eval(env_value)
        if class_value:
            return env_value if isinstance(class_value, str) else eval(env_value)
        return env_value
