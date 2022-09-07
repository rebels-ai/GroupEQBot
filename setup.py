from setuptools import setup

setup(
    name='group_eq_bot',
    version='1.0.0',
    packages=['group_eq_bot', 'group_eq_bot.data', 'group_eq_bot.models', 'group_eq_bot.telegram_event_router', 'group_eq_bot.telegram_event_handlers',
              'group_eq_bot.storage', 'group_eq_bot.storage.users_driven_database', 'group_eq_bot.storage.events_driven_database',
              'group_eq_bot.storage.schemas', 'group_eq_bot.telegram_event_processors', 'group_eq_bot.telegram_event_processors.public',
              'group_eq_bot.telegram_event_processors.private', 'group_eq_bot.internal_logger'],
    python_requires='>=3.7, <4',
    package_dir={'': 'source'},
    entry_points={
        'runners': [
            'main = group_eq_bot.run_bot:main',
        ]
    },
    url='https://github.com/rebels-ai/whois_coffee_bot_internal',
    license='MIT',
    author='rebels.ai',
    author_email='maksim.kumundzhiev@rebels.ai',
    description='Python interface (telegram bot) for telegram groups, which solves substantial chatting-related problems, making the communication more ethical, secured, targeted and in general, wholesome ! '
)
