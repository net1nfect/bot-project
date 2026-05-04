"""Selector CSS/XPath hasil pemetaan UI untuk simulasi pendaftaran dan pemutaran."""

SELECTORS = {
    "signup_button": 'button[data-testid="signup-button"]',
    "email_input": 'input[id="username"]',
    "password_input": 'input[id="new-password"]',
    "display_name_input": 'input[id="displayName"]',
    "day_input": 'input[id="day"]',
    "month_select": 'select[id="month"]',
    "year_input": 'input[id="year"]',
    "gender_male": 'label[for="gender-male"]',
    "gender_female": 'label[for="gender-female"]',
    "submit_button": 'button[type="submit"]',
    "login_button": 'button[data-testid="login-button"]',
    "play_button": 'button[aria-label="Play"]',
    "loop_button": 'button[aria-label*="loop"]',
    "cookie_accept": 'button[id="onetrust-accept-btn-handler"]',
}
