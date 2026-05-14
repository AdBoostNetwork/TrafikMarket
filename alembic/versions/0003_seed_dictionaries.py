"""003_seed_dictionaries

Revision ID: 0003_seed_dictionaries
Revises: 0002_create_dictionaries
Create Date: 2026-05-14 14:21:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "0003_seed_dictionaries"
down_revision: Union[str, Sequence[str], None] = "0002_create_dictionaries"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        INSERT INTO countries (country_name)
        VALUES
            ('Россия'),
            ('Узбекистан'),
            ('Казахстан'),
            ('Украина'),
            ('Беларусь'),
            ('Индия'),
            ('Китай')
        ON CONFLICT (country_name) DO NOTHING;
        """
    )

    op.execute(
        """
        INSERT INTO topics (topic_name)
        VALUES
            ('Telegram'),
            ('Бизнес и стартапы'),
            ('Блоги'),
            ('Букмекерство'),
            ('Видео и фильмы'),
            ('Даркнет'),
            ('Дизайн'),
            ('Для взрослых'),
            ('Другое'),
            ('Еда и кулинария'),
            ('Здоровье и Фитнес'),
            ('Игры'),
            ('Инстаграм'),
            ('Интерьер и строительство'),
            ('Искусство'),
            ('Картинки и фото'),
            ('Карьера'),
            ('Книги'),
            ('Криптовалюты'),
            ('Курсы и гайды'),
            ('Лингвистика'),
            ('Маркетинг, PR, реклама'),
            ('Медицина'),
            ('Мода и красота'),
            ('Музыка'),
            ('Новости и СМИ'),
            ('Образование'),
            ('Общество'),
            ('Познавательное'),
            ('Политика'),
            ('Право'),
            ('Природа'),
            ('Продажи'),
            ('Психология'),
            ('Путешествия'),
            ('Религия'),
            ('Рукоделие'),
            ('Семья и дети'),
            ('Софт и приложения'),
            ('Спорт'),
            ('Ставки и беттинг'),
            ('Технологии'),
            ('Транспорт'),
            ('Цитаты'),
            ('Шок-контент'),
            ('Эзотерика'),
            ('Экономика'),
            ('Эротика'),
            ('Юмор и развлечения')
        ON CONFLICT (topic_name) DO NOTHING;
        """
    )

    op.execute(
        """
        INSERT INTO platforms (platform_name)
        VALUES
            ('Telegram'),
            ('TikTok'),
            ('VK'),
            ('Like'),
            ('YouTube'),
            ('Instagram'),
            ('FaceBook'),
            ('X'),
            ('MAX')
        ON CONFLICT (platform_name) DO NOTHING;
        """
    )

    op.execute(
        """
        INSERT INTO traffic_types (traffic_type_name)
        VALUES
            ('Прямой пост'),
            ('Приветка'),
            ('ОП'),
            ('Мотивированный'),
            ('Спам'),
            ('Инвайтинг'),
            ('Таргет')
        ON CONFLICT (traffic_type_name) DO NOTHING;
        """
    )

    op.execute(
        """
        INSERT INTO audience_types (type_name)
        VALUES
            ('мца'),
            ('жца'),
            ('смешанная')
        ON CONFLICT (type_name) DO NOTHING;
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        DELETE FROM audience_types
        WHERE type_name IN ('мца', 'жца', 'смешанная');
        """
    )
    op.execute(
        """
        DELETE FROM traffic_types
        WHERE traffic_type_name IN (
            'Прямой пост',
            'Приветка',
            'ОП',
            'Мотивированный',
            'Спам',
            'Инвайтинг',
            'Таргет'
        );
        """
    )
    op.execute(
        """
        DELETE FROM platforms
        WHERE platform_name IN (
            'Telegram',
            'TikTok',
            'VK',
            'Like',
            'YouTube',
            'Instagram',
            'FaceBook',
            'X',
            'MAX'
        );
        """
    )
    op.execute(
        """
        DELETE FROM topics
        WHERE topic_name IN (
            'Telegram',
            'Бизнес и стартапы',
            'Блоги',
            'Букмекерство',
            'Видео и фильмы',
            'Даркнет',
            'Дизайн',
            'Для взрослых',
            'Другое',
            'Еда и кулинария',
            'Здоровье и Фитнес',
            'Игры',
            'Инстаграм',
            'Интерьер и строительство',
            'Искусство',
            'Картинки и фото',
            'Карьера',
            'Книги',
            'Криптовалюты',
            'Курсы и гайды',
            'Лингвистика',
            'Маркетинг, PR, реклама',
            'Медицина',
            'Мода и красота',
            'Музыка',
            'Новости и СМИ',
            'Образование',
            'Общество',
            'Познавательное',
            'Политика',
            'Право',
            'Природа',
            'Продажи',
            'Психология',
            'Путешествия',
            'Религия',
            'Рукоделие',
            'Семья и дети',
            'Софт и приложения',
            'Спорт',
            'Ставки и беттинг',
            'Технологии',
            'Транспорт',
            'Цитаты',
            'Шок-контент',
            'Эзотерика',
            'Экономика',
            'Эротика',
            'Юмор и развлечения'
        );
        """
    )
    op.execute(
        """
        DELETE FROM countries
        WHERE country_name IN (
            'Россия',
            'Узбекистан',
            'Казахстан',
            'Украина',
            'Беларусь',
            'Индия',
            'Китай'
        );
        """
    )
