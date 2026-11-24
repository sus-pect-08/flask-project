
from playwright.sync_api import Page, expect


BASE_URL = "http://127.0.0.1:5000"


def test_example(page: Page) -> None:

    # 1. log-in
    page.goto(f"{BASE_URL}/auth/login")

    expect(page).to_have_url(f"{BASE_URL}/auth/login")
    expect(page.get_by_role("heading", name="Login")).to_be_visible()

    email = page.get_by_role("textbox", name="Your Email")
    password = page.get_by_role("textbox", name="Your Password")

    expect(email).to_be_visible()
    expect(password).to_be_visible()

    email.fill("admin@example.com")
    password.fill("test2026")

    page.get_by_role("checkbox", name="Remember me").check()
    page.get_by_role("button", name="Submit").click()

    expect(page.get_by_role("link", name="Logout")).to_be_visible()

    # 2. visualizzazione conferenza esistente
    conference = page.get_by_role("link", name=":35 Conference ABC")
    expect(conference).to_be_visible()
    conference.click()

    # 3. ritorno al calendario
    back_calendar = page.get_by_role(
        "link", name="Back to Calendar", exact=True
    )

    expect(back_calendar).to_be_visible()
    back_calendar.click()

    # 4. creazione attività
    create_button = page.locator(
        "div:nth-child(7) > div:nth-child(4) > .d-flex > .btn"
    )

    expect(create_button).to_be_visible()
    create_button.click()

    activity_name = page.get_by_role("textbox", name="Activity Name")
    start_time = page.get_by_role("textbox", name="Start Time")
    end_time = page.get_by_role("textbox", name="End Time")
    description = page.get_by_role(
        "textbox", name="Meeting Details / Description"
    )

    expect(activity_name).to_be_visible()
    expect(start_time).to_be_visible()
    expect(end_time).to_be_visible()
    expect(description).to_be_visible()

    activity_name.fill("Activity")
    start_time.fill("15:02")
    end_time.fill("16:03")
    description.fill("123")

    page.get_by_label("Select Room").select_option("1")
    page.get_by_label("Participants").select_option(["1", "4"])

    page.get_by_role("button", name="Create Activity").click()

    # 5. verifica creazine
    created_activity = page.get_by_role("link", name=":02 Activity")

    expect(created_activity).to_be_visible()
    created_activity.click()

    expect(page.get_by_role("heading", name="Activity")).to_be_visible()

    # 6. modifica attività creata
    edit_button = page.get_by_role("link", name="Edit Activity")

    expect(edit_button).to_be_visible()
    edit_button.click()

    activity_name = page.get_by_role("textbox", name="Activity Name")

    expect(activity_name).to_be_visible()
    activity_name.fill("Activity2")

    page.get_by_role("button", name="Save Changes").click()

    expect(
        page.get_by_role("heading", name="Activity2")
    ).to_be_visible()

    # 7. eliminare attività create
    page.once("dialog", lambda dialog: dialog.accept())

    delete_button = page.get_by_role("button", name="Delete Activity")

    expect(delete_button).to_be_visible()
    delete_button.click()

    expect(
        page.get_by_role("heading", name="Activity2")
    ).not_to_be_visible()

    # 8. logout
    logout_button = page.get_by_role("link", name="Logout")

    expect(logout_button).to_be_visible()
    logout_button.click()

    # verifica ritorno alla pagina di log-in
    expect(
        page.get_by_role("textbox", name="Your Email")
    ).to_be_visible()

    # 9. ritorna alla home
    home_button = page.get_by_role("link", name="Home")

    expect(home_button).to_be_visible()
    current_url = page.url
    home_button.click()

    #verifica fallimento
    expect(page).to_have_url(current_url)