from __future__ import annotations

from datetime import date
import os

import streamlit as st

from frontend.api_client import ApiError, RunningTrackerApiClient

KM_PER_MILE = 1.60934

st.set_page_config(
    page_title='Running Tracker',
    page_icon='R',
    layout='wide',
)


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Manrope:wght@400;500;600;700&display=swap');

        :root {
            --ink: #101010;
            --paper: #f6f1e8;
            --card: rgba(255, 255, 255, 0.78);
            --line: rgba(16, 16, 16, 0.08);
            --accent: #d7ff4a;
            --muted: #6f695f;
            --shadow: 0 20px 60px rgba(16, 16, 16, 0.08);
            --radius-xl: 28px;
            --radius-lg: 20px;
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(215, 255, 74, 0.32), transparent 34%),
                radial-gradient(circle at top right, rgba(16, 16, 16, 0.06), transparent 18%),
                linear-gradient(180deg, #f8f4ec 0%, #efe8dd 100%);
            color: var(--ink);
            font-family: 'Manrope', sans-serif;
        }

        .block-container {
            max-width: 1280px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4 {
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        [data-testid='stSidebar'] {
            background: linear-gradient(180deg, #171717 0%, #0d0d0d 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        [data-testid='stSidebar'] * {
            color: #f4f0e8;
        }

        [data-testid='stSidebar'] div[data-baseweb='input'] > div,
        [data-testid='stSidebar'] div[data-baseweb='select'] > div,
        [data-testid='stSidebar'] div[data-testid='stDateInput'] > div,
        [data-testid='stSidebar'] div[data-baseweb='textarea'] > div {
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            border-radius: 16px !important;
        }

        [data-testid='stSidebar'] input,
        [data-testid='stSidebar'] textarea,
        [data-testid='stSidebar'] [role='combobox'],
        [data-testid='stSidebar'] svg {
            color: #f4f0e8 !important;
            fill: #f4f0e8 !important;
            -webkit-text-fill-color: #f4f0e8 !important;
        }

        .account-shell,
        .overview-shell,
        .stats-shell,
        .empty-state {
            background: var(--card);
            backdrop-filter: blur(18px);
            border: 1px solid var(--line);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow);
        }

        .overview-shell {
            padding: 0.95rem 1.2rem;
            margin-bottom: 0.9rem;
            min-height: 112px;
        }

        .stats-shell {
            padding: 1.1rem 1.25rem 1.2rem 1.25rem;
            margin-bottom: 1rem;
        }

        .account-shell {
            padding: 1rem 1.1rem;
            min-height: 148px;
        }

        .eyebrow,
        .section-kicker {
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-size: 0.78rem;
            color: var(--muted);
        }

        .overview-row {
            display: flex;
            align-items: start;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.45rem;
            flex-wrap: wrap;
        }

        .overview-title,
        .account-name,
        .section-title,
        .stats-title {
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            line-height: 0.94;
            margin: 0;
        }

        .overview-title {
            font-size: clamp(1.45rem, 2.4vw, 2rem);
            max-width: 12ch;
        }

        .stats-title {
            font-size: clamp(2.1rem, 4vw, 3rem);
            margin-bottom: 0.35rem;
        }

        .account-name {
            font-size: 2rem;
            margin-top: 0.2rem;
        }

        .section-title {
            font-size: 2.1rem;
        }

        .overview-copy,
        .account-copy,
        .section-copy,
        .stats-copy {
            color: var(--muted);
            line-height: 1.65;
            margin: 0;
        }

        .mini-pill {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: #111111;
            color: #f7f3eb;
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.86rem;
        }

        .section-head {
            margin-bottom: 0.9rem;
        }

        div[data-testid='stMetric'] {
            background: rgba(255,255,255,0.9);
            border: 1px solid var(--line);
            border-radius: var(--radius-lg);
            padding: 1rem 1.05rem;
            box-shadow: 0 12px 30px rgba(16,16,16,0.05);
        }

        div[data-testid='stMetricLabel'] {
            font-family: 'Barlow Condensed', sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.95rem;
        }

        div[data-testid='stMetricValue'] {
            font-family: 'Barlow Condensed', sans-serif;
            font-size: 2.35rem;
        }

        div[data-testid='stForm'],
        div[data-testid='stVerticalBlock'] > div:has(> div[data-testid='stForm']) {
            background: rgba(255,255,255,0.68);
            border: 1px solid var(--line);
            border-radius: var(--radius-xl);
            padding: 1rem;
            box-shadow: var(--shadow);
        }

        div[data-baseweb='input'] > div,
        div[data-baseweb='select'] > div,
        div[data-baseweb='textarea'] > div,
        div[data-testid='stDateInput'] > div {
            border-radius: 16px !important;
            border-color: rgba(16,16,16,0.14) !important;
            background: rgba(255,255,255,0.94) !important;
        }

        .stButton > button,
        button[kind='primary'] {
            border-radius: 999px !important;
            border: none !important;
            min-height: 2.9rem;
            padding: 0.55rem 1.1rem;
            font-family: 'Barlow Condensed', sans-serif !important;
            font-size: 1rem !important;
            text-transform: uppercase !important;
            letter-spacing: 0.08em !important;
            background: #111111 !important;
            color: #f8f5ef !important;
            box-shadow: 0 12px 22px rgba(16,16,16,0.16);
        }

        .stButton > button:hover {
            background: #1d1d1d !important;
        }

        div[data-testid='stDataFrame'] {
            background: rgba(255,255,255,0.76);
            border: 1px solid var(--line);
            border-radius: var(--radius-xl);
            padding: 0.45rem;
            box-shadow: var(--shadow);
        }

        .empty-state {
            padding: 1.4rem;
            color: var(--muted);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_client() -> RunningTrackerApiClient:
    base_url = os.getenv('RUNNING_TRACKER_API_URL', 'http://127.0.0.1:8000')
    return RunningTrackerApiClient(base_url=base_url)


def init_session_state() -> None:
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'auth_dialog' not in st.session_state:
        st.session_state.auth_dialog = None
    if 'distance_unit' not in st.session_state:
        st.session_state.distance_unit = 'Kilometers'


def open_dialog(dialog_name: str) -> None:
    st.session_state.auth_dialog = dialog_name
    st.rerun()


def convert_distance_to_km(distance_value: float, unit: str) -> float:
    if unit == 'Miles':
        return round(distance_value * KM_PER_MILE, 4)
    return round(distance_value, 4)


def convert_distance_from_km(distance_km: float, unit: str) -> float:
    if unit == 'Miles':
        return round(distance_km / KM_PER_MILE, 2)
    return round(distance_km, 2)


@st.dialog('Sign In')
def sign_in_dialog(client: RunningTrackerApiClient) -> None:
    st.markdown("<div class='section-kicker'>Welcome Back</div>", unsafe_allow_html=True)
    with st.form('sign_in_form'):
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')
        submitted = st.form_submit_button('Sign In', use_container_width=True)

        if submitted:
            try:
                user = client.sign_in({'email': email.strip(), 'password': password})
                st.session_state.current_user = user
                st.session_state.auth_dialog = None
                st.success('Signed in successfully.')
                st.rerun()
            except ApiError as exc:
                st.error(f'Could not sign in: {exc}')

    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button('Forgot password?', use_container_width=True):
            open_dialog('reset_password')
    with action_col2:
        if st.button('Create account', use_container_width=True):
            open_dialog('create_account')


@st.dialog('Create Account')
def create_account_dialog(client: RunningTrackerApiClient) -> None:
    st.markdown("<div class='section-kicker'>New Runner</div>", unsafe_allow_html=True)
    with st.form('create_user_form'):
        name = st.text_input('Name')
        email = st.text_input('Email address')
        password = st.text_input('Password', type='password')
        confirm_password = st.text_input('Confirm password', type='password')
        create_user = st.form_submit_button('Create account', use_container_width=True)

        if create_user:
            if not name.strip() or not email.strip() or not password:
                st.warning('Name, email, and password are required.')
            elif password != confirm_password:
                st.warning('Passwords do not match.')
            else:
                try:
                    user = client.create_user(
                        {
                            'name': name.strip(),
                            'email': email.strip(),
                            'password': password,
                        }
                    )
                    st.session_state.current_user = user
                    st.session_state.auth_dialog = None
                    st.success('Account created and signed in.')
                    st.rerun()
                except ApiError as exc:
                    st.error(f'Could not create account: {exc}')

    if st.button('Back to sign in', use_container_width=True):
        open_dialog('sign_in')


@st.dialog('Reset Password')
def reset_password_dialog(client: RunningTrackerApiClient) -> None:
    st.markdown("<div class='section-kicker'>Recovery</div>", unsafe_allow_html=True)
    with st.form('reset_password_form'):
        email = st.text_input('Email address')
        new_password = st.text_input('New password', type='password')
        confirm_password = st.text_input('Confirm new password', type='password')
        reset_submitted = st.form_submit_button('Reset password', use_container_width=True)

        if reset_submitted:
            if not email.strip() or not new_password:
                st.warning('Email and new password are required.')
            elif new_password != confirm_password:
                st.warning('Passwords do not match.')
            else:
                try:
                    client.reset_password({'email': email.strip(), 'new_password': new_password})
                    st.success('Password reset. Please sign in.')
                    open_dialog('sign_in')
                except ApiError as exc:
                    st.error(f'Could not reset password: {exc}')

    if st.button('Back to sign in', use_container_width=True):
        open_dialog('sign_in')


def show_pending_dialog(client: RunningTrackerApiClient) -> None:
    if st.session_state.auth_dialog == 'sign_in':
        sign_in_dialog(client)
    elif st.session_state.auth_dialog == 'create_account':
        create_account_dialog(client)
    elif st.session_state.auth_dialog == 'reset_password':
        reset_password_dialog(client)


def render_account_panel(current_user: dict[str, object] | None) -> None:
    if current_user is None:
        st.markdown(
            """
            <div class='account-shell'>
                <div class='eyebrow'>Account</div>
                <div class='account-name'>Sign In</div>
                <p class='account-copy'>Open your training space and pick up where you left off.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button('Open sign in', use_container_width=True):
            open_dialog('sign_in')
    else:
        st.markdown(
            f"""
            <div class='account-shell'>
                <div class='eyebrow'>Account</div>
                <div class='account-name'>{current_user['name']}</div>
                <p class='account-copy'>{current_user['email']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button('Sign out', use_container_width=True):
            st.session_state.current_user = None
            st.rerun()


def render_overview(current_user: dict[str, object], unit: str) -> None:
    unit_label = 'mi' if unit == 'Miles' else 'km'
    st.markdown(
        f"""
        <div class='overview-shell'>
            <div class='overview-row'>
                <div>
                    <div class='eyebrow'>Performance Overview</div>
                    <div class='overview-title'>Welcome Back, {current_user['name']}.</div>
                </div>
                <div class='mini-pill'>{unit_label} mode</div>
            </div>
            <p class='overview-copy'>Log a session fast and keep your block moving.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stats_summary(stats: dict[str, object], unit: str) -> None:
    unit_label = 'mi' if unit == 'Miles' else 'km'
    total_distance = convert_distance_from_km(float(stats['total_distance_km']), unit)
    weekly_distance = convert_distance_from_km(float(stats['weekly_mileage_km']), unit)

    st.markdown(
        """
        <div class='stats-shell'>
            <div class='eyebrow'>Training Summary</div>
            <div class='stats-title'>Current Block</div>
            <p class='stats-copy'>Your key numbers, with more weight up front.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric('Total Distance', f'{total_distance} {unit_label}')
    col2.metric('Weekly Mileage', f'{weekly_distance} {unit_label}')
    col3.metric('Average Pace', str(stats['average_pace']))
    col4.metric('Training Frequency', str(stats['training_frequency']))


def render_section_head(kicker: str, title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class='section-head'>
            <div class='section-kicker'>{kicker}</div>
            <div class='section-title'>{title}</div>
            <p class='section-copy'>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_runs(runs: list[dict[str, object]], unit: str) -> list[dict[str, object]]:
    unit_label = 'mi' if unit == 'Miles' else 'km'
    speed_label = 'mph' if unit == 'Miles' else 'km/h'
    rows: list[dict[str, object]] = []
    for run in runs:
        speed_value = float(run['avg_speed_kmh']) / KM_PER_MILE if unit == 'Miles' else float(run['avg_speed_kmh'])
        rows.append(
            {
                'Run ID': run['run_id'],
                'Date': run['date'],
                f'Distance ({unit_label})': convert_distance_from_km(float(run['distance_km']), unit),
                'Duration (s)': run['duration_seconds'],
                'Pace': run['avg_pace'],
                f'Speed ({speed_label})': round(speed_value, 2),
                'Heart Rate': run.get('avg_heart_rate') or '-',
                'Elevation Gain': run.get('elevation_gain') or '-',
                'Notes': run.get('notes') or '',
            }
        )
    return rows


def main() -> None:
    inject_styles()
    init_session_state()
    client = get_client()

    show_pending_dialog(client)
    current_user = st.session_state.current_user

    top_left, top_right = st.columns([4.0, 1.35])
    with top_left:
        if current_user is None:
            st.markdown(
                """
                <div class='stats-shell'>
                    <div class='eyebrow'>Daily Movement System</div>
                    <div class='stats-title'>Run Fresh. Track Clean.</div>
                    <p class='stats-copy'>A sharp training space built for quick logging, focused stats, and less friction. Sign in from the account panel to unlock your dashboard.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            try:
                stats = client.get_stats(user_id=current_user['id'])
                render_overview(current_user, st.session_state.distance_unit)
                render_stats_summary(stats, st.session_state.distance_unit)
            except ApiError as exc:
                st.error(f'Could not load stats: {exc}')
    with top_right:
        render_account_panel(current_user)

    with st.sidebar:
        st.markdown("<div class='eyebrow'>Control Room</div>", unsafe_allow_html=True)
        st.markdown('### Session Settings')
        st.write(f"API: `{client.base_url}`")
        st.session_state.distance_unit = st.selectbox(
            'Distance unit',
            options=['Kilometers', 'Miles'],
            index=0 if st.session_state.distance_unit == 'Kilometers' else 1,
        )
        try:
            health = client.get_health()
            st.success(f"Backend status: {health['status']}")
        except Exception as exc:
            st.error(f'Backend unavailable: {exc}')
            st.stop()

    if current_user is None:
        st.markdown(
            """
            <div class='empty-state'>
                <div class='section-kicker'>Ready When You Are</div>
                Sign in to unlock run logging, your performance view, and the history feed. Use the account panel in the top right to sign in, create an account, or reset your password.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.divider()

    left, right = st.columns([1.05, 1.45])
    distance_label = 'Distance (mi)' if st.session_state.distance_unit == 'Miles' else 'Distance (km)'
    max_distance_default = 13.0 if st.session_state.distance_unit == 'Miles' else 21.0

    with left:
        render_section_head(
            'Track Session',
            'Log A Run',
            'Distance can be entered in miles or kilometers. Time starts at thirty minutes and uses split hour, minute, and second controls.',
        )
        with st.form('log_run_form', clear_on_submit=True):
            run_date = st.date_input('Date', value=date.today())
            distance_value = st.number_input(distance_label, min_value=0.1, step=0.1, value=3.0)
            time_col1, time_col2, time_col3 = st.columns(3)
            with time_col1:
                hours = st.number_input('Hours', min_value=0, step=1, value=0)
            with time_col2:
                minutes = st.number_input('Minutes', min_value=0, max_value=59, step=1, value=30)
            with time_col3:
                seconds = st.number_input('Seconds', min_value=0, max_value=59, step=1, value=0)
            avg_heart_rate = st.number_input('Average heart rate', min_value=0, step=1, value=0)
            elevation_gain = st.number_input('Elevation gain', min_value=0.0, step=1.0, value=0.0)
            notes = st.text_area('Notes', placeholder='Effort, route feel, weather, surfaces, or workout notes...')
            submitted = st.form_submit_button('Save run', use_container_width=True)

            if submitted:
                duration_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                if duration_seconds <= 0:
                    st.warning('Run duration must be greater than zero.')
                else:
                    payload = {
                        'user_id': current_user['id'],
                        'date': run_date.isoformat(),
                        'distance_km': convert_distance_to_km(float(distance_value), st.session_state.distance_unit),
                        'duration_seconds': duration_seconds,
                        'avg_heart_rate': int(avg_heart_rate) or None,
                        'elevation_gain': float(elevation_gain) or None,
                        'notes': notes.strip() or None,
                    }
                    try:
                        client.create_run(payload)
                        st.success('Run logged successfully.')
                        st.rerun()
                    except ApiError as exc:
                        st.error(f'Could not log run: {exc}')

    with right:
        render_section_head(
            'History Feed',
            'Review Your Runs',
            'Filter sessions by date and distance while keeping the display aligned with your chosen unit.',
        )
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        with filter_col1:
            start_date = st.date_input('Start date', value=None)
        with filter_col2:
            end_date = st.date_input('End date', value=None)
        with filter_col3:
            min_distance = st.number_input('Min distance', min_value=0.0, step=0.5, value=0.0)
        with filter_col4:
            max_distance = st.number_input('Max distance', min_value=0.0, step=0.5, value=max_distance_default)

        params: dict[str, object] = {'user_id': current_user['id']}
        if start_date:
            params['start_date'] = start_date.isoformat()
        if end_date:
            params['end_date'] = end_date.isoformat()
        if min_distance > 0:
            params['min_distance_km'] = convert_distance_to_km(float(min_distance), st.session_state.distance_unit)
        if max_distance > 0:
            params['max_distance_km'] = convert_distance_to_km(float(max_distance), st.session_state.distance_unit)

        try:
            runs = client.list_runs(params=params)
        except ApiError as exc:
            st.error(f'Could not load runs: {exc}')
            runs = []

        if runs:
            st.dataframe(format_runs(runs, st.session_state.distance_unit), use_container_width=True, hide_index=True)
        else:
            st.markdown(
                """
                <div class='empty-state'>
                    <div class='section-kicker'>No Matching Sessions</div>
                    Tighten the filters or log a new run and the feed will update here.
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == '__main__':
    main()
