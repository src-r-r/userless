import os

# Define common directory paths

HOME = os.path.expanduser('~')
REFRACTION_DIR = os.path.join(HOME, '.config', 'refraction')
USERLESS_DIR = os.path.join(REFRACTION_DIR, 'userless')
SYS_USERLESS_DIR = os.path.join('/etc', 'userless')
EMAIL_DIR = os.path.join(USERLESS_DIR, 'email')

HTML_EMAIL_DIR = os.path.join(EMAIL_DIR, 'html')
TEXT_EMAIL_DIR = os.path.join(EMAIL_DIR, 'text')

TEXT_EMAIL_USER_VERIFY = os.path.join(TEXT_EMAIL_DIR, 'user_verify.html')
TEXT_EMAIL_PASSWORD_RESET = os.path.join(TEXT_EMAIL_DIR, 'password_reset.html')

HTML_EMAIL_USER_VERIFY = os.path.join(HTML_EMAIL_DIR, 'user_verify.html')
HTML_EMAIL_PASSWORD_RESET = os.path.join(HTML_EMAIL_DIR, 'password_reset.html')

MAIN_CONFIG = os.path.join(USERLESS_DIR, 'main.cfg')
if not os.path.exists(MAIN_CONFIG):
    MAIN_CONFIG = os.path.join(SYS_USERLESS_DIR, 'main.cfg')

_REQUIRED_DIRS = (
    REFRACTION_DIR,
    USERLESS_DIR,
    EMAIL_DIR,
    HTML_EMAIL_DIR,
    TEXT_EMAIL_DIR,
)

_REQUIRED_FILES = (
    TEXT_EMAIL_USER_VERIFY,
    TEXT_EMAIL_PASSWORD_RESET,
    MAIN_CONFIG,
)

_SUGGESTED_FILES = (
    HTML_EMAIL_USER_VERIFY,
    HTML_EMAIL_PASSWORD_RESET,
)
